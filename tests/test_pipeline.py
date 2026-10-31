import json
from pathlib import Path
import tempfile
import unittest

from arabic_dubbing.data import Segment, Word, TranslatedSegment, SeparatedAudio
from arabic_dubbing.pipeline import DubbingPipeline, PipelinePorts


def make_file(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"test placeholder")
    return path


class FakeMedia:
    def extract_audio(self, video, destination):
        return make_file(destination)

    def render(self, video, dubbed_audio, destination):
        return make_file(destination)


class FakeSeparation:
    def separate(self, audio, output_dir):
        return SeparatedAudio(make_file(output_dir / "speech.wav"),
                              make_file(output_dir / "background.wav"))


class FakeASR:
    def transcribe(self, speech):
        return [Segment("seg-1", "Machine learning", 100, 2500,
                        (Word("Machine", 100, 900), Word("learning", 950, 2500)))]


class FakeTranslation:
    def __init__(self, mutate=False):
        self.mutate = mutate

    def translate(self, segments):
        source = segments[0]
        return [TranslatedSegment("wrong-id" if self.mutate else source.segment_id,
                                  "تعلّم الآلة", source.start_ms, source.end_ms)]


class FakeSynthesis:
    def synthesize(self, lines, destination):
        return make_file(destination)


class FakeDuration:
    def align(self, audio, lines, destination):
        return make_file(destination)


class FakeMix:
    def mix(self, background, speech, destination):
        return make_file(destination)


class FakeLip:
    def sync(self, video, speech, destination):
        return make_file(destination)


def ports(mutate=False, lip=False):
    return PipelinePorts(
        media=FakeMedia(), separation=FakeSeparation(),
        transcription=FakeASR(), translation=FakeTranslation(mutate),
        synthesis=FakeSynthesis(), duration=FakeDuration(),
        mixing=FakeMix(), lip_sync=FakeLip() if lip else None,
    )


class PipelineTests(unittest.TestCase):
    def test_offline_fake_pipeline_preserves_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = make_file(root / "lecture.mp4")
            run = DubbingPipeline(ports()).run(original, root / "runs", "trial_01")
            self.assertTrue(run.final_video.is_file())
            self.assertTrue(run.manifest.is_file())
            self.assertEqual(run.source_segments[0].segment_id, "seg-1")
            self.assertEqual(run.source_segments[0].words[1].end_ms, 2500)
            metadata = json.loads(run.manifest.read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "completed")
            self.assertFalse(metadata["lip_sync_applied"])
            self.assertEqual(original.read_bytes(), b"test placeholder")
            with self.assertRaises(FileExistsError):
                DubbingPipeline(ports()).run(original, root / "runs", "trial_01")

    def test_rejects_translation_changing_source_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_video = make_file(root / "lecture.mp4")
            with self.assertRaisesRegex(ValueError, "ID"):
                DubbingPipeline(ports(mutate=True)).run(
                    input_video, root / "runs", "bad_translation"
                )
            self.assertFalse((root / "runs/bad_translation/manifest.json").exists())

    def test_optional_lip_sync(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_video = make_file(root / "lecture.mp4")
            result = DubbingPipeline(ports(lip=True)).run(
                input_video, root / "runs", "lip_trial"
            )
            self.assertTrue(json.loads(result.manifest.read_text(encoding="utf-8"))["lip_sync_applied"])

    def test_rejects_bad_run_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_video = make_file(root / "lecture.mp4")
            with self.assertRaises(ValueError):
                DubbingPipeline(ports()).run(input_video, root / "runs", "../unsafe")


if __name__ == "__main__":
    unittest.main()
