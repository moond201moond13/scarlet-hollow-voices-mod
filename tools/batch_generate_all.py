"""Batch voice generator for Scarlet Hollow: every character in cast_data.py.

Reads dialogue_dump.tsv, sends each line to the Breeze server with the character's
saved voice plus a delivery direction, and saves game/voice/<line id>.wav.

Safe to stop (Ctrl+C or closing the window) and run again: lines that already have a file
are skipped. Identical lines are generated once and copied to every line id that needs them.

    py batch_generate_all.py --dry-run                      # counts and estimates only
    py batch_generate_all.py --speakers narrator --limit 50
    py batch_generate_all.py                                # everything, biggest voices first
    py batch_generate_all.py --speakers stella,kaneeka      # chosen speakers (ids from the game)
"""
import argparse
import os
import re
import shutil
import time
import urllib.error
from collections import Counter

from breeze_common import (DEFAULT_ROOT, DEFAULT_SERVER, clean, load_rows, post, safe,
                           saved_voice_names, speakable, write_wav)
from cast_data import CAST, NOT_YET

NAME_TOKEN = "[player_name]"
PLACEHOLDER_SPEAKERS = {"speaker", "unknown", "extend"}   # real speaker comes from speaker_overrides.tsv
CHARS_PER_AUDIO_SECOND = 14.0    # rough speech rate, only used for estimates
ASSUMED_SPEED = 1.4              # rough real-time factor, only used for estimates
EMOTION_CFG = "2"                # guidance for lines with a delivery direction (1 = off)


# ------------------------------------------------------ player name handling --
def drop_vocatives(t):
    """Remove the player's name when it is only a form of address ("Good night, [player_name].").
    The player types the name, so it can't be spoken; the sentence reads naturally without it."""
    if NAME_TOKEN not in t:
        return t
    # at the start of the text or of a sentence:  "[player_name], stop"  /  "[player_name]? What..."
    t = re.sub(r"(^|(?<=[.!?\u2026] ))\[player_name\][,?!.]+\s*(\w)",
               lambda m: m.group(1) + m.group(2).upper(), t)
    # after a comma:  "Good night, [player_name]."  /  "Stay safe, [player_name], and ..."
    t = re.sub(r",\s*\[player_name\](?=[,.!?\u2026:;]|\s*$)", "", t)
    return t


# ------------------------------------------------------- delivery direction --
# Each returns (instruction, strong). strong=True means "use guidance" (slower, but the
# direction actually steers the voice); False means plain delivery at cfg 1.
def narrator_mod(t):
    if "!" in t:
        return "Tense and urgent, but still low and controlled.", True
    if "..." in t:
        return "Uneasy, slow, trailing off.", True
    return "Calm, deadpan, low and unhurried narration.", False


def tabitha_mod(t):
    low = t.lower()
    if "thank god" in low:
        return "Relieved and shaky, with an edge of anger.", True
    if "..." in t and "!" in t:
        return "Strained and desperate, voice cracking, close to breaking.", True
    if "?!" in t or t.count("!") >= 2:
        return "Furious and exasperated, voice raised, sharp and forceful.", True
    if "!" in t:
        return "Heated and forceful, sharp.", True
    if re.match(r"^(ugh|tch|ha\. ha)", low):
        return "Exasperated and sarcastic, as if rolling her eyes.", True
    if "..." in t or "\u2014" in t:
        return "Hesitant and uncertain, trailing off, a little shaky.", True
    if re.search(r"\b(sorry|please|thank|thanks)\b", low):
        return "Soft and sincere, a little vulnerable.", True
    if "?" in t:
        return "Pointed and questioning, dry.", True
    return "Natural and conversational, guarded but real.", False


def generic_mod(t):
    low = t.lower()
    if "?!" in t or t.count("!") >= 2:
        return "Shouting, voice raised, intense.", True
    if "!" in t:
        return "Emphatic and energetic, voice raised.", True
    if "..." in t or "\u2014" in t:
        return "Hesitant, trailing off.", True
    if re.search(r"\b(sorry|please|thank|thanks)\b", low):
        return "Sincere and softer.", True
    return "", False


MODS = {"narrator": narrator_mod, "tabitha": tabitha_mod}


def direction(voice, style, text):
    """-> (instruction, cfg_scale string)"""
    mod, strong = MODS.get(voice, generic_mod)(text)
    if style:
        # a character-specific style always applies, and needs guidance to take effect
        instruction = (style + " " + mod).strip() if strong else style
        return instruction, EMOTION_CFG
    return mod, (EMOTION_CFG if strong else "1")


