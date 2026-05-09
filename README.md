# 🎬 Arabic Video Dubbing System

> **End-to-end AI-powered pipeline for dubbing English videos into Modern Standard Arabic with multi-speaker voice synthesis, lip-sync, and automatic gender-aware voice mapping.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-11.8+-green.svg)](https://developer.nvidia.com/cuda-toolkit)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Colab](https://img.shields.io/badge/Open%20in-Colab-orange.svg)](https://colab.research.google.com/)

---

## 📖 Overview

A production-grade Jupyter notebook that automates the entire video dubbing workflow — from raw video input to a final lip-synced Arabic-dubbed output. The system unifies state-of-the-art models for speech recognition, speaker diarization, gender detection, neural translation, multi-voice text-to-speech, and lip synchronization into a single cohesive pipeline.

### Key Highlights

- 🎙️ **Unified ASR + Diarization + Gender Detection** — Single pipeline replacing legacy multi-model workflows
- 🗣️ **Automatic Multi-Voice TTS** — Different voice for each speaker, auto-mapped by detected gender
- 🌍 **Time-Aware Arabic Translation** — LLM-powered translation respecting subtitle duration constraints
- 💋 **Optional Lip-Sync Enhancement** — MuseTalk + CodeFormer for broadcast-quality output
- 🎚️ **Professional Audio Mixing** — Sidechain ducking + EBU R128 loudness normalization
- 📝 **RTL-Aware Subtitle Generation** — Properly formatted Arabic subtitles with mixed-language support

---

## 🏗️ Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    INPUT: English Video (.mp4)                       │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 1: Audio Extraction     │
                  │     (FFmpeg → 16kHz mono)     │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 2: Source Separation    │
                  │  ├── Demucs (vocals/bg)       │
                  │  └── DualStream ResUNet       │
                  │      (speech denoising)       │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 3: Unified Pipeline 🆕  │
                  │  ├── WhisperX ASR             │
                  │  ├── Word-level Alignment     │
                  │  ├── pyannote Diarization     │
                  │  └── Wav2Vec2 Gender Detect   │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 4: Arabic Translation   │
                  │  ├── Gemini / Groq LLM        │
                  │  ├── Time-aware compression   │
                  │  └── Number-to-words          │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 5: Multi-Voice TTS 🆕   │
                  │  ├── Edge TTS / ElevenLabs    │
                  │  ├── Auto gender→voice map    │
                  │  └── atempo time-fitting      │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 6: Audio Mixing         │
                  │  ├── Sidechain ducking        │
                  │  └── EBU R128 loudnorm        │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 7: Final Render         │
                  │  ├── Mux video + dub audio    │
                  │  └── RTL-fixed subtitles      │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  Step 8: Lip-Sync (Optional)  │
                  │  ├── MuseTalk inference       │
                  │  └── CodeFormer enhancement   │
                  └───────────────┬───────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────────┐
│              OUTPUT: Arabic-Dubbed Video + Subtitles                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Capabilities

| Feature | Technology | Description |
|---------|-----------|-------------|
| **Speech Recognition** | WhisperX (large-v3) | High-accuracy multilingual ASR |
| **Word Alignment** | wav2vec2 forced alignment | Sub-second word-level timestamps |
| **Speaker Diarization** | pyannote 3.1 | Identifies who speaks when |
| **Gender Detection** | Wav2Vec2 classifier | Per-speaker gender classification |
| **Translation** | Gemini 2.0 / Groq Qwen3 | Domain-aware MSA translation |
| **TTS** | Microsoft Edge / ElevenLabs | Neural Arabic voice synthesis |
| **Vocal Separation** | Demucs htdemucs | Music/vocals isolation |
| **Speech Denoising** | Custom DualStream ResUNet | Spectral noise suppression |
| **Lip Sync** | MuseTalk | Audio-driven mouth animation |
| **Face Restoration** | CodeFormer | High-fidelity face enhancement |

### Smart Features

- **Auto Gender-Voice Mapping** — Male speakers get male voices, female speakers get female voices, with no manual configuration
- **Time-Constrained Translation** — Each translated line respects the original subtitle duration, with automatic compression passes for over-budget lines
- **Multi-Speaker Voice Continuity** — Same speaker maintains the same voice throughout the video
- **Number Localization** — Digits are converted to Arabic words for natural TTS pronunciation
- **RTL Subtitle Handling** — Proper bidirectional text formatting for mixed Arabic/Latin content
- **Resilient Caching** — TTS outputs are cached by content hash to enable safe iteration
- **Pipeline State Persistence** — JSON-based state management survives runtime restarts

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

1. Open the notebook in Colab:
   ```
   https://colab.research.google.com/github/<your-username>/<repo>/blob/main/Arabic_Dubbing_System_Unified.ipynb
   ```
2. Set runtime type to **GPU** (T4 minimum, A100 recommended for Step 8)
3. Run cells sequentially from Step 0 to Step 7 (or Step 8 for lip-sync)

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/arabic-dubbing-system.git
cd arabic-dubbing-system

# Create a Python 3.10 environment
conda create -n dubbing python=3.10 -y
conda activate dubbing

# Install FFmpeg
sudo apt-get install ffmpeg libsndfile1

# Launch Jupyter
jupyter notebook Arabic_Dubbing_System_Unified.ipynb
```

---

## 🔑 Required API Keys

Create a `.env` file at `/content/.env` (Colab) or in your working directory:

```env
# Required for Diarization (Step 3)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxx

# Required for Translation (Step 4) - choose one
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxx

# Required only if using ElevenLabs TTS (Step 5)
ELEVEN_API_KEY=xxxxxxxxxxxxxxxxxx
```

### How to obtain tokens

| Service | URL | Required For |
|---------|-----|--------------|
| HuggingFace | https://huggingface.co/settings/tokens | Diarization |
| HuggingFace License | https://huggingface.co/pyannote/speaker-diarization-3.1 | Accept license |
| HuggingFace License | https://huggingface.co/pyannote/segmentation-3.0 | Accept license |
| Groq | https://console.groq.com/keys | Translation (free tier) |
| Google AI Studio | https://aistudio.google.com/app/apikey | Translation (free tier) |
| ElevenLabs | https://elevenlabs.io/app/settings/api-keys | TTS (paid) |

---

## 📦 Dependencies

The notebook auto-installs all dependencies, but key requirements include:

### Main Pipeline (Steps 0-7)
- `torch >= 2.0`, `torchaudio`
- `whisperx` (with `pyannote.audio`)
- `demucs >= 4.0`
- `transformers >= 4.38, < 5`
- `edge-tts`, `pydub`, `pysrt`, `soundfile`
- `groq`, `google-genai`
- `pandas`, `numpy < 2`

### Lip-Sync Pipeline (Step 8)
- Python 3.10 (Miniconda environment)
- `torch == 2.0.1+cu118`, `torchvision == 0.15.2`
- `mmcv >= 2.0.1`, `mmdet >= 3.1.0`, `mmpose >= 1.1.0`
- `basicsr`, `facexlib`, `lpips`, `realesrgan`
- MuseTalk + CodeFormer model weights (~10 GB)

### Required Model Weights
- `best_model.pth` — DualStream ResUNet weights (place in `/content/gdrive/MyDrive/dub_project/`)
- All other weights download automatically

---

## 📂 Project Structure

```
arabic-dubbing-system/
├── Arabic_Dubbing_System_Unified.ipynb   # Main pipeline notebook
├── README.md                              # This file
├── LICENSE                                # MIT License
└── runtime/                               # Auto-created during execution
    ├── input/                            # Input videos
    ├── work/                             # Intermediate artifacts
    │   ├── 00_extract/                   # Extracted audio/video
    │   ├── 01_demucs/                    # Demucs stems
    │   ├── 02_denoise/                   # Cleaned speech
    │   ├── 03_asr_diarize/               # Transcripts + speaker info
    │   ├── 04_translate/                 # Arabic SRT files
    │   ├── 05_tts/                       # Generated TTS clips
    │   └── 06_mix/                       # Final audio mix
    └── output/                           # Final deliverables
        ├── *_dubbed.mp4                  # Step 7 output
        └── final_video_lipsync.mp4       # Step 8 output (optional)
```

---

## ⚙️ Configuration

### Voice Selection

Edit Step 5.0 cell parameters:

```python
EDGE_VOICE_MALE   = "ar-SA-HamedNeural"     # Saudi male
EDGE_VOICE_FEMALE = "ar-SA-ZariyahNeural"   # Saudi female
```

Available Edge TTS Arabic voices:
- **Saudi**: `ar-SA-HamedNeural` (M), `ar-SA-ZariyahNeural` (F)
- **Egyptian**: `ar-EG-ShakirNeural` (M), `ar-EG-SalmaNeural` (F)
- **UAE**: `ar-AE-HamdanNeural` (M), `ar-AE-FatimaNeural` (F)

### Translation Tuning

```python
AR_CHARS_PER_SEC      = 13.0    # Target Arabic speech rate
SOFT_OVER_BUDGET      = 1.15    # Trigger compression if 15% over
MAX_COMPRESS_ROUNDS   = 2       # Re-compression passes
DOMAIN                = "academic"  # general | technical | medical | academic
```

### Mix Parameters

```python
music_gain_db    = -2.0    # Background music attenuation
duck_threshold   = 0.02    # Sidechain trigger level
duck_ratio       = 8.0     # Compression ratio when ducking
```

---

## 🎓 Usage Examples

### Example 1: Quick Dub (Steps 0-7, ~10-15 min)

```python
# In notebook, just run cells 0 through 7.2
# Output: /content/dub_project/output/<video>_dubbed.mp4
```

### Example 2: Premium Quality (Steps 0-8, ~45-60 min)

```python
# Run all cells including Step 8
# Note: Step 8.1 will reset the runtime - this is normal
# After restart, continue from Step 8.2
# Output: /content/dub_project/output/final_video_lipsync.mp4
```

### Example 3: Custom Voice for Specific Speaker

After Step 3, modify the gender map manually before Step 5:

```python
PIPELINE_PATHS["speaker_gender_map"] = {
    "SPEAKER_00": "male",
    "SPEAKER_01": "female",
    "SPEAKER_02": "male"  # Override auto-detection
}
```

---

## 📊 Performance Benchmarks

Tested on Google Colab T4 GPU with a 10-minute educational video:

| Step | Duration | GPU Memory |
|------|----------|------------|
| 1. Audio Extraction | ~30s | 0 GB |
| 2. Demucs + Denoise | ~2 min | 4 GB |
| 3. ASR + Diarization | ~3 min | 8 GB |
| 4. Translation | ~1 min | 0 GB |
| 5. Multi-voice TTS | ~2 min | 0 GB |
| 6. Mixing | ~30s | 0 GB |
| 7. Final Render | ~30s | 0 GB |
| **Total (Steps 0-7)** | **~10 min** | **8 GB peak** |
| 8. Lip-Sync (optional) | ~30 min | 14 GB |
| **Total (Steps 0-8)** | **~40 min** | **14 GB peak** |

---

## 🛠️ Troubleshooting

### Common Issues

**`HF_TOKEN not accepted` during diarization**
- Ensure you've accepted licenses for both pyannote models (links above)
- Token must have `read` permissions

**`Demucs failed on all settings`**
- Reduce `segments_try` to `"1"` in Step 2.1
- Switch device to `cpu` if GPU memory is exhausted

**`Edge TTS WSServerHandshakeError`**
- Network/regional issue with Microsoft endpoints
- Retry the cell (built-in 5-attempt backoff)
- Switch to ElevenLabs as fallback

**`MuseTalk: ImportError torchvision.transforms.functional_tensor`**
- Step 8 requires a clean Python 3.10 environment
- Run cells 8.1 → 8.4 in order without skipping
- Restart runtime if needed after Step 8.1

**Arabic text rendering as `???` in subtitles**
- Ensure your video player supports UTF-8 SRT
- Check that Step 7.0 (RTL fix) ran successfully

### Memory Optimization

If running on T4 (15 GB) and hitting OOM:
- Step 2: Use `htdemucs` instead of `htdemucs_ft`
- Step 3: Set `compute_type` to `int8` instead of `float16`
- Step 8: Skip lip-sync or use external A100 instance

---

## 🗺️ Roadmap

### Planned Features
- [ ] **Voice Cloning** — Clone original speaker voices via XTTS-v2 / OpenVoice
- [ ] **Interactive SRT Editor** — Review and edit translations before TTS generation
- [ ] **Translation Glossary** — Custom term dictionary for consistent terminology
- [ ] **Web UI** — Gradio/Streamlit interface for non-technical users
- [ ] **Multi-dialect Support** — Egyptian, Levantine, Gulf dialect options
- [ ] **Bilingual Subtitles** — Arabic + English side-by-side
- [ ] **Batch Processing** — Process multiple videos in queue
- [ ] **Real-time Mode** — Live streaming dubbing
- [ ] **Emotion-aware TTS** — Preserve emotional tone from source

### Recently Added
- [x] Unified ASR + Diarization + Gender pipeline
- [x] Auto gender-to-voice mapping
- [x] Optional MuseTalk + CodeFormer lip-sync
- [x] Pipeline state persistence across runtime restarts

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas Where Help Is Needed
- Testing on different video genres (movies, podcasts, lectures)
- Dialect-specific TTS voice tuning
- Performance optimization for low-VRAM GPUs
- Documentation translations

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

### Third-Party Model Licenses

This project uses several open-source models, each governed by their own licenses. **Users are responsible for complying with the licenses of all underlying models for their use case (especially commercial use):**

- **WhisperX** — BSD 4-Clause
- **pyannote.audio** — MIT (gated access required)
- **Demucs** — MIT
- **MuseTalk** — MIT
- **CodeFormer** — S-Lab License (non-commercial research only)
- **Edge TTS** — Microsoft Terms of Service apply
- **ElevenLabs** — Subject to ElevenLabs commercial license

---

## 🙏 Acknowledgments

This project builds on the incredible work of:

- [WhisperX](https://github.com/m-bain/whisperX) by Max Bain et al.
- [pyannote-audio](https://github.com/pyannote/pyannote-audio) by Hervé Bredin
- [Demucs](https://github.com/facebookresearch/demucs) by Meta AI
- [MuseTalk](https://github.com/TMElyralab/MuseTalk) by Tencent ML Lab
- [CodeFormer](https://github.com/sczhou/CodeFormer) by Shangchen Zhou
- [Edge TTS](https://github.com/rany2/edge-tts) by rany2

---

## 📧 Contact

For questions, suggestions, or collaboration:
- Open an [issue](https://github.com/<your-username>/<repo>/issues)
- Start a [discussion](https://github.com/<your-username>/<repo>/discussions)

---

<div align="center">

**⭐ If this project helps you, please consider giving it a star! ⭐**

Made with ❤️ for the Arabic-speaking community

</div>
