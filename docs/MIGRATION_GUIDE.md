# Graduation-1 notebooks → source modules: migration map

**This is a staged refactor, not a rewrite of old findings.**

| Legacy notebook section | Target interface/file | Migration state |
|---|---|---|
| Setup and Google Drive | Future `config/` and runtime adapters | Not migrated; old notebook preserved |
| FFmpeg audio extraction and final render | `media.py` (`FFmpegMedia`) | Implemented minimal baseline; not a byte-for-byte copy |
| Demucs + custom denoiser and `best_model.pth` | `SeparationPort` | Interface only; must verify model/checkpoint |
| WhisperX ASR/alignment | `TranscriptionPort` | Interface only; immutable segment and word schemas added |
| Gemini/Groq and translation prompt | `TranslationPort` | Interface only; original provider prompts unchanged in notebooks |
| ElevenLabs, Edge TTS, XTTS v2 | `SynthesisPort` | Interface only; no credentials or provider calls |
| Time fitting | `DurationPort` | Interface only; no actual waveform changes |
| MuseTalk/CodeFormer | Optional `LipSyncPort` | Interface only; historical outcomes not verified |
| FFmpeg audio mixing | `FFmpegBasicMixer` | Simplified baseline, not sidechain ducking |
| SRT output | `subtitles.to_srt` | Pure helper; no original timestamps edited |

The notebooks also include diarization and gender detection. Those features are **historical** and explicitly outside the currently approved research scope.

## Next milestones (not completed in this PR)

1. Verify checkpoint provenance, model architecture, license and inference I/O before implementing separation.
2. Add a WhisperX adapter that preserves the original IDs and word-alignment timings, with isolated fixtures.
3. Implement translator and TTS provider adapters behind explicit flags and mocks, never embedding secrets.
4. Add duration, background mixing and lip-sync integration with offline test fixtures.
5. Establish a dataset card, baseline and ablation tests against independent references; do not turn draft targets into measured results.

To run **core tests only** (Python 3.10+; no packages required):

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Do not run the original notebook cells automatically as part of these tests.
