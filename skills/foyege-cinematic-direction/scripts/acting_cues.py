"""Map declared audio sample cues to a constant-rate timeline; no ASR or media I/O."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def ratio(data, name):
    if not isinstance(data, dict):
        raise ValueError(f"{name} requires num/den")
    return Fraction(integer(data.get("num"), name + ".num", 1),
                    integer(data.get("den"), name + ".den", 1))


def exact(value):
    return {"num": value.numerator, "den": value.denominator}


def build(data):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("require schema_version 1")
    if not isinstance(data.get("shot_id"), str) or not data["shot_id"].strip():
        raise ValueError("require shot_id")
    audio, timeline = data["audio"], data["timeline"]
    expected_timeline = {"mode", "fps", "start_frame", "frame_count", "audio_in_sample", "audio_playback_rate"}
    if (not isinstance(timeline, dict) or set(timeline) != expected_timeline
            or timeline["mode"] != "constant_audio_rate_cfr"):
        raise ValueError("only explicit constant_audio_rate_cfr timeline fields are supported")
    if not isinstance(audio.get("asset_id"), str) or not audio["asset_id"].strip():
        raise ValueError("require audio.asset_id")
    sha = audio.get("sha256")
    if sha is not None and (not isinstance(sha, str) or not re.fullmatch("[0-9a-f]{64}", sha)):
        raise ValueError("audio.sha256 must be null or lowercase SHA256")
    sample_rate = integer(audio.get("sample_rate"), "sample_rate", 1)
    fps = ratio(timeline.get("fps"), "fps")
    speed = ratio(timeline.get("audio_playback_rate"), "audio_playback_rate")
    start = integer(timeline.get("start_frame"), "start_frame")
    count = integer(timeline.get("frame_count"), "frame_count", 1)
    source_in = integer(timeline.get("audio_in_sample"), "audio_in_sample")
    events, reactions = data.get("events"), data.get("reactions")
    if not isinstance(events, list) or not isinstance(reactions, list):
        raise ValueError("events and reactions must be lists")
    if not events or not reactions:
        raise ValueError("require at least one event and reaction")
    by_id, prior_reactions, event_rows, reaction_rows, issues = {}, {}, [], [], []
    needs_binding = sha is None
    all_ids = set()
    for event in events:
        label = event.get("id")
        if not isinstance(label, str) or not label.strip() or label in all_ids:
            raise ValueError("event/reaction ids must be nonempty and unique")
        all_ids.add(label)
        sample = integer(event.get("source_sample"), "source_sample")
        text = event.get("text", "")
        if not isinstance(text, str):
            raise ValueError("event text must be a string")
        evidence = event.get("evidence")
        if evidence not in {"provisional", "alignment", "manual"}:
            raise ValueError("evidence must be provisional, alignment or manual")
        needs_binding |= evidence == "provisional"
        position = Fraction(start) + Fraction(sample - source_in, sample_rate) * fps / speed
        if not start <= position < start + count:
            raise ValueError(f"{label}: cue outside this clip; choose the actual audio timeline region")
        containing = position.numerator // position.denominator
        safe = -(-position.numerator // position.denominator)
        by_id[label] = (position, safe, evidence)
        event_rows.append({"id": label, "text": text, "source_sample": sample, "evidence": evidence,
                           "timeline_frame_exact": exact(position),
                           "containing_frame": containing, "first_boundary_not_before": safe})
    for reaction in reactions:
        label = reaction.get("id")
        if not isinstance(label, str) or not label.strip() or label in all_ids:
            raise ValueError("event/reaction ids must be nonempty and unique")
        all_ids.add(label)
        intent = reaction.get("intent", "")
        if not isinstance(intent, str):
            raise ValueError("reaction intent must be a string")
        trigger = reaction.get("trigger")
        if trigger not in by_id:
            raise ValueError(f"{label}: unknown trigger")
        position, safe, evidence = by_id[trigger]
        planned = integer(reaction.get("planned_frame"), "planned_frame")
        hold_end = integer(reaction.get("hold_end_frame"), "hold_end_frame")
        if not start <= planned < hold_end <= start + count:
            raise ValueError(f"{label}: require start <= planned < hold_end <= clip end")
        observed = reaction.get("observed_frame")
        if observed is not None:
            integer(observed, "observed_frame")
            if not start <= observed < start + count:
                raise ValueError(f"{label}: observed frame outside clip")
        dependency = reaction.get("after_reaction")
        gap = integer(reaction.get("min_gap_frames", 0), "min_gap_frames")
        if dependency is not None:
            if dependency not in prior_reactions:
                raise ValueError(f"{label}: after_reaction must name an earlier reaction row")
            prior = prior_reactions[dependency]
            if planned < prior["planned_frame"] + gap:
                issues.append({"id": label, "kind": "planned_reaction_order"})
            if (observed is not None and prior["observed_frame"] is not None
                    and observed < prior["observed_frame"] + gap):
                issues.append({"id": label, "kind": "observed_reaction_order"})
        elif gap:
            raise ValueError("min_gap_frames requires after_reaction")
        prior_reactions[label] = {"planned_frame": planned, "observed_frame": observed}
        if planned < position:
            issues.append({"id": label, "kind": "planned_before_trigger"})
        if observed is not None and observed < position:
            issues.append({"id": label, "kind": "observed_before_trigger"})
        reaction_rows.append({"id": label, "intent": intent, "trigger": trigger, "planned_frame": planned,
                              "first_boundary_not_before": safe, "hold_end_frame_exclusive": hold_end,
                              "after_reaction": dependency, "min_gap_frames": gap,
                              "planned_delay_frames_exact": exact(Fraction(planned) - position),
                              "observed_frame": observed,
                              "observation": "not_measured" if observed is None else "caller_declared"})
    return {"schema_version": 1, "shot_id": data["shot_id"],
            "status": "needs_review" if issues else ("provisional" if needs_binding else "plan_consistent"),
            "audio": audio, "timeline": timeline, "events": event_rows, "reactions": reaction_rows,
            "issues": issues, "content_acceptance": "unmeasured",
            "scope": "declared CFR sample-to-frame arithmetic; not ASR, PTS, lip sync or acting validation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        raw = Path(args.input).read_bytes()
        report = build(json.loads(raw.decode("utf-8-sig")))
        report["spec_sha256"] = hashlib.sha256(raw).hexdigest()
        with Path(args.output).open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps({"status": report["status"], "issues": report["issues"]}, ensure_ascii=False))
        return 1 if report["issues"] else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
