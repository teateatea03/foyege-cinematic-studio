#!/usr/bin/env python3
"""What an ABC score contains, section by section: pitch variety, repeated notes, leaps, rests, chords.
Sections are `% label` comment lines; voices are `V: Vocal` and `V: Ins`, as in YuE2 scores.
Usage: score_stats.py name=path.abc [name=path.abc ...]"""
import pathlib, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
TOK = re.compile(r"\[K:([^\]]+)\]|(\|)|(\^\^|__|\^|_|=)?([A-Ga-gzx])([,']*)(\d*)(/*)(\d*)")
SCALE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ALTER = {'^^': 2, '^': 1, '=': 0, '_': -1, '__': -2}
FIFTHS = {'Cb': -7, 'Gb': -6, 'Db': -5, 'Ab': -4, 'Eb': -3, 'Bb': -2, 'F': -1, 'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7, 'G#': 8, 'D#': 9, 'A#': 10}


def key_alters(key):
    """Letter -> semitones from a major or minor key field such as Fm, Bbm, Eb, C. Other modes stop the script rather than miscount."""
    m = re.fullmatch(r'\s*([A-G][b#]?)\s*(m|min|minor|maj|major)?\s*', key)
    if not m or m[1] not in FIFTHS:
        sys.exit(f'unsupported key field: K:{key}')
    n = FIFTHS[m[1]] - (3 if m[2] in ('m', 'min', 'minor') else 0)
    if not -7 <= n <= 7:
        sys.exit(f'unsupported key field: K:{key}')
    order = 'FCGDAEB' if n > 0 else 'BEADGCF'
    return {c: (1 if n > 0 else -1) for c in order[:abs(n)]}


def parse(block):
    """(diatonic position, semitone, length) per note; rests are ('z', None, length). Accidentals hold to the end of the bar
    for that letter in every octave, as YuE2's native ABC does (see its yue2-music skill, references/abc-editing.md)."""
    block = re.sub(r'"[^"]*"|![^!]*!', ' ', block)
    block = re.sub(r'\[(?!K:)[^\]]*\]', ' ', block)
    key, bar, out = {}, {}, []
    for m in TOK.finditer(block):
        if m[1]:
            key, bar = key_alters(m[1]), {}
        elif m[2]:
            bar = {}
        else:
            num = int(m[6] or 1)
            length = num / (2 ** len(m[7]) if m[7] and not m[8] else int(m[8] or 1))
            if m[4] in 'zx':
                out.append(('z', None, length))
                continue
            letter = m[4].upper()
            octave = (1 if m[4].islower() else 0) + m[5].count("'") - m[5].count(',')
            if m[3]:
                bar[letter] = ALTER[m[3]]
            alter = bar.get(letter, key.get(letter, 0))
            out.append(('CDEFGAB'.index(letter) + 7 * octave, SCALE[letter] + 12 * octave + alter, length))
    return out


def stats(label, vocal, chords):
    ns = parse(vocal)
    notes = [(x, s) for x, s, _ in ns if x != 'z']
    if not notes:
        return f'{label:14s} no sung notes'
    p = [x for x, _ in notes]
    s = [y for _, y in notes]
    total = sum(k for _, _, k in ns)
    rest = sum(k for x, _, k in ns if x == 'z')
    rep = 100 * sum(a == b for a, b in zip(s, s[1:])) / max(1, len(s) - 1)
    leap = 100 * sum(abs(a - b) >= 4 for a, b in zip(p, p[1:])) / max(1, len(p) - 1)
    return (f'{label:14s} notes {len(p):4d}  pitches {len(set(s)):2d}  range {max(p) - min(p):2d} steps  '
            f'repeat {rep:3.0f}%  leaps>=5th {leap:3.0f}%  rests {100 * rest / (total or 1):3.0f}%  '
            f'chords {dict(Counter(chords).most_common(6))}')


def sections(text):
    out, cur, voice = {}, None, None
    keys = {'Vocal': 'C', 'Ins': 'C'}  # the key in force per voice, so an inline [K:x] carries into the next section
    for line in text.splitlines():
        if line.startswith('% '):
            base, key, i = line[2:].strip(), line[2:].strip(), 2
            while key in out:
                key, i = f'{base} {i}', i + 1
            cur = key
            out[cur] = {'Vocal': f"[K:{keys['Vocal']}] ", 'Ins': f"[K:{keys['Ins']}] ", 'chords': []}
            continue
        m = re.match(r'V:[ \t]*(\S+)', line)
        if m:
            voice = m[1]
        elif re.match(r'K:', line):
            keys['Vocal'] = keys['Ins'] = re.split(r'%', line[2:])[0].strip()
            if cur:
                out[cur]['Vocal'] += f"[K:{keys['Vocal']}] "
                out[cur]['Ins'] += f"[K:{keys['Ins']}] "
        elif line.startswith('%') or re.match(r'[A-Za-z+]:', line):
            continue  # comments, lyrics (w:) and other fields are not notes
        elif cur and voice in ('Vocal', 'Ins'):
            line = line.split('%', 1)[0]  # a trailing comment is not notes
            out[cur][voice] += line + ' '
            for k in re.findall(r'\[K:([^\]]+)\]', line):
                keys[voice] = k.strip()
            if voice == 'Vocal':
                out[cur]['chords'] += re.findall(r'"([^"]+)"', line)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        name, path = arg.split('=', 1)
        print('==', name)
        for k, v in sections(pathlib.Path(path).read_text(encoding='utf-8')).items():
            q = [x for x, _, _ in parse(v['Ins']) if x != 'z']
            print(stats(k, v['Vocal'], v['chords']), f' | instrument notes {len(q)}')
