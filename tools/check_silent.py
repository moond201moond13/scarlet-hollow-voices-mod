"""List every line of the "???" speakers (and any other speaker you choose) that has NO voice file,
and say why. Reads only; changes nothing. Put it in E:\f next to batch_generate_all.py.

    py check_silent.py                 # ??? speakers only
    py check_silent.py --all           # every speaker
Writes silent_report.tsv (id, speaker, reason, text) into ScarletHollow_mod.
"""
import argparse, os, re
from collections import Counter
from breeze_common import DEFAULT_ROOT, load_rows, speakable
from cast_data import CAST
from batch_generate_all import drop_vocatives, PLACEHOLDER_SPEAKERS

QQQ = {"unknown", "wayne_unknown", "eldritch_unknown"}
def is_qqq(s):
    return s in QQQ or (s.startswith("u") and s in CAST and s[1:] in CAST)

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=DEFAULT_ROOT)
ap.add_argument("--all", action="store_true")
a = ap.parse_args()

rows = load_rows(os.path.join(a.root, "dialogue_dump.tsv"))
ov = {}
p = os.path.join(a.root, "speaker_overrides.tsv")
if os.path.exists(p):
    with open(p, encoding="utf-8") as f:
        next(f)
        for l in f:
            q = l.rstrip("\r\n").split("\t")
            if len(q) >= 2: ov[q[0]] = q[1]
voice_dir = os.path.join(a.root, "game", "voice")
have = {f[:-4] for f in os.listdir(voice_dir)} if os.path.isdir(voice_dir) else set()

out, why = [], Counter()
for ident, spk, raw in rows:
    if not (a.all or is_qqq(spk)):
        continue
    if spk in ("p",):
        continue
    real = ov.get(ident) if spk in PLACEHOLDER_SPEAKERS else spk
    text = drop_vocatives(speakable(raw))
    if real is None:                 reason = "no speaker known (needs an override)"
    elif real not in CAST:           reason = "no voice for " + real
    elif "[" in text:                reason = "still has a [variable]"
    elif len(re.findall(r"\w", text)) < 2: continue   # empty/extend, nothing to say
    elif ident in have:              continue
    else:                            reason = "not generated yet (or failed)"
    why[reason] += 1
    out.append((ident, spk, reason, text))

rp = os.path.join(a.root, "silent_report.tsv")
with open(rp, "w", encoding="utf-8") as f:
    f.write("id\tspeaker\treason\ttext\n")
    for r in out: f.write("\t".join(r) + "\n")
print("Silent lines:", len(out))
for k, v in why.most_common(): print("  %5d  %s" % (v, k))
print("Details in", rp)
