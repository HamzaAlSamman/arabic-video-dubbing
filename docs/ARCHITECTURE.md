# Proposed modular architecture (initial foundation)

The new `src/arabic_dubbing/` is a **testable core**, not a finished dubbing product.

## Research pipeline

| Research stage | Runtime responsibility | Implementation status |
|---|---|---|
| 1. Extract audio | `MediaPort.extract_audio` | Minimal FFmpeg media adapter provided |
| 2. Train separation model | OFFLINE research/training notebook | **Not executed or migrated** |
| 3. Separate speech/background | `SeparationPort.separate` | Interface only; notebook logic remains unchanged |
| 4. ASR + aligned words | `TranscriptionPort.transcribe` | Interface only; source IDs/word times are validated |
| 5. Contextual translation | `TranslationPort.translate` | Interface only; verifies all source IDs and slots survive |
| 6. Arabic TTS | `SynthesisPort.synthesize` | Interface only |
| 7. Duration fitting | `DurationPort.align` | Interface only |
| 8. Lip synchronization (optional) | `LipSyncPort.sync` | Interface only; bypassable |
| 9. Re-mix with background | `MixingPort.mix` | FFmpeg **basic baseline** adapter provided |
| 10. Final video render | `MediaPort.render` | Minimal FFmpeg adapter provided |

## What is actually runnable?

- Pure data, SRT formatting, command construction, and the **pipeline with injected test doubles**.
- The FFmpeg adapter can be invoked independently with installed FFmpeg and valid media, but this commit **does not run it on actual audio/video**.
- There are no real registered adapters yet for Demucs, DualStreamResUNet, WhisperX, Gemini/Groq, TTS, duration adjustment, or MuseTalk. Therefore **do not advertise the end-to-end system as operational**.
- The lightweight unit tests mock subprocesses and model interfaces. They do **not** validate sound quality, translations, training, GPU execution or the final MP4.
- A `manifest.json` is written only after an explicitly invoked pipeline run returns existing output artifacts. It records source segments and word-level alignment without mutation; it is not a scientific evaluation report.

## Design decisions

- Preserve original notebooks and their outputs byte-for-byte under `notebooks/`.
- Inject adapters into `PipelinePorts`; **importing the library cannot invoke models or external APIs**.
- Training runs separately, never during inference.
- Initial tests assume one main instructor, not diarization or overlapping speaker separation.
- Original word-level timestamps and source IDs are immutable; translated segment slots must match by ID and timing.
- Fail loudly when an adapter produces no artifact. Use unique `run_id` directories and refuse overwriting existing run folders.
- Basic `amix` can clip and does not implement the notebook's sidechain ducking or LUFS normalization; use only for future baseline comparisons.

## Safety and reproducibility

No paid API, GPU, video processing, model load, or network action is part of these unit tests. A future real integration must have explicit opt-in to external providers, dataset/run manifests, pinned dependencies, benchmark validation and licensing review.
