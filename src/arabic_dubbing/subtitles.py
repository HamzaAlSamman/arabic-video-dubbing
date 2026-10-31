"""Pure SRT export; never mutates the original WhisperX word alignment."""
from typing import Sequence
from .data import TranslatedSegment


def _stamp(milliseconds: int) -> str:
    if isinstance(milliseconds, bool) or not isinstance(milliseconds, int) or milliseconds < 0:
        raise ValueError("SRT timestamp must be non-negative integer milliseconds")
    seconds, ms = divmod(milliseconds, 1000)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    return f"{hours:02d}:{minute:02d}:{sec:02d},{ms:03d}"


def to_srt(lines: Sequence[TranslatedSegment]) -> str:
    blocks = []
    for i, line in enumerate(lines, start=1):
        blocks.append(
            f"{i}\n{_stamp(line.start_ms)} --> {_stamp(line.end_ms)}\n"
            f"{line.text_ar.strip()}\n"
        )
    return "\n".join(blocks) + ("\n" if blocks else "")
