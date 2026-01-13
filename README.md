# 🎥 AI Video Dubbing to Arabic (Colab Edition)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HamzaAlSamman/arabic-video-dubbing/blob/main/AI_Dubbing_System.ipynb)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python\&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange?logo=pytorch\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Note:** This project is designed to run seamlessly on **Google Colab** using T4 GPUs (with CPU fallback).

A comprehensive, end-to-end pipeline that converts any educational or general video into a **Modern Standard Arabic (MSA)** dubbed version using state-of-the-art AI — fully running on **Google Colab** with no local setup.

The system includes:

* Audio extraction from video
* Multi-stage voice enhancement and isolation
* Accurate ASR transcription with timestamps
* Context-aware Arabic rewriting (dubbing-oriented, not literal)
* Arabic Text-to-Speech generation
* Professional audio mixing and final video rendering

---

## 📑 Table of Contents

* [Demo](#-demo)
* [Pipeline Overview](#-pipeline-overview)
* [Key Features](#-key-features)
* [Tech Stack](#-tech-stack)
* [Prerequisites](#-prerequisites)
* [Setup & Usage](#-setup--usage)
* [Project Structure](#-project-structure)
* [Security](#-security)
* [Contributing](#-contributing)
* [License](#-license)

---

## 🎬 Demo

See the system in action:

[![Watch the Demo](https://img.youtube.com/vi/b4sYfCN6ilE/maxresdefault.jpg)](https://youtu.be/b4sYfCN6ilE)

> *Click the image above to watch the demo video.*

---

## 🔄 Pipeline Overview

The automated workflow follows a robust multi-stage pipeline:

1. **Audio Extraction**
   `FFmpeg` extracts the audio track from the source video.

2. **Primary Source Separation**
   **Demucs** separates vocals from background music and sound effects.

3. **Advanced Denoising (Custom Model)**
   The extracted vocals are processed through a **custom Dual-Stream Residual U-Net** to remove residual noise and artifacts.

4. **Transcription (ASR)**
   **WhisperX** generates precise, timestamp-aligned subtitles (SRT).

5. **Translation & Arabic Adaptation**
   LLMs (**Groq / Gemini**) rewrite and translate the text into **dubbing-friendly Arabic**, maintaining meaning and timing.

6. **Text-to-Speech (TTS)**
   Arabic voiceover is generated using **Edge TTS** or **ElevenLabs**.

7. **Dubbing & Audio Mixing**
   The Arabic voice is merged with the original background music using **Sidechain Ducking** to automatically reduce music volume during speech.

---

## ✨ Key Features

* 🚀 **Google Colab Native** – no local installation required
* 🧠 **Dual-Stage Audio Cleaning** – Demucs + custom **Dual-Stream Residual U-Net**
* ⚡ **GPU Accelerated** – optimized for T4 GPUs with CPU fallback
* 🗣️ **Smart Arabic Translation** – context-aware, dubbing-oriented (not literal)
* ⏱️ **Timing Adjustment** – aligns Arabic speech with original timestamps
* 🎧 **Professional Audio Mixing** – Sidechain Ducking for broadcast-quality sound
* 🤖 **Multi-LLM Support** – Groq (fast) or Gemini (high-context)
* ↔️ **RTL Arabic Support** – correct handling of Arabic text direction
* 🔒 **Secure API Handling** – no keys hard-coded (uses `.env`)

---

## 🧠 Tech Stack

| Component         | Technology                     | Role                      |
| ----------------- | ------------------------------ | ------------------------- |
| Environment       | Google Colab                   | Runtime & GPU             |
| Audio Processing  | FFmpeg                         | Extraction & Mixing       |
| Source Separation | Demucs                         | Vocals / Music Split      |
| Denoising         | **Dual-Stream Residual U-Net** | Custom Voice Refinement   |
| ASR               | WhisperX                       | Transcription & Alignment |
| LLMs              | Groq / Gemini                  | Translation & Logic       |
| TTS               | Edge TTS / ElevenLabs          | Arabic Voice Generation   |

---

## 📦 Prerequisites

Before running the notebook, ensure you have:

1. A **Google Account** (for Colab & Drive)
2. A source video file (`.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`)
3. **API Keys** (at least one LLM key is required):

   * Groq API Key **or** Gemini API Key
   * *(Optional)* ElevenLabs API Key for premium voices

---

## 🛠 Setup & Usage

### 1️⃣ Open in Colab

Click the **Open in Colab** badge at the top of this README.

### 2️⃣ Enable GPU

In Colab:
`Runtime → Change runtime type → T4 GPU`

### 3️⃣ Create `.env` File (Mandatory)

For security reasons, API keys must be stored in a `.env` file.

Inside the **Files** panel in Colab, create a file named `.env` and add:

```env
# LLM Providers (choose at least one)
GROQ_API_KEY=gsk_...
# GEMINI_API_KEY=AIza...

# TTS Providers (optional)
ELEVEN_API_KEY=xi_...
```

### 4️⃣ Run the Notebook

Execute the notebook cells **sequentially**.
You will be prompted to provide:

* A video upload
* Or a Google Drive video path

The final dubbed video will be generated automatically.

---

## 📁 Project Structure

```text
arabic-video-dubbing/
├── 📓 AI_Dubbing_System.ipynb      # Main pipeline notebook
├── 📄 README.md                    # Documentation
└── ⚙️ Runtime Directories (auto-created)
    ├── 📂 input                    # Source videos
    ├── 📂 work                     # Intermediate files (audio, SRT, text)
    └── 📂 output                   # Final dubbed videos
```

---

## 🔐 Security

* API keys are **never** stored in the code
* Keys are loaded from `.env`
* Make sure to add this to `.gitignore`:

```gitignore
.env
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/HamzaAlSamman/arabic-video-dubbing.git
   ```
3. Create a feature branch:

   ```bash
   git checkout -b feature/NewFeature
   ```
4. Commit your changes and push
5. Open a Pull Request

---

## 📄 License

This project is open-source under the **MIT License**.
See the `LICENSE` file for details.

---

<p align="center">
Built with ❤️ by <a href="https://github.com/HamzaAlSamman">Hamza</a>
</p>