# ------------------------------------------------------------------- jobs --
def build_jobs(rows, speaker_ids, overrides):
    jobs, order = {}, []
    skipped = Counter()
    for ident, speaker, raw in rows:
        if speaker in PLACEHOLDER_SPEAKERS:
            speaker = overrides.get(ident)          # None = no known speaker
            if speaker is None:
                continue
        if speaker not in speaker_ids:
            continue
        if speaker not in CAST:
            skipped["no voice for " + speaker] += 1
            continue
        voice, style = CAST[speaker]
        text = drop_vocatives(speakable(raw))
        if "[" in text:
            skipped["variable"] += 1
            continue
        if len(re.findall(r"\w", text)) < 2:
            skipped["empty"] += 1
            continue
        instruction, cfg = direction(voice, style, text)
        key = (voice, text, instruction, cfg)
        if key not in jobs:
            jobs[key] = {"voice": voice, "text": text, "instruction": instruction,
                         "cfg": cfg, "ids": []}
            order.append(key)
        jobs[key]["ids"].append(ident)
    return [jobs[k] for k in order], skipped


def fmt_hours(seconds):
    return "%.1f hours" % (seconds / 3600.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--server", default=DEFAULT_SERVER)
    ap.add_argument("--speakers", default="all",
                    help='"all", or a comma list of speaker ids (narrator = narration)')
    ap.add_argument("--limit", type=int, default=0, help="stop after N new clips")
    ap.add_argument("--from-log", action="store_true",
                    help="only voice the lines you played (from shown_lines.txt)")
    ap.add_argument("--from-report", action="store_true",
                    help="only voice the lines listed in silent_report.tsv (from check_silent.py)")
    ap.add_argument("--dry-run", action="store_true", help="count and estimate only")
    args = ap.parse_args()

    dump = os.path.join(args.root, "dialogue_dump.tsv")
    out_dir = os.path.join(args.root, "game", "voice")
    if not os.path.exists(dump):
        print("Missing file:", dump)
        return
    rows = load_rows(dump)
    overrides = {}
    ov_path = os.path.join(args.root, "speaker_overrides.tsv")
    if os.path.exists(ov_path):
        with open(ov_path, encoding="utf-8") as f:
            next(f)
            for line in f:
                parts = line.rstrip("\r\n").split("\t")
                if len(parts) >= 2:
                    overrides[parts[0]] = parts[1]
        print("Loaded %d speaker overrides." % len(overrides))
    else:
        print("No speaker_overrides.tsv found in", args.root, "- speaker/unknown/extend lines will be skipped.")
    if args.from_report:
        rp = os.path.join(args.root, "silent_report.tsv")
        if not os.path.exists(rp):
            print("Missing file:", rp, "- run check_silent.py first")
            return
        with open(rp, encoding="utf-8") as f:
            next(f)
            want = {l.split("\t")[0] for l in f if l.strip()}
        rows = [r for r in rows if r[0] in want]
        print("Lines from silent_report.tsv: %d" % len(rows))
    if args.from_log:
        log_path = os.path.join(args.root, "shown_lines.txt")
        if not os.path.exists(log_path):
            print("Missing file:", log_path)
            return
        ids, texts = set(), set()
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\r\n").split("\t", 1)
                if parts[0].strip():
                    ids.add(parts[0].strip())
                if len(parts) > 1 and parts[1].strip():
                    texts.add(clean(parts[1]))
        rows = [r for r in rows if r[0] in ids or clean(r[2]) in texts]
        print("Lines matched from your play log: %d" % len(rows))
    counts = Counter((overrides.get(i) if spk in PLACEHOLDER_SPEAKERS else spk)
                     for i, spk, _t in rows)
    counts.pop(None, None)

    unassigned = {s: n for s, n in counts.items() if s not in CAST and s not in NOT_YET}
    if unassigned:
        print("Speakers with no voice assigned yet (skipped):")
        for s, n in sorted(unassigned.items(), key=lambda x: -x[1]):
            print("   %-20s %d lines" % (s, n))

    if args.speakers == "all":
        chosen = [s for s in CAST if s in counts]
        # narration first, then Tabitha, then the rest by number of lines
        chosen.sort(key=lambda s: (s != "", s != "tabitha", -counts[s]))
    else:
        chosen = []
        for name in (n.strip() for n in args.speakers.split(",") if n.strip()):
            sid = "" if name == "narrator" else name
            if sid in CAST:
                chosen.append(sid)
            else:
                print("Unknown speaker:", name)
                return

    # build jobs speaker by speaker so the run order follows `chosen`
    work, total_skipped = [], Counter()
    per_voice = Counter()
    seen_keys = {}
    for sid in chosen:
        jobs, skipped = build_jobs(rows, {sid}, overrides)
        total_skipped.update(skipped)
        for j in jobs:
            key = (j["voice"], j["text"], j["instruction"], j["cfg"])
            if key in seen_keys:
                # same clip already queued under another speaker id (e.g. ukaneeka vs kaneeka):
                # add these line ids to it so they get a copy too
                seen_keys[key]["ids"].extend(j["ids"])
                continue
            seen_keys[key] = j
            work.append(j)
            per_voice[j["voice"]] += len(j["text"])
    chars = sum(len(j["text"]) for j in work)
    ids = sum(len(j["ids"]) for j in work)
    audio = chars / CHARS_PER_AUDIO_SECOND
    print("\n%d line ids -> %d unique clips, %d characters" % (ids, len(work), chars))
    print("skipped: %d lines with [variables], %d empty" %
          (total_skipped["variable"], total_skipped["empty"]))
    print("estimate: about %s of audio, %s to generate at about %.1fx, about %.0f GB as wav files"
          % (fmt_hours(audio), fmt_hours(audio / ASSUMED_SPEED), ASSUMED_SPEED,
             audio * 48000 / 1e9))
    if args.dry_run:
        print("\nDry run only. Nothing was generated.")
        return

    existing = saved_voice_names(args.server)
    if existing is None:
        print("\nCould not read the voice list from the server. Is it running at", args.server, "?")
        return
    needed = {j["voice"] for j in work}
    missing = sorted(needed - existing)
    if missing:
        print("\nThese voices are not on the server yet, so their lines will be skipped:")
        print("   " + ", ".join(missing))
        print("Run  py cast_voices.py  first, then run this again.")
        work = [j for j in work if j["voice"] in existing]

    os.makedirs(out_dir, exist_ok=True)
    fail_path = os.path.join(args.root, "batch_failures.tsv")
    todo, remaining_chars = [], 0
    for job in work:                      # resume: reuse files that already exist
        paths = [os.path.join(out_dir, i + ".wav") for i in job["ids"]]
        have = [p for p in paths if os.path.exists(p)]
        if have:
            for p in paths:
                if not os.path.exists(p):
                    shutil.copyfile(have[0], p)
            continue
        todo.append((job, paths))
        remaining_chars += len(job["text"])
    print("\nClips still to generate: %d (%d characters)" % (len(todo), remaining_chars))
    if not todo:
        print("Everything for these speakers already exists.")
        return

    done, audio_total, time_total, chars_done = 0, 0.0, 0.0, 0
    try:
        for job, paths in todo:
            if args.limit and done >= args.limit:
                break
            start = time.time()
            fields = [("text", job["text"]), ("voice_id", job["voice"]), ("cfg_scale", job["cfg"])]
            if job["instruction"]:
                fields.append(("instruction", job["instruction"]))
            data = None
            for _attempt in range(8):
                try:
                    data = post(args.server + "/v1/audio/speech", fields)
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 409:     # server busy: wait and retry
                        time.sleep(2)
                        continue
                    print("Server error %s for %s: %s" % (e.code, job["ids"][0], safe(e.read()[:150])))
                    with open(fail_path, "a", encoding="utf-8") as f:
                        f.write("%s\t%s\t%s\n" % (job["ids"][0], e.code, job["text"]))
                    break
                except Exception as e:
                    print("\nCould not reach the server (%s). Is it still running?" % e)
                    print("Start it again and re-run this script; it will resume.")
                    return
            if data is None:
                continue
            secs = write_wav(paths[0], data)
            for p in paths[1:]:
                shutil.copyfile(paths[0], p)
            took = time.time() - start
            done += 1
            audio_total += secs
            time_total += took
            chars_done += len(job["text"])
            print("%-40s %-9s %4.1fs in %4.1fs  %s"
                  % (job["ids"][0][:40], job["voice"][:9], secs, took, safe(job["text"][:36])))
            if done % 25 == 0 and chars_done:
                left = remaining_chars - chars_done
                eta = time_total / chars_done * left
                print("--- %d done | %.2fx real time | about %s left ---"
                      % (done, audio_total / time_total, fmt_hours(eta)))
    except KeyboardInterrupt:
        print("\nStopped. Run the same command again to continue.")
    if done:
        print("\nThis run: %d clips, %.0fs of audio in %.0fs = %.2fx real time"
              % (done, audio_total, time_total, audio_total / time_total))


if __name__ == "__main__":
    main()
