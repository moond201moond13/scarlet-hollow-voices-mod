"""Pack game/voice/*.wav into a few big zip files ("shards") for upload to Hugging Face.
Hugging Face allows under 10,000 files per folder, and you have about 50,000 wavs, so
they must be packed. Originals are NOT touched. Safe to stop and re-run (finished shards are skipped).

    py make_shards.py --dry-run
    py make_shards.py                 # writes ScarletHollow_mod\\voice_shards\\voices_001.zip ... + manifest.json
    py make_shards.py --store         # no compression, much faster
    py make_shards.py --shard-gb 1    # shard size in GB (default 1.0)
Run it only after batch_generate_all.py has finished, so the file list does not change.
"""
import argparse, json, os, sys, zipfile
from breeze_common import DEFAULT_ROOT

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=DEFAULT_ROOT)
ap.add_argument("--shard-gb", type=float, default=1.0)
ap.add_argument("--store", action="store_true", help="no compression: much faster, slightly bigger zips")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

src = os.path.join(a.root, "game", "voice")
dst = os.path.join(a.root, "voice_shards")
if not os.path.isdir(src):
    sys.exit("Missing folder: " + src)
files = sorted(f for f in os.listdir(src) if f.lower().endswith(".wav"))
limit = int(a.shard_gb * 1e9)

shards, cur, cur_bytes = [], [], 0
for f in files:
    sz = os.path.getsize(os.path.join(src, f))
    if cur and cur_bytes + sz > limit:
        shards.append(cur); cur, cur_bytes = [], 0
    cur.append(f); cur_bytes += sz
if cur:
    shards.append(cur)
total = sum(os.path.getsize(os.path.join(src, f)) for f in files) / 1e9
print("%d wav files, %.1f GB -> %d shards" % (len(files), total, len(shards)))
if a.dry_run:
    sys.exit(0)

os.makedirs(dst, exist_ok=True)
manifest = []
for i, names in enumerate(shards, 1):
    zname = "voices_%03d.zip" % i
    zpath = os.path.join(dst, zname)
    if os.path.exists(zpath):
        print("  %s exists, skipped" % zname)
    else:
        tmp = zpath + ".part"
        mode = zipfile.ZIP_STORED if a.store else zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(tmp, "w", mode, **({} if a.store else {"compresslevel": 1})) as z:
            for n in names:
                z.write(os.path.join(src, n), n)
        os.replace(tmp, zpath)
        print("  wrote %s (%d files, %.2f GB)" % (zname, len(names), os.path.getsize(zpath) / 1e9))
    manifest.append({"name": zname, "files": len(names), "bytes": os.path.getsize(zpath)})
with open(os.path.join(dst, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump({"shards": manifest, "totalFiles": len(files)}, f, indent=1)
print("Done. Upload the folder:", dst)
