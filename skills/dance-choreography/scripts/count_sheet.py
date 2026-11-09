#!/usr/bin/env python3
"""Turn a measured beat grid into dance counts, clip frames and valid clip lengths.

Stdlib only. Beat 0 is at --t0, bars have --beats-per-bar beats, and one dance
count lasts --beats-per-count beats (2 = counting a fast song at half time).

Count table:
  count_sheet.py --bpm 190 --t0 0.036 --beats-per-count 2 --start-bar 17 --bars 16
Where counts fall inside a clip:
  count_sheet.py --bpm 190 --t0 0.036 --beats-per-count 2 --start-bar 17 \
      --clip-start 26.3123 --clip-frames 124 --fps 24
Shortest valid clip for a phrase (grid "17,5" means 17k+5 frames):
  count_sheet.py --bpm 190 --t0 0.036 --fit-seconds 2.526 --lead 0.25 --grid 17,5
"""
import argparse
import math
import sys


def positive(text):
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(f"must be a positive number, got {text}")
    return value


def counts_in_eight(args):
    """Yield (eight_count_no, count_no, seconds) from the start bar onwards."""
    beat = 60.0 / args.bpm
    start = args.t0 + args.start_bar * args.beats_per_bar * beat
    step = args.beats_per_count * beat
    index = 0
    while True:
        yield index // 8 + 1, index % 8 + 1, start + index * step
        index += 1


def print_table(args):
    beat = 60.0 / args.bpm
    total = args.bars * args.beats_per_bar * beat
    eight = 8 * args.beats_per_count * beat
    print(f"BPM {args.bpm:g}; one count {args.beats_per_count * beat:.4f} s; "
          f"one 8-count {eight:.4f} s; start bar {args.start_bar}")
    print()
    print("| 8-count | start s | end s | count 1 to 8 (s) |")
    print("|---:|---:|---:|---|")
    rows = {}
    end = args.t0 + args.start_bar * args.beats_per_bar * beat + total
    for no, _, sec in counts_in_eight(args):
        if sec >= end - 1e-6:
            break
        rows.setdefault(no, []).append(sec)
    for no, secs in rows.items():
        marks = " ".join(f"{s:.3f}" for s in secs)
        print(f"| {no} | {secs[0]:.3f} | {min(secs[0] + eight, end):.3f} | {marks} |")


def print_clip(args):
    print(f"Clip starts {args.clip_start:.4f} s, {args.clip_frames} frames at {args.fps:g} fps")
    print()
    print("| 8-count | count | song s | clip frame |")
    print("|---:|---:|---:|---:|")
    clip_end = args.clip_start + args.clip_frames / args.fps
    for no, count, sec in counts_in_eight(args):
        if sec >= clip_end:
            break
        if sec >= args.clip_start:
            print(f"| {no} | {count} | {sec:.3f} | {(sec - args.clip_start) * args.fps:.1f} |")


def print_fit(args):
    try:
        step, offset = (int(part) for part in args.grid.split(","))
    except ValueError:
        sys.exit("--grid must look like 17,5")
    if step <= 0 or offset < 0:
        sys.exit("--grid needs a positive step and a non-negative offset")
    need = (args.fit_seconds + args.lead) * args.fps
    k = max(0, math.ceil((need - offset) / step))
    frames = step * k + offset
    print(f"Need {need:.1f} frames ({args.fit_seconds:g} s + {args.lead:g} s lead); "
          f"shortest valid: {frames} frames = {frames / args.fps:.3f} s")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bpm", type=positive, required=True)
    parser.add_argument("--t0", type=float, default=0.0, help="time of beat 0 in seconds")
    parser.add_argument("--beats-per-bar", type=int, default=4)
    parser.add_argument("--beats-per-count", type=int, default=1,
                        help="grid beats in one dance count; 2 counts a fast song at half time")
    parser.add_argument("--start-bar", type=int, default=0, help="zero-based bar index where 8-count 1 begins; 0 is the first bar")
    parser.add_argument("--bars", type=int, help="print a count table for this many bars")
    parser.add_argument("--clip-start", type=float, help="clip start time in the song, seconds")
    parser.add_argument("--clip-frames", type=int, help="clip length in frames")
    parser.add_argument("--fps", type=positive, default=24.0)
    parser.add_argument("--fit-seconds", type=positive, help="phrase length to fit into a clip")
    parser.add_argument("--lead", type=float, default=0.0, help="lead-in seconds before the phrase")
    parser.add_argument("--grid", default="17,5", help="valid frame counts as step,offset")
    args = parser.parse_args()

    for name in ("t0", "clip_start", "lead"):
        value = getattr(args, name)
        if value is not None and not math.isfinite(value):
            parser.error(f"--{name.replace('_', '-')} must be a finite number")
    if args.beats_per_bar <= 0 or args.beats_per_count <= 0:
        parser.error("--beats-per-bar and --beats-per-count must be positive")
    if args.start_bar < 0 or args.lead < 0:
        parser.error("--start-bar and --lead cannot be negative")
    if args.bars is not None and args.bars <= 0:
        parser.error("--bars must be positive")
    if (args.clip_start is None) != (args.clip_frames is None):
        parser.error("--clip-start and --clip-frames go together")
    if args.clip_frames is not None and args.clip_frames <= 0:
        parser.error("--clip-frames must be positive")
    if args.bars is None and args.clip_start is None and args.fit_seconds is None:
        parser.error("choose --bars, --clip-start with --clip-frames, or --fit-seconds")

    if args.bars is not None:
        print_table(args)
    if args.clip_start is not None:
        print_clip(args)
    if args.fit_seconds is not None:
        print_fit(args)


if __name__ == "__main__":
    main()
