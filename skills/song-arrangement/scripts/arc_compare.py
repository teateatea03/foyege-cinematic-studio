#!/usr/bin/env python3
"""Compare songs from their 4-stem separations (drums, bass, other, vocals): spectrum, width, section contrast, harmony, melody, drum repetition.
Run the same separator on every song. Chords are estimates and pitch tracking is inflated by stacked vocals, so compare directions, not exact values.
Files are <dir>/<tag>_<stem>.wav. Usage: arc_compare.py name=dir:tag [name=dir:tag ...]"""
import json, pathlib, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np, soundfile as sf, librosa
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
SONGS = {}
for arg in sys.argv[1:]:
    name, rest = arg.split('=', 1)
    d, tag = rest.rsplit(':', 1)
    SONGS[name] = (pathlib.Path(d), tag)
if not SONGS:
    sys.exit(__doc__)
BANDS = [(20, 80), (80, 300), (300, 2000), (2000, 6000), (6000, 14000)]
SR = 22050
NOTE = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def load(d, tag):
    st = {}
    for k in ('drums', 'bass', 'other', 'vocals'):
        a, sr = sf.read(d / f'{tag}_{k}.wav', always_2d=True, dtype='float32')
        st[k] = a
    return st, sr


def templates():
    t = []
    names = []
    for r in range(12):
        for q, iv in (('', (0, 4, 7)), ('m', (0, 3, 7))):
            v = np.zeros(12)
            for i in iv:
                v[(r + i) % 12] = 1
            t.append(v / np.linalg.norm(v))
            names.append(NOTE[r] + q)
    return np.array(t), names


