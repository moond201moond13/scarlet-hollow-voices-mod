"""Upload the voice_shards folder to your Hugging Face dataset, one file at a time.
Resumes: files already on Hugging Face are skipped, so if it stops just run it again.
Needs:   py -3.13 -m pip install huggingface_hub

    set HF_TOKEN=your_new_write_token      (same Command Prompt window)
    py -3.13 upload_to_hf.py
"""
import getpass, os, sys, time
from huggingface_hub import HfApi

REPO = "moond13/scarlet-hollow-voices"
FOLDER = r"E:\tmp gam\ScarletHollow_mod\voice_shards"

if not os.path.isdir(FOLDER):
    sys.exit("Folder not found: " + FOLDER + "  (run make_shards.py first)")
if any(f.endswith(".part") for f in os.listdir(FOLDER)):
    sys.exit("make_shards.py has not finished (a .part file is still in the folder). Let it print Done first.")
token = os.environ.get("HF_TOKEN") or getpass.getpass("Hugging Face write token: ").strip()
api = HfApi(token=token)
print("Logged in as:", api.whoami()["name"])
api.create_repo(REPO, repo_type="dataset", exist_ok=True)

on_hub = set(api.list_repo_files(REPO, repo_type="dataset"))
names = sorted(os.listdir(FOLDER))
todo = [n for n in names if n not in on_hub]
print("%d files in folder, %d still to upload" % (len(names), len(todo)))
failed = []
for i, n in enumerate(todo, 1):
    path = os.path.join(FOLDER, n)
    print("[%d/%d] %s (%.2f GB) ..." % (i, len(todo), n, os.path.getsize(path) / 1e9), flush=True)
    t0 = time.time()
    try:
        api.upload_file(path_or_fileobj=path, path_in_repo=n, repo_id=REPO, repo_type="dataset",
                        commit_message="add " + n)
        print("   done in %.0f s" % (time.time() - t0))
    except Exception as e:
        print("   FAILED:", e)
        failed.append(n)
if failed:
    print("Failed:", ", ".join(failed), "- run again to retry.")
else:
    print("All uploaded: https://huggingface.co/datasets/" + REPO)
