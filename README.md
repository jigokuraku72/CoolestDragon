# The Dragon and the Red Sun

A Japanese ukiyo-e woodblock print for make.fun `coolest-art-01`.

A giant dark dragon rises from towering stylized waves before a massive
red sun, with snow-capped Mount Fuji and a red torii gate on the right,
and a lone boatman in a small wooden boat below — small against the
storm, staring up at the beast. The image was scaled down from the
original 1254x1254 with no cropping: the whole scene is preserved.

## How it works

`main.py` (Python 3, stdlib only, no network) copies `entry.png` to the
output directory and verifies it: JPEG magic bytes, 1 MiB size limit,
1024x1024 dimensions, and a sha256 match against the source.

The output directory is `$MAKEFUN_OUTPUT_DIR` when set, falling back to
`/output` (the grader's Docker container does not set the variable).

## Files

- `entry.png` — the art (1024x1024 JPEG, 510,376 bytes)
- `main.py` — the entry program
- `LICENSE` — MIT
