import unittest
from arabic_dubbing.data import Segment, Word, TranslatedSegment
from arabic_dubbing.subtitles import to_srt


class DataTests(unittest.TestCase):
    def test_preserves_word_timing_and_segment_id(self):
        word = Word("Script", 100, 450)
        item = Segment("lesson:001", "Script", 100, 500, (word,))
        self.assertEqual(item.segment_id, "lesson:001")
        self.assertEqual(item.words[0].start_ms, 100)
        self.assertEqual(item.words[0].end_ms, 450)

    def test_rejects_invalid_ranges_and_word_spill(self):
        with self.assertRaises(ValueError):
            Word("bad", 100, 100)
        with self.assertRaises(ValueError):
            Segment("id", "text", 0, 100, (Word("overflow", 0, 101),))
        with self.assertRaises(TypeError):
            Word("bad", 0.0, 50)

    def test_srt_supports_arabic_and_milliseconds(self):
        lines = [TranslatedSegment("a", "مرحبًا بالعالم", 1000, 2150)]
        self.assertIn("00:00:01,000 --> 00:00:02,150", to_srt(lines))
        self.assertIn("مرحبًا بالعالم", to_srt(lines))


if __name__ == "__main__":
    unittest.main()
