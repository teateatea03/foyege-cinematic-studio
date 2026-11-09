"""Render original, frame-addressable system cards with an explicitly supplied font."""
import argparse
import hashlib
import json
from pathlib import Path
import platform

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


def load_config(path):
    config = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    for key in ("width", "height", "fps", "frame_count"):
        if type(config.get(key)) is not int or config[key] < 1:
            raise ValueError(f"{key} must be a positive integer")
    if (config["width"], config["height"]) != (960, 540):
        raise ValueError("this draft template supports 960x540 only")
    cues = config.get("cues")
    if not isinstance(cues, list) or not cues:
        raise ValueError("require nonempty cues")
    cursor = 0
    for cue in cues:
        if (type(cue.get("start")) is not int or type(cue.get("end")) is not int
                or cue["start"] != cursor or cue["end"] <= cursor):
            raise ValueError("cue intervals must be contiguous [start,end)")
        if cue.get("style") not in {"boot", "error", "hold"}:
            raise ValueError("unknown card style")
        if not isinstance(cue.get("title"), str) or not isinstance(cue.get("detail"), str):
            raise ValueError("title and detail must be strings")
        cursor = cue["end"]
    if cursor != config["frame_count"]:
        raise ValueError("cues must cover exactly frame_count")
    return config


def fonts(path):
    return {size: ImageFont.truetype(str(path), size=size) for size in (18, 22, 30, 52)}


def render_frame(config, typefaces, frame):
    if type(frame) is not int or not 0 <= frame < config["frame_count"]:
        raise ValueError("frame outside timeline")
    cue = next(c for c in config["cues"] if c["start"] <= frame < c["end"])
    accent = "#ff637c" if cue["style"] == "error" else "#65e5d1"
    image = Image.new("RGB", (960, 540), "#0b111b")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((36, 32, 924, 508), radius=16, outline="#304054", width=2)
    draw.text((68, 62), "HITOMI / SYSTEM CONSOLE", font=typefaces[22], fill=accent)
    draw.text((68, 105), "DRAFT  ·  字卡示例 / 尚未綁定歌曲", font=typefaces[18], fill="#8899ad")
    draw.line((68, 150, 892, 150), fill="#304054", width=2)
    for text, size, limit in [(cue["title"], 52, 816), (cue["detail"], 30, 816)]:
        if draw.textbbox((0, 0), text, font=typefaces[size])[2] > limit:
            raise ValueError("text overflows template; shorten text or adapt layout explicitly")
    draw.text((68, 205), cue["title"], font=typefaces[52], fill="#eef5ff")
    draw.text((68, 290), cue["detail"], font=typefaces[30], fill="#b3c4d6")
    if cue["style"] == "boot":
        fraction = (frame - cue["start"]) / max(1, cue["end"] - cue["start"] - 1)
        fraction = fraction * fraction * (3 - 2 * fraction)
        draw.rounded_rectangle((68, 382, 892, 394), radius=6, fill="#253246")
        right = 68 + round(824 * fraction)
        if right > 68:
            draw.rectangle((68, 382, right, 394), fill=accent)
    elif cue["style"] == "error":
        # Continuous movement, no random state or flash; exact frame can be revisited.
        offset = round(60 * (frame - cue["start"]) / max(1, cue["end"] - cue["start"] - 1))
        draw.line((68 + offset, 388, 380 + offset, 388), fill=accent, width=5)
    else:
        draw.line((68, 388, 892, 388), fill=accent, width=3)
    draw.text((68, 450), "LOCAL ASSETS  /  NO AUDIO  /  REVIEW REQUIRED", font=typefaces[18], fill="#8899ad")
    return image


def render(config_path, font_path, output):
    config_raw = Path(config_path).read_bytes()
    font_sha = hashlib.sha256(Path(font_path).read_bytes()).hexdigest()
    config = load_config(config_path)
    typefaces = fonts(font_path)
    if Path(config_path).read_bytes() != config_raw:
        raise ValueError("configuration changed during preparation")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    frames = output / "frames"
    frames.mkdir()
    incomplete = output / "INCOMPLETE"
    incomplete.write_text("Render pending. Do not treat as accepted output.\n", encoding="utf-8")
    receipt = {"schema_version": 1, "config": config,
               "config_sha256": hashlib.sha256(config_raw).hexdigest(),
               "font_sha256": font_sha,
               "font_name": Path(font_path).name, "pillow": pillow_version,
               "python": platform.python_version(), "frames": [], "audio": None,
               "scope": "draft graphics; timing is illustrative and not aligned to a song"}
    for frame in range(config["frame_count"]):
        image = render_frame(config, typefaces, frame)
        name = f"{frame:06d}.png"
        image.save(frames / name)
        receipt["frames"].append({"frame": frame, "file": name,
                                  "rgb_sha256": hashlib.sha256(image.tobytes()).hexdigest()})
    if (Path(config_path).read_bytes() != config_raw
            or hashlib.sha256(Path(font_path).read_bytes()).hexdigest() != font_sha):
        raise ValueError("configuration/font changed during render; output remains INCOMPLETE")
    with (output / "render.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    incomplete.unlink()
    return {"frames": config["frame_count"], "fps": config["fps"], "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--font", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.config, args.font, args.out), ensure_ascii=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
