#!/usr/bin/env python3
"""coolest-art-01 entry: "The Dragon and the Red Sun".

Writes entry.png (a Japanese ukiyo-e woodblock print: a giant dark
dragon rising from stylized waves before a massive red sun, Mount Fuji
and a red torii gate, a lone boatman below) to the output directory.

Stdlib only, no network. The output directory is read from
$MAKEFUN_OUTPUT_DIR when set; the grader's Docker container does NOT
set it, so we fall back to the real writable mount at /output.
"""

import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

MAX_BYTES = 1_048_576  # 1 MiB
EXPECTED_SIZE = 510376
EXPECTED_SHA256 = (
    "a6c15072e6c14f3a00ff911e3e03e0fbec0835dc4f6cf2ad34752b8b94c1f5f5"
)
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def jpeg_dimensions(path):
    """Read width/height from a JPEG's SOF marker (stdlib only)."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2  # skip SOI (FF D8)
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = (data[i + 2] << 8) | data[i + 3]
        i += 2 + seg_len
    raise ValueError("no SOF marker found")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    with open(SRC, "rb") as f:
        magic = f.read(2)
    if magic != b"\xff\xd8":
        print("error: entry.png is not a JPEG (bad magic bytes)", file=sys.stderr)
        return 1

    src_size = os.path.getsize(SRC)
    if src_size > MAX_BYTES:
        print(f"error: entry.png is {src_size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    src_sha = sha256_of(SRC)
    if src_sha != EXPECTED_SHA256:
        print("error: entry.png sha256 mismatch", file=sys.stderr)
        return 1
    width, height = jpeg_dimensions(SRC)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"error: entry.png is {width}x{height}, expected "
              f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}", file=sys.stderr)
        return 1
    print(f"source verified: {src_size} bytes, JPEG magic OK, "
          f"dimensions {width}x{height}")

    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)

    dst_size = os.path.getsize(dst)
    dst_sha = sha256_of(dst)
    with open(dst, "rb") as f:
        dst_magic = f.read(2)
    if dst_magic != b"\xff\xd8":
        print("error: output entry.png is not a JPEG", file=sys.stderr)
        return 1
    if dst_size != src_size or dst_sha != src_sha:
        print("error: output does not match source", file=sys.stderr)
        return 1

    print(f"wrote {dst} ({dst_size} bytes, JPEG magic OK)")
    print(f"sha256 source={src_sha}")
    print(f"sha256 output={dst_sha} (match)")
    print("verified: output is byte-identical to source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
