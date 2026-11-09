"""Compare a generated still with the blockout render of the same camera.

    python overlay_check.py --blockout cam_C1_day.png --image still.png --out OUT_DIR

Writes OUT_DIR/overlay_50.png (50 % blend), OUT_DIR/edges.png (blockout edges red, still edges cyan)
and OUT_DIR/overlay_check.json. OUT_DIR must not exist yet.

layout_match is the share of the blockout's vertical and horizontal edges (the lower of the two) that the still
also has within --radius pixels. It says whether the big shapes (walls, door, window, furniture outlines) landed
in the same place; it does not judge style or detail. Light changes it too, so rank candidates for one camera
and one time of day by it, then look at edges.png yourself. Measured on renders of the sample room:
same geometry 0.91-0.95 (similar light) and 0.65-0.77 (night lamp vs day); shifted 1-2 % or zoomed 3 %: 0.52-0.59;
another camera 0.49.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageStat


def fit(im, size):
    """Center-crop im to the aspect of size, then resize to size."""
    w, h = im.size
    tw, th = size
    if abs(w / h - tw / th) > 0.01:
        if w / h > tw / th:
            nw = round(h * tw / th)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = round(w * th / tw)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize(size, Image.LANCZOS)


WORK_W = 640  # compare at this width: removes render noise and fine texture


def edges(im):
    """Edge strength, scaled x3 so the lines are visible; flat render noise stays near 0."""
    g = im.convert("L").filter(ImageFilter.GaussianBlur(1.0)).filter(ImageFilter.FIND_EDGES)
    return g.point(lambda v: min(255, v * 3))


SOBEL_X = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
SOBEL_Y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]


def oriented_edges(im, threshold):
    """Binary maps of vertical edges (from the x gradient) and horizontal edges (from the y gradient).
    Matching them separately catches a frame that slid along a line, which one combined map misses."""
    g = im.convert("L").filter(ImageFilter.GaussianBlur(1.0))
    out = []
    for k in (SOBEL_X, SOBEL_Y):
        pos = g.filter(ImageFilter.Kernel((3, 3), k, scale=1))
        neg = g.filter(ImageFilter.Kernel((3, 3), [-v for v in k], scale=1))
        mag = ImageChops.lighter(pos, neg)
        out.append(mag.point(lambda v: 255 if v >= threshold else 0).convert("1"))
    return out


def count_on(binary):
    return binary.convert("L").histogram()[255]


def matched(a_bin, b_bin, radius):
    """Share of a's edge pixels that have a b edge pixel within radius."""
    near_b = b_bin.convert("L").filter(ImageFilter.MaxFilter(2 * radius + 1)).point(lambda v: 255 if v else 0).convert("1")
    hit = count_on(ImageChops.logical_and(a_bin, near_b))
    return hit / max(1, count_on(a_bin))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blockout", type=Path, required=True)
    ap.add_argument("--image", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--threshold", type=int, default=60, help="scaled edge strength 0-255 counted as an edge")
    ap.add_argument("--radius", type=int, default=3, help="pixels (at 640 wide) an edge may move and still count")
    ap.add_argument("--sobel-threshold", type=int, default=40, help="gradient strength counted as an oriented edge")
    args = ap.parse_args()
    a_full = Image.open(args.blockout).convert("RGB")
    b_raw = Image.open(args.image).convert("RGB")
    args.out.mkdir(parents=True, exist_ok=False)
    Image.blend(a_full, fit(b_raw, a_full.size), 0.5).save(args.out / "overlay_50.png")

    work = (WORK_W, round(WORK_W * a_full.size[1] / a_full.size[0]))
    a = a_full.resize(work, Image.LANCZOS)
    b = fit(b_raw, work)
    ea, eb = edges(a), edges(b)

    rms = ImageStat.Stat(ImageChops.difference(ea, eb)).rms[0]
    psnr = 99.0 if rms == 0 else 20 * math.log10(255 / rms)
    radius = args.radius
    (av, ah), (bv, bh) = oriented_edges(a, args.sobel_threshold), oriented_edges(b, args.sobel_threshold)
    found_v, found_h = matched(av, bv, radius), matched(ah, bh, radius)
    # picture: the still, dimmed, with blockout edges in red and still edges in cyan
    base = b.convert("L").point(lambda v: v // 3)
    a_lines = ImageChops.logical_or(av, ah).convert("L")
    b_lines = ImageChops.logical_or(bv, bh).convert("L")
    pic = Image.merge("RGB", (ImageChops.lighter(base, a_lines), ImageChops.lighter(base, b_lines), ImageChops.lighter(base, b_lines)))
    pic.resize((work[0] * 2, work[1] * 2), Image.NEAREST).save(args.out / "edges.png")
    a_bin = ea.point(lambda v: 255 if v >= args.threshold else 0).convert("1")
    b_bin = eb.point(lambda v: 255 if v >= args.threshold else 0).convert("1")
    report = {
        "blockout": str(args.blockout), "blockout_sha256": hashlib.sha256(args.blockout.read_bytes()).hexdigest(),
        "image": str(args.image), "image_sha256": hashlib.sha256(args.image.read_bytes()).hexdigest(),
        "image_size": list(b_raw.size), "compared_at": list(a.size),
        "aspect_cropped": abs(b_raw.size[0] / b_raw.size[1] - a.size[0] / a.size[1]) > 0.01,
        "edge_psnr_db": round(psnr, 2),
        "layout_match": round(min(found_v, found_h), 3),
        "vertical_edges_found": round(found_v, 3),
        "horizontal_edges_found": round(found_h, 3),
        "blockout_edges_found_in_image": round(matched(a_bin, b_bin, radius), 3),
        "image_edges_found_in_blockout": round(matched(b_bin, a_bin, radius), 3),
        "match_radius_px": radius,
        "note": "blockout_edges_found_in_image matters most: did the walls, openings and furniture outlines land in place. "
                "The second number is low whenever the still adds texture and props, which is expected.",
    }
    (args.out / "overlay_check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.write(json.dumps({k: report[k] for k in ("layout_match", "vertical_edges_found", "horizontal_edges_found",
                                                         "blockout_edges_found_in_image", "edge_psnr_db", "aspect_cropped")}) + "\n")


if __name__ == "__main__":
    main()
