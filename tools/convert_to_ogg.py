"""Convert every game/voice/*.wav to a small .ogg in game/voice_ogg (originals are NOT touched).
Needs ffmpeg. Safe to stop and re-run: finished files are skipped.

    py convert_to_ogg.py --dry-run     # count only
    py convert_to_ogg.py               # convert everything
    py convert_to_ogg.py --quality 3   # 0-10, higher = bigger and better (default 3)
"""
import argparse, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from breeze_common import DEFAULT_ROOT

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=DEFAULT_ROOT)
ap.add_argument("--quality", default="3")
ap.add_argument("--jobs", type=int, default=4, help="files converted at the same time")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

src = os.path.join(a.root, "game", "voice")
dst = os.path.join(a.root, "game", "voice_ogg")
if not os.path.isdir(src):
    sys.exit("Missing folder: " + src)
if not a.dry_run and not shutil.which("ffmpeg"):
    sys.exit("ffmpeg not found. Install it, then open a NEW Command Prompt and try again.")

names = [f for f in os.listdir(src) if f.lower().endswith(".wav")]
todo = [f for f in names if not os.path.exists(os.path.join(dst, f[:-4] + ".ogg"))]
size = sum(os.path.getsize(os.path.join(src, f)) for f in names) / 1e9
print("%d wav files (%.1f GB), %d still to convert" % (len(names), size, len(todo)))
if a.dry_run or not todo:
    sys.exit(0)
os.makedirs(dst, exist_ok=True)
failed, done, t0 = [], 0, time.time()

def conv(f):
    out = os.path.join(dst, f[:-4] + ".ogg")
    tmp = out + ".part.ogg"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(src, f),
                        "-ac", "1", "-c:a", "libvorbis", "-q:a", a.quality, tmp],
                       capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, out)
        return f, True
    return f, False

try:
    with ThreadPoolExecutor(a.jobs) as ex:
        for f, ok in ex.map(conv, todo):
            done += 1
            if not ok: failed.append(f)
            if done % 500 == 0:
                print("  %d / %d (%.0f s)" % (done, len(todo), time.time() - t0))
except KeyboardInterrupt:
    print("Stopped. Run again to continue.")
out_size = sum(os.path.getsize(os.path.join(dst, f)) for f in os.listdir(dst) if f.endswith(".ogg")) / 1e9
print("Done. ogg folder is now %.1f GB. Failed: %d" % (out_size, len(failed)))
for f in failed[:20]: print("  failed:", f)
