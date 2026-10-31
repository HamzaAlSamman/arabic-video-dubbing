"""Minimal FFmpeg media adapter: explicit subprocess calls, no shell.

This is a basic research baseline, not the old notebook's sidechain-ducking,
loudness normalization, or lip-sync implementation.
"""
from pathlib import Path
import subprocess
from typing import Callable


def extract_command(video: Path, output: Path, executable: str = "ffmpeg") -> list[str]:
    return [executable, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(output)]


def mix_command(background: Path, speech: Path, output: Path,
                executable: str = "ffmpeg") -> list[str]:
    return [executable, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(background), "-i", str(speech),
            "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]",
            "-map", "[a]", "-c:a", "pcm_s16le", str(output)]


def render_command(video: Path, dubbed_audio: Path, output: Path,
                   executable: str = "ffmpeg") -> list[str]:
    return [executable, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(video), "-i", str(dubbed_audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-shortest", str(output)]


class FFmpegMedia:
    """Executes extract/render only on explicit method calls."""
    def __init__(self, executable: str = "ffmpeg",
                 runner: Callable[..., object] = subprocess.run):
        self.executable = executable
        self.runner = runner

    def _execute(self, args: list[str], output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        self.runner(args, check=True, capture_output=True, text=True)
        if not output.is_file():
            raise FileNotFoundError(f"FFmpeg output missing: {output}")
        return output

    def extract_audio(self, video: Path, destination: Path) -> Path:
        return self._execute(
            extract_command(video, destination, self.executable), destination
        )

    def render(self, video: Path, dubbed_audio: Path, destination: Path) -> Path:
        return self._execute(
            render_command(video, dubbed_audio, destination, self.executable), destination
        )


class FFmpegBasicMixer:
    """Simple amix baseline; not loudness-normalized or production-safe."""
    def __init__(self, executable: str = "ffmpeg",
                 runner: Callable[..., object] = subprocess.run):
        self.executable = executable
        self.runner = runner

    def mix(self, background_audio: Path, speech_audio: Path,
            destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.runner(
            mix_command(background_audio, speech_audio, destination, self.executable),
            check=True, capture_output=True, text=True,
        )
        if not destination.is_file():
            raise FileNotFoundError(f"FFmpeg mix output missing: {destination}")
        return destination
