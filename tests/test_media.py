from pathlib import Path
import tempfile
import unittest

from arabic_dubbing.media import (
    FFmpegBasicMixer, FFmpegMedia, extract_command, mix_command, render_command,
)


class MediaTests(unittest.TestCase):
    def test_commands_use_arg_list_not_shell(self):
        name = Path("lecture; echo unsafe.mp4")
        cmd = extract_command(name, Path("track.wav"))
        self.assertEqual(cmd[0], "ffmpeg")
        self.assertIn(str(name), cmd)
        self.assertEqual(cmd[-1], "track.wav")
        self.assertNotIn("sh", cmd)
        self.assertIn("-filter_complex", mix_command(Path("bg.wav"), Path("ar.wav"), Path("mix.wav")))
        self.assertEqual(render_command(name, Path("mix.wav"), Path("out.mp4"))[-1], "out.mp4")

    def test_runner_is_mocked_without_ffmpeg(self):
        invocations = []
        def fake_runner(cmd, **kwargs):
            invocations.append((cmd, kwargs))
            Path(cmd[-1]).write_bytes(b"fake ffmpeg bytes")

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = FFmpegMedia(runner=fake_runner)
            mixer = FFmpegBasicMixer(runner=fake_runner)
            media.extract_audio(root / "source.mp4", root / "source.wav")
            mixer.mix(root / "background.wav", root / "ar.wav", root / "mixed.wav")
            media.render(root / "source.mp4", root / "mixed.wav", root / "output.mp4")
            self.assertEqual(len(invocations), 3)
            for _, kwargs in invocations:
                self.assertTrue(kwargs["check"])
                self.assertNotIn("shell", kwargs)


if __name__ == "__main__":
    unittest.main()
