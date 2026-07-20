"""Losslessly shrink the .m4a clips in audio/ by removing dead header bytes.

afconvert pads every file it writes with a `free` atom so the media data starts
on a 4096-byte boundary. That padding is ~2.8 KB, which on a 1-second TTS clip
is a quarter of the file and is pure dead weight over the wire.

This is not a re-encode: the audio bitstream (`mdat`) is copied through byte for
byte, so there is no generation loss and no format change. Only the container
shrinks. The one thing that must be fixed up is `stco`, the table of absolute
file offsets to each audio chunk — removing bytes ahead of `mdat` slides every
chunk earlier, so each offset is decremented by exactly the number of bytes
removed before it.

Idempotent: a file with nothing left to strip is left untouched.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.abspath(os.path.join(HERE, "..", "audio"))

# `free`/`skip` are pure padding, defined by the spec as ignorable.
#
# `udta` is NOT in this set, though it looks like a tempting 250 bytes: it holds
# the iTunSMPB tag describing the encoder's priming delay. Dropping it makes
# decoders replay those priming samples instead of discarding them, which shifts
# every sample and lengthens the clip by ~23 ms. Verified by decoding to PCM
# before and after — the buffers stop matching. Padding only.
DROP = {b"free", b"skip"}


def parse(data, start, end):
    """Yield (type, offset, size) for each atom in [start, end)."""
    off = start
    while off + 8 <= end:
        size = struct.unpack(">I", data[off:off + 4])[0]
        typ = data[off + 4:off + 8]
        if size == 0:            # extends to end of file
            size = end - off
        if size < 8 or off + size > end:
            raise ValueError(f"bad atom {typ!r} size {size} at {off}")
        yield typ, off, size
        off += size


def rewrite_moov(moov):
    """Return moov with DROP children removed, and the number of bytes dropped."""
    out = bytearray(moov[:8])
    dropped = 0
    for typ, off, size in parse(moov, 8, len(moov)):
        if typ in DROP:
            dropped += size
            continue
        out += moov[off:off + size]
    struct.pack_into(">I", out, 0, len(out))
    return bytes(out), dropped


def patch_stco(moov, delta):
    """Subtract delta from every absolute chunk offset in every stco/co64 table."""
    buf = bytearray(moov)
    i = 0
    while True:
        i = buf.find(b"stco", i)
        if i == -1:
            break
        base = i + 4 + 4                      # version/flags, then entry count
        count = struct.unpack(">I", buf[base:base + 4])[0]
        pos = base + 4
        for _ in range(count):
            old = struct.unpack(">I", buf[pos:pos + 4])[0]
            struct.pack_into(">I", buf, pos, old - delta)
            pos += 4
        i += 4
    i = 0
    while True:
        i = buf.find(b"co64", i)
        if i == -1:
            break
        base = i + 4 + 4
        count = struct.unpack(">I", buf[base:base + 4])[0]
        pos = base + 4
        for _ in range(count):
            old = struct.unpack(">Q", buf[pos:pos + 8])[0]
            struct.pack_into(">Q", buf, pos, old - delta)
            pos += 8
        i += 4
    return bytes(buf)


def strip(path):
    """Rewrite one file in place. Returns bytes saved (0 if nothing to do)."""
    data = open(path, "rb").read()
    top = list(parse(data, 0, len(data)))
    if not any(t == b"mdat" for t, _, _ in top):
        return 0

    kept = []          # (type, bytes) in original order
    removed_before_mdat = 0
    seen_mdat = False
    for typ, off, size in top:
        chunk = data[off:off + size]
        if typ == b"mdat":
            seen_mdat = True
        if typ in DROP:
            if not seen_mdat:
                removed_before_mdat += size
            continue
        if typ == b"moov":
            chunk, inner = rewrite_moov(chunk)
            if not seen_mdat:
                removed_before_mdat += inner
        kept.append((typ, chunk))

    if removed_before_mdat == 0:
        return 0                                    # already stripped

    kept = [(t, patch_stco(c, removed_before_mdat) if t == b"moov" else c) for t, c in kept]
    out = b"".join(c for _, c in kept)
    if len(out) != len(data) - removed_before_mdat:
        raise ValueError(f"{path}: size bookkeeping mismatch")
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(out)
    os.replace(tmp, path)
    return len(data) - len(out)


def main():
    files = sorted(f for f in os.listdir(AUDIO) if f.endswith(".m4a"))
    before = sum(os.path.getsize(os.path.join(AUDIO, f)) for f in files)
    saved = touched = 0
    for name in files:
        try:
            s = strip(os.path.join(AUDIO, name))
        except Exception as e:
            print(f"  ! {name}: {e}, left untouched")
            continue
        saved += s
        touched += bool(s)
    after = sum(os.path.getsize(os.path.join(AUDIO, f)) for f in files)
    print(f"{touched}/{len(files)} files stripped")
    print(f"audio/: {before/1024/1024:.1f} MB -> {after/1024/1024:.1f} MB "
          f"(saved {saved/1024/1024:.1f} MB, {saved/before*100:.0f}%)")


if __name__ == "__main__":
    main()
