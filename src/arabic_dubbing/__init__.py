"""Core building blocks for the educational EN→AR dubbing research project.

No model inference, network request, or Colab startup occurs on import.
"""
from .data import Segment, Word, TranslatedSegment, SeparatedAudio, RunResult
from .pipeline import DubbingPipeline, PipelinePorts

__all__ = [
    "Segment", "Word", "TranslatedSegment", "SeparatedAudio", "RunResult",
    "DubbingPipeline", "PipelinePorts",
]
