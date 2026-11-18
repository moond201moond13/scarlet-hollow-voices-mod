"""Shared helpers for cast_voices.py and batch_generate.py.
Keep this file in the same folder as those two scripts."""
import json
import os
import re
import uuid
import wave
import urllib.request

SAMPLE_RATE = 24000
DEFAULT_ROOT = r"E:\tmp gam\ScarletHollow_mod"   # folder that contains ScarletHollow.exe
DEFAULT_SERVER = "http://127.0.0.1:8080"

TAG_RE = re.compile(r"\{[^}]*\}")
LABEL_RE = re.compile(r"^\((?:[A-Z][A-Za-z']*)(?: [A-Z][A-Za-z']*)*\)\s*")


def safe(s):
    """Make text printable in any Windows console."""
    return str(s).encode("ascii", "replace").decode("ascii")


def clean(text):
    text = TAG_RE.sub("", text or "")
    for ch in ("\t", "\r", "\n"):
        text = text.replace(ch, " ")
    return text.strip()


def speakable(text):
    """Game text -> what should actually be spoken."""
    t = clean(text)
    if t.startswith("''"):
        t = t[2:]
    if t.endswith("''"):
        t = t[:-2]
    return LABEL_RE.sub("", t.strip()).strip()


def load_rows(path):
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) < 3:
                continue
            rows.append((parts[0], parts[1], "\t".join(parts[2:])))
    return rows


def multipart(fields, files=None):
    """fields: list of (name, value). files: list of (name, filename, bytes)."""
    boundary = "----breeze" + uuid.uuid4().hex
    chunks = []
    for name, value in fields:
        chunks.append(
            ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
             % (boundary, name, value)).encode("utf-8"))
    for name, filename, content in (files or []):
        chunks.append(
            ('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\n'
             'Content-Type: audio/wav\r\n\r\n' % (boundary, name, filename)).encode("utf-8"))
        chunks.append(content)
        chunks.append(b"\r\n")
    chunks.append(("--%s--\r\n" % boundary).encode("ascii"))
    return b"".join(chunks), "multipart/form-data; boundary=" + boundary


def post(url, fields, files=None, timeout=900):
    body, ctype = multipart(fields, files)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def get_json(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def saved_voice_names(server):
    """Names of the voices the server knows. Returns None if it can't be read."""
    try:
        data = get_json(server + "/v1/voices")
        if isinstance(data, dict):
            data = data.get("voices", [])
        return {v.get("id") for v in data}
    except Exception:
        return None


def write_wav(path, data):
    """Write server audio (raw 24 kHz mono 16-bit, or a wav) to path. Returns seconds."""
    tmp = path + ".part"
    if data[:4] == b"RIFF":
        with open(tmp, "wb") as f:
            f.write(data)
    else:
        with wave.open(tmp, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(data)
    with wave.open(tmp, "rb") as w:
        secs = w.getnframes() / float(w.getframerate())
    os.replace(tmp, path)
    return secs
