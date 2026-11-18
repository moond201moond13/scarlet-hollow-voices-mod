"""Create a saved voice for every character in cast_data.py.

For each voice it (1) designs a voice from the written description, speaking one of
that character's calm lines, (2) saves an audition clip to cast_samples\\<voice>.wav,
and (3) saves the voice on the server so batch_generate.py can use it.

Voices that already exist on the server are skipped (so narrator and tabitha are safe).

    py cast_voices.py --dry-run               # show the plan only
    py cast_voices.py                         # make every missing voice
    py cast_voices.py --only stella,kaneeka   # just these
    py cast_voices.py --redo stella --seed 7  # remake one with a different seed
    py cast_voices.py --redo stella --desc "A woman in her thirties, ..."  # new description
    py cast_voices.py --audition kaneeka --count 5   # 5 sample clips with different seeds, saves nothing
"""
import argparse
import os
import re
import sys
import time
import urllib.error

from breeze_common import (DEFAULT_ROOT, DEFAULT_SERVER, load_rows, post, safe,
                           saved_voice_names, speakable, write_wav)
from cast_data import GENERIC_REF, VOICE_DEFS

DESIGN_CFG = "4"          # the official docs recommend 4 for voice design


def pick_ref_line(rows, speaker):
    """A calm, medium-length line by this speaker: becomes the sample and its transcript."""
    if speaker:
        best = []
        for _ident, spk, raw in rows:
            if spk != speaker:
                continue
            t = speakable(raw)
            if not (55 <= len(t) <= 110):
                continue
            if any(c in t for c in "[!?\u2014") or "..." in t or '"' in t:
                continue
            if not t.endswith("."):
                continue
            best.append(t)
            if len(best) >= 5:
                break
        if best:
            return best[min(2, len(best) - 1)]
    return GENERIC_REF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--only", default="", help="comma list of voice names")
    ap.add_argument("--redo", default="", help="comma list of voices to remake")
    ap.add_argument("--seed", type=int, default=0, help="seed override (with --only/--redo)")
    ap.add_argument("--desc", default="", help="description override (with one voice)")
    ap.add_argument("--audition", default="", help="make sample clips for one voice, save nothing")
    ap.add_argument("--count", type=int, default=5, help="number of seeds for --audition")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dump = os.path.join(args.root, "dialogue_dump.tsv")
    if not os.path.exists(dump):
        print("Missing file:", dump)
        return
    rows = load_rows(dump)
    sample_dir = os.path.join(args.root, "cast_samples")

    if args.audition:
        name = args.audition.strip()
        if name not in VOICE_DEFS:
            print("Unknown voice name:", name)
            print("Valid names:", ", ".join(VOICE_DEFS))
            return
        desc, ref_from = VOICE_DEFS[name]
        if args.desc:
            desc = args.desc
        text = pick_ref_line(rows, ref_from)
        os.makedirs(sample_dir, exist_ok=True)
        print("Auditioning %s with %d seeds. Text: %s" % (name, args.count, safe(text)))
        for seed in range(1, args.count + 1):
            data = None
            for _attempt in range(8):
                try:
                    data = post(args.server + "/v1/audio/speech",
                                [("text", text), ("instruction", desc),
                                 ("cfg_scale", DESIGN_CFG), ("seed", str(seed))])
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 409:
                        time.sleep(2)
                        continue
                    print("failed: HTTP", e.code, safe(e.read()[:150]))
                    break
                except Exception as e:
                    print("Could not reach the server (%s). Is it running?" % e)
                    return
            if data is None:
                return
            path = os.path.join(sample_dir, "%s_seed%d.wav" % (name, seed))
            secs = write_wav(path, data)
            print("  seed %d -> %s (%.1fs)" % (seed, path, secs))
        print("\nListen, pick one, then run:  py cast_voices.py --redo %s --seed N" % name)
        return

    names = list(VOICE_DEFS)
    redo = {n.strip() for n in args.redo.split(",") if n.strip()}
    only = {n.strip() for n in args.only.split(",") if n.strip()} | redo
    unknown = [n for n in only if n not in VOICE_DEFS]
    if unknown:
        print("Unknown voice name(s):", unknown)
        print("Valid names:", ", ".join(names))
        return
    if only:
        names = [n for n in names if n in only]

    existing = saved_voice_names(args.server) if not args.dry_run else set()
    if existing is None:
        print("Could not read the voice list from the server. Is it running at", args.server, "?")
        return

    plan = []
    for name in names:
        if name in existing and name not in redo:
            continue
        desc, ref_from = VOICE_DEFS[name]
        if args.desc and len(names) == 1:
            desc = args.desc
        seed = args.seed if (args.seed and only) else 100 + list(VOICE_DEFS).index(name)
        text = pick_ref_line(rows, ref_from)
        plan.append((name, desc, seed, text))

    print("Voices to make: %d (already on the server: %d)" % (len(plan), len(existing or [])))
    if args.dry_run:
        for name, desc, seed, text in plan:
            print("  %-14s seed %-4d %s" % (name, seed, safe(text[:70])))
        print("\nDry run only. Nothing was made.")
        return
    if not plan:
        print("Nothing to do.")
        return

    os.makedirs(sample_dir, exist_ok=True)
    made, failed = 0, []
    t0 = time.time()
    try:
        for i, (name, desc, seed, text) in enumerate(plan, 1):
            start = time.time()
            print("[%d/%d] %-14s " % (i, len(plan), name), end="", flush=True)
            data = None
            for _attempt in range(8):
                try:
                    data = post(args.server + "/v1/audio/speech",
                                [("text", text), ("instruction", desc),
                                 ("cfg_scale", DESIGN_CFG), ("seed", str(seed))])
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 409:
                        time.sleep(2)
                        continue
                    print("design failed: HTTP", e.code, safe(e.read()[:150]))
                    break
                except Exception as e:
                    print("\nCould not reach the server (%s). Is it still running?" % e)
                    return
            if data is None:
                failed.append(name)
                continue
            wav_path = os.path.join(sample_dir, name + ".wav")
            secs = write_wav(wav_path, data)
            with open(wav_path, "rb") as f:
                wav_bytes = f.read()
            try:
                post(args.server + "/v1/voices",
                     [("ref_text", text), ("name", name), ("description", desc)],
                     [("ref_audio", name + ".wav", wav_bytes)])
            except urllib.error.HTTPError as e:
                print("save failed: HTTP", e.code, safe(e.read()[:150]))
                failed.append(name)
                continue
            made += 1
            print("ok  %.1fs sample, %.0fs to make  | %s" % (secs, time.time() - start, safe(text[:45])))
    except KeyboardInterrupt:
        print("\nStopped. Run the same command again to continue.")

    print("\nMade %d voices in %.0f minutes." % (made, (time.time() - t0) / 60))
    if failed:
        print("Failed:", ", ".join(failed), "(re-run to retry)")
    print("Audition clips are in:", sample_dir)


if __name__ == "__main__":
    main()
