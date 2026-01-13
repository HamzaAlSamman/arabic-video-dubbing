# 🎥 AI Video Dubbing to Arabic (Colab Edition)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HamzaAlSamman/arabic-video-dubbing/blob/main/AI_Dubbing_System.ipynb)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Note:** This project is designed to run seamlessly on **Google Colab** using T4 GPUs.

A comprehensive, end-to-end pipeline to convert any educational or general video into a **Modern Standard Arabic (MSA)** dubbed version. The system leverages state-of-the-art AI models for vocal isolation, transcription, translation, and speech synthesis, requiring **zero local setup**.

---

## 📑 Table of Contents
- [Demo](#-demo)
- [Pipeline Overview](#-pipeline-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Setup & Usage](#-setup--usage)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎬 Demo

> *Watch a sample output comparing the original video with the AI-dubbed Arabic version.*

*(Replace this line with a link to your YouTube video or a GIF)*

---

## 🔄 Pipeline Overview

The automated process follows these 6 stages:

1.  **Audio Extraction:** `FFmpeg` separates audio tracks from the video file.
2.  **Vocal Isolation:** `Demucs` removes background noise and music, isolating human speech.
3.  **Transcription (ASR):** `WhisperX` generates precise, timestamped subtitles.
4.  **Translation & Paraphrasing:** LLMs (`Groq`/`Gemini`) convert text to context-aware Arabic suitable for dubbing.
5.  **Text-to-Speech (TTS):** `EdgeTTS` or `ElevenLabs` generates the Arabic voiceover.
6.  **Dubbing:** The new audio is merged with the original video (with background noise re-mixed if desired).

---

## ✨ Key Features

-   🚀 **Google Colab Native:** Zero local installation required.
-   ⚡ **Hardware Acceleration:** Optimized for T4 GPUs with CPU fallback.
-   🗣️ **Smart Translation:** Context-aware translation tailored for dubbing (not literal).
-   ⏱️ **Timing Adjustment:** Logic to fit the Arabic audio within original timestamps.
-   🤖 **Multi-LLM Support:** Flexible choice between **Groq** (Fast) or **Gemini** (High Context).
-   🎙️ **Multi-TTS Support:** Support for **Edge TTS** (Free) and **ElevenLabs** (Premium).
-   ↔️ **RTL Support:** Proper rendering and handling of Arabic text.
-   🔒 **Secure:** API keys managed via `.env` file.

---

## 🧠 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Environment** | Google Colab | Runtime & GPU |
| **Processing** | FFmpeg | Audio/Video manipulation |
| **Separation** | Demucs (Facebook) | Vocal Isolation |
| **ASR** | WhisperX | Transcription & Alignment |
| **LLM** | Groq / Gemini Pro | Translation & Logic |
| **TTS** | EdgeTTS / ElevenLabs | Voice Generation |

---

## 📦 Prerequisites

Before running the notebook, ensure you have:

1.  A **Google Account** (for Colab & Drive).
2.  A source video file (`.mp4`, `.mov`, `.mkv`, `.avi`).
3.  **API Keys** (At least one LLM key is required):
    * [Groq API Key](https://console.groq.com/) OR [Gemini API Key](https://aistudio.google.com/).
    * *(Optional)* [ElevenLabs API Key](https://elevenlabs.io/) for premium voices.

---

## 🛠 Setup & Usage

### 1. Open in Colab
Click the "Open in Colab" badge at the top of this README.

### 2. Set Runtime to GPU
In the Colab menu: `Runtime` → `Change runtime type` → `T4 GPU`.

### 3. Create `.env` File (Mandatory)
For security, create a file named `.env` inside the Colab **Files** section and add your keys:

```env
# LLM Providers (Choose at least one)
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...

# TTS Providers (Optional)
ELEVEN_API_KEY=xi...
