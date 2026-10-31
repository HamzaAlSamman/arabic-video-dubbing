"""Immutable records: preserve source segment IDs and word-level timestamps."""
from dataclasses import dataclass
from pathlib import Path


def _interval(start_ms: int, end_ms: int) -> None:
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (start_ms, end_ms)):
        raise TypeError("timestamps must be integer milliseconds")
    if start_ms < 0 or end_ms <= start_ms:
        raise ValueError("timestamps must satisfy 0 <= start_ms < end_ms")


@dataclass(frozen=True)
class Word:
    text: str
    start_ms: int
    end_ms: int

    def __post_init__(self) -> None:
        _interval(self.start_ms, self.end_ms)
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("word text must be non-empty")


@dataclass(frozen=True)
class Segment:
    segment_id: str
    text: str
    start_ms: int
    end_ms: int
    words: tuple[Word, ...] = ()

    def __post_init__(self) -> None:
        _interval(self.start_ms, self.end_ms)
        if not isinstance(self.segment_id, str) or not self.segment_id.strip():
            raise ValueError("segment_id is required")
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("segment text must be non-empty")
        if not isinstance(self.words, tuple) or any(not isinstance(w, Word) for w in self.words):
            raise TypeError("words must be a tuple of Word records")
        for word in self.words:
            if word.start_ms < self.start_ms or word.end_ms > self.end_ms:
                raise ValueError("word timing must be within its source segment")


@dataclass(frozen=True)
class TranslatedSegment:
    """A translated line anchored to the unchanged source ID and time slot."""
    source_segment_id: str
    text_ar: str
    start_ms: int
    end_ms: int

    def __post_init__(self) -> None:
        _interval(self.start_ms, self.end_ms)
        if not isinstance(self.source_segment_id, str) or not self.source_segment_id.strip():
            raise ValueError("source_segment_id is required")
        if not isinstance(self.text_ar, str) or not self.text_ar.strip():
            raise ValueError("Arabic text must be non-empty")


@dataclass(frozen=True)
class SeparatedAudio:
    speech: Path
    background: Path


@dataclass(frozen=True)
class RunResult:
    run_id: str
    final_video: Path
    manifest: Path
    source_segments: tuple[Segment, ...]
    translated_segments: tuple[TranslatedSegment, ...]
