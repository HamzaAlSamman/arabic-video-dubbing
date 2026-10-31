"""Dependency-injected orchestration; model adapters are NOT implemented here.

The previous notebooks remain intact. A new adapter must be explicitly written
for each model/provider before this can become a functioning end-to-end runner.
"""
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Protocol, Sequence

from .data import RunResult, Segment, SeparatedAudio, TranslatedSegment


class MediaPort(Protocol):
    def extract_audio(self, video: Path, destination: Path) -> Path: ...
    def render(self, video: Path, dubbed_audio: Path, destination: Path) -> Path: ...


class SeparationPort(Protocol):
    def separate(self, audio: Path, output_dir: Path) -> SeparatedAudio: ...


class TranscriptionPort(Protocol):
    def transcribe(self, speech_audio: Path) -> Sequence[Segment]: ...


class TranslationPort(Protocol):
    def translate(self, segments: Sequence[Segment]) -> Sequence[TranslatedSegment]: ...


class SynthesisPort(Protocol):
    def synthesize(self, lines: Sequence[TranslatedSegment], destination: Path) -> Path: ...


class DurationPort(Protocol):
    def align(self, speech_audio: Path, lines: Sequence[TranslatedSegment], destination: Path) -> Path: ...


class LipSyncPort(Protocol):
    def sync(self, video: Path, speech_audio: Path, destination: Path) -> Path: ...


class MixingPort(Protocol):
    def mix(self, background_audio: Path, speech_audio: Path, destination: Path) -> Path: ...


@dataclass(frozen=True)
class PipelinePorts:
    media: MediaPort
    separation: SeparationPort
    transcription: TranscriptionPort
    translation: TranslationPort
    synthesis: SynthesisPort
    duration: DurationPort
    mixing: MixingPort
    lip_sync: LipSyncPort | None = None


def _must_exist(value: Path, stage: str) -> Path:
    path = Path(value)
    if not path.is_file():
        raise FileNotFoundError(f"{stage} did not produce an existing file: {path}")
    return path


def _verify_source(segments: tuple[Segment, ...]) -> None:
    if not segments:
        raise ValueError("ASR returned no speech segments")
    ids = [s.segment_id for s in segments]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate source segment IDs")


def _verify_translations(
    original: tuple[Segment, ...],
    translated: tuple[TranslatedSegment, ...],
) -> None:
    if len(original) != len(translated):
        raise ValueError("Translation changed the number of source segments")
    for source, target in zip(original, translated):
        if (source.segment_id != target.source_segment_id
                or source.start_ms != target.start_ms
                or source.end_ms != target.end_ms):
            raise ValueError("Translation changed an original ID, order, or time slot")


class DubbingPipeline:
    """Run inference stages 1,3–10. Model training is an OFFLINE activity.

    Calls real adapters only when run() is explicitly invoked; importing and
    constructing the pipeline do not launch any jobs or paid APIs.
    """

    def __init__(self, ports: PipelinePorts):
        self.ports = ports

    def run(self, video: Path, workspace: Path, run_id: str) -> RunResult:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", run_id):
            raise ValueError("run_id must be 1-64 safe ASCII characters")
        video = _must_exist(Path(video), "Input video")
        run_dir = Path(workspace) / run_id
        # Prevent silent overwrites and accidental reuse of intermediate artifacts.
        run_dir.mkdir(parents=True, exist_ok=False)
        for name in ("00_extract", "01_separate", "04_tts",
                     "05_duration", "06_lipsync", "07_mix", "08_render"):
            (run_dir / name).mkdir()

        audio = _must_exist(
            self.ports.media.extract_audio(video, run_dir / "00_extract/source.wav"),
            "Extract audio",
        )
        stems = self.ports.separation.separate(audio, run_dir / "01_separate")
        speech = _must_exist(stems.speech, "Speech separation")
        background = _must_exist(stems.background, "Background separation")

        source_segments = tuple(self.ports.transcription.transcribe(speech))
        _verify_source(source_segments)
        translated = tuple(self.ports.translation.translate(source_segments))
        _verify_translations(source_segments, translated)

        tts = _must_exist(
            self.ports.synthesis.synthesize(translated, run_dir / "04_tts/voice.wav"),
            "Arabic TTS",
        )
        aligned = _must_exist(
            self.ports.duration.align(tts, translated, run_dir / "05_duration/aligned.wav"),
            "Duration alignment",
        )

        # Face animation is optional: never force it on video without a usable face.
        video_for_render = video
        if self.ports.lip_sync is not None:
            video_for_render = _must_exist(
                self.ports.lip_sync.sync(
                    video, aligned, run_dir / "06_lipsync/synced.mp4"
                ), "Lip sync",
            )

        mixed = _must_exist(
            self.ports.mixing.mix(
                background, aligned, run_dir / "07_mix/final_audio.wav"
            ), "Audio mixing",
        )
        final = _must_exist(
            self.ports.media.render(
                video_for_render, mixed, run_dir / "08_render/dubbed.mp4"
            ), "Final render",
        )

        manifest = run_dir / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "input_video": str(video),
                    "output_video": str(final),
                    "lip_sync_applied": self.ports.lip_sync is not None,
                    "source_segments": [asdict(s) for s in source_segments],
                    "translated_segments": [asdict(s) for s in translated],
                    "status": "completed",
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return RunResult(run_id, final, manifest, source_segments, translated)