T, CH = templates()
OUT = {}
for name, (d, tag) in SONGS.items():
    st, sr = load(d, tag)
    n = min(len(v) for v in st.values())
    st = {k: v[:n] for k, v in st.items()}
    back = st['drums'] + st['bass'] + st['other']
    mix = back + st['vocals']
    mono = mix.mean(1)
    rec = {'sec': round(n / sr, 1)}
    # spectrum of the whole mix
    S = np.abs(librosa.stft(mono, n_fft=4096, hop_length=2048)) ** 2
    f = librosa.fft_frequencies(sr=sr, n_fft=4096)
    tot = S.sum()
    rec['bands'] = [round(float(10 * np.log10(S[(f >= a) & (f < b)].sum() / tot)), 1) for a, b in BANDS]
    # stereo width, side over mid
    wid = lambda a: round(float(db(a[:, 0] - a[:, 1]) - db(a[:, 0] + a[:, 1])), 1)
    rec['width'] = {'back': wid(back), 'other': wid(st['other']), 'vocals': wid(st['vocals'])}
    # shares
    e = {k: float((v ** 2).sum()) for k, v in st.items()}
    t = sum(e.values())
    rec['share'] = {k: round(100 * v / t) for k, v in e.items()}
    # eight-second windows across the song
    w, h = int(sr * 8), int(sr * 2)
    idx = range(0, n - w, h)
    lev = {k: np.array([db(st[k][i:i + w]) for i in idx]) for k in st}
    lb = np.array([db(back[i:i + w]) for i in idx])
    rg = lambda a: round(float(np.percentile(a, 90) - np.percentile(a, 10)), 1)
    rec['range_back'] = rg(lb)
    rec['range'] = {k: rg(v) for k, v in lev.items()}
    rec['drums_off_pct'] = round(float((lev['drums'] < np.median(lev['drums']) - 15).mean() * 100), 1)
    rec['voc_off_pct'] = round(float((lev['vocals'] < np.median(lev['vocals']) - 15).mean() * 100), 1)
    # brightness of the backing across the song, and how different its textures get
    bm = librosa.resample(back.mean(1), orig_sr=sr, target_sr=SR)
    cent = librosa.feature.spectral_centroid(y=bm, sr=SR, hop_length=1024)[0]
    fr = 8 * SR // 1024
    ce = np.array([np.median(cent[i:i + fr]) for i in range(0, len(cent) - fr, fr // 4)])
    rec['bright_oct'] = round(float(np.log2(np.percentile(ce, 90) / np.percentile(ce, 10))), 2)
    mf = librosa.feature.mfcc(y=bm, sr=SR, n_mfcc=14, hop_length=1024)[1:]
    wn = 4 * SR // 1024
    v = np.array([mf[:, i:i + wn].mean(1) for i in range(0, mf.shape[1] - wn, wn)])
    v = v - v.mean(0)
    v = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)
    sim = v @ v.T
    rec['texture_spread'] = round(float(1 - np.abs(sim[np.triu_indices(len(v), 1)]).mean()), 3)
    # harmony per bar from the pitched backing, bars from the beat grid
    tempo, beats = librosa.beat.beat_track(y=librosa.resample(st['drums'].mean(1), orig_sr=sr, target_sr=SR), sr=SR, hop_length=512)
    tempo = float(np.atleast_1d(tempo)[0])
    pit = librosa.resample((st['other'] + st['bass']).mean(1), orig_sr=sr, target_sr=SR)
    chroma = librosa.feature.chroma_cqt(y=pit, sr=SR, hop_length=512)
    bars = beats[::4]
    lab = []
    for a, b in zip(bars[:-1], bars[1:]):
        c = chroma[:, a:b].mean(1)
        lab.append(CH[int(np.argmax(T @ (c / (np.linalg.norm(c) + 1e-9))))])
    cnt = Counter(lab)
    tb = len(lab)
    rec['tempo'] = round(tempo, 1)
    rec['bars'] = tb
    rec['chords_ge2pct'] = sum(v >= .02 * tb for v in cnt.values())
    rec['top4_share'] = round(sum(v for _, v in cnt.most_common(4)) / tb * 100)
    rec['top_chords'] = [f'{k} {round(v / tb * 100)}%' for k, v in cnt.most_common(6)]
    grams = Counter(tuple(lab[i:i + 4]) for i in range(0, tb - 3))
    rec['top_4bar_loop_share'] = round(grams.most_common(1)[0][1] / (tb - 3) * 100)
    rec['distinct_4bar'] = len(grams)
    # drum pattern repetition, 16 slots per bar
    dr = librosa.onset.onset_strength(y=librosa.resample(st['drums'].mean(1), orig_sr=sr, target_sr=SR), sr=SR, hop_length=512)
    pats = []
    for a, b in zip(bars[:-1], bars[1:]):
        if b - a < 16:
            continue
        ix = np.linspace(a, b, 17).astype(int)
        pats.append([dr[ix[i]:ix[i + 1]].max() if ix[i + 1] > ix[i] else 0 for i in range(16)])
    p = np.array(pats)
    p = (p - p.mean(1, keepdims=True)) / (p.std(1, keepdims=True) + 1e-9)
    cc = (p[:-1] * p[1:]).mean(1)
    rec['drum_next_bar_corr'] = round(float(np.median(cc)), 2)
    rec['drum_change_bars_pct'] = round(float((cc < .5).mean() * 100), 1)
    # melody
    y = librosa.resample(st['vocals'].mean(1), orig_sr=sr, target_sr=SR)
    f0 = librosa.yin(y, fmin=120, fmax=1300, sr=SR, frame_length=2048, hop_length=512)
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    m = min(len(f0), len(rms))
    f0, rms = f0[:m], rms[:m]
    voiced = rms > np.percentile(rms, 40)
    mid = librosa.hz_to_midi(f0)
    dt = 512 / SR
    q = mid[voiced]
    rec['pitch_p5_p95'] = round(float(np.percentile(q, 95) - np.percentile(q, 5)), 1)
    # register arc: median pitch per 8 s window
    fr = int(8 / dt)
    arc = np.array([np.median(mid[i:i + fr][voiced[i:i + fr]]) for i in range(0, m - fr, fr // 2) if voiced[i:i + fr].mean() > .2])
    rec['register_arc'] = rg(arc)
    # notes: runs within half a semitone of their running median, at least 70 ms
    notes = []
    i = 0
    while i < m:
        if not voiced[i]:
            i += 1
            continue
        j = i
        while j + 1 < m and voiced[j + 1] and abs(mid[j + 1] - np.median(mid[i:j + 1])) < .6:
            j += 1
        if (j - i + 1) * dt >= .07:
            notes.append((float(np.median(mid[i:j + 1])), (j - i + 1) * dt, i * dt))
        i = j + 1
    pn = np.array([x[0] for x in notes])
    du = np.array([x[1] for x in notes])
    st_time = np.array([x[2] for x in notes])
    # two notes connect when the silence between them is short, however long the first note lasts
    iv = np.abs(np.diff(pn))[st_time[1:] - (st_time[:-1] + du[:-1]) < 1.0] if len(notes) > 1 else np.array([])
    rec['notes_per_s'] = round(len(notes) / max(voiced.sum() * dt, dt), 2)
    rec['repeat_pct'] = round(float((iv < 1).mean() * 100)) if len(iv) else None
    rec['step_pct'] = round(float(((iv >= 1) & (iv < 3)).mean() * 100)) if len(iv) else None
    rec['leap5_pct'] = round(float((iv >= 5).mean() * 100)) if len(iv) else None
    rec['mean_iv'] = round(float(iv.mean()), 2) if len(iv) else None
    rec['long_note_pct_time'] = round(float(du[du >= .5].sum() / du.sum() * 100)) if len(notes) else None
    pc = Counter(int(round(x)) % 12 for x in pn)
    tp = sum(pc.values())
    rec['pitch_classes'] = [f'{NOTE[k]} {round(v / tp * 100)}' for k, v in pc.most_common(7)]
    p_ = np.array(list(pc.values())) / tp
    rec['pc_entropy_bits'] = round(float(-(p_ * np.log2(p_)).sum()), 2)
    OUT[name] = rec
    print(name, 'ok', flush=True)
ks = list(OUT)
print('\n' + 'metric'.ljust(24) + ''.join(k.rjust(9) for k in ks))
for key in ('sec', 'tempo', 'bars', 'range_back', 'drums_off_pct', 'voc_off_pct', 'bright_oct', 'texture_spread', 'chords_ge2pct', 'top4_share', 'top_4bar_loop_share', 'distinct_4bar', 'drum_next_bar_corr', 'drum_change_bars_pct', 'pitch_p5_p95', 'register_arc', 'notes_per_s', 'repeat_pct', 'step_pct', 'leap5_pct', 'mean_iv', 'long_note_pct_time', 'pc_entropy_bits'):
    print(key.ljust(24) + ''.join(str(OUT[k][key]).rjust(9) for k in ks))
for sub in ('range', 'share', 'width'):
    for key in OUT[ks[0]][sub]:
        print(f'{sub}.{key}'.ljust(24) + ''.join(str(OUT[k][sub][key]).rjust(9) for k in ks))
for i, b in enumerate(BANDS):
    print(f'band {b[0]}-{b[1]}'.ljust(24) + ''.join(str(OUT[k]['bands'][i]).rjust(9) for k in ks))
for k in ks:
    print(k, 'chords', OUT[k]['top_chords'], '| notes', OUT[k]['pitch_classes'])
