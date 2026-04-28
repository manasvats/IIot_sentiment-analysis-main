# SentiVoice AI — Project Description

## Overview

**SentiVoice AI** is a full-stack, AI-driven sentiment analysis web application built with Python (Flask) and modern frontend technologies. The platform enables users to analyze the emotional tone of text and speech inputs in real time, with deep support for both English and **Hinglish** (Romanized Hindi + English). It combines a dual-model analysis engine with a rich, premium interface to deliver granular emotion detection far beyond simple positive/negative classification.

---

## Key Features

### 🔐 Authentication System
- User **registration** and **login** via a secure session-based flow.
- New users can register directly from the login page.
- Protected routes redirect unauthenticated users to the login screen.
- Cryptographically secure session keys (`os.urandom(24)`).

### 🧠 Dual-Model Sentiment Engine
- **Naive Bayes Engine**: Token-based classification across 11 emotion categories with logarithmic positional weighting.
- **Sequence Logic Engine (LSTM-inspired)**: Sliding 3-token window analysis that detects negation patterns and intensity modifiers in sequence.
- **Hybrid Scoring**: Final sentiment is a weighted blend — 60% Naive Bayes + 40% Sequence Logic — producing a confidence score (10–99%).

### 🌐 Hinglish Intelligence
- Dedicated Hinglish lexicon with 80+ positive and 50+ negative phrases.
- Negation detection (`nahi`, `mat`, `na`, etc.) that flips sentiment polarity.
- Intensifier support (`bahut`, `ekdum`, `zyada`) that boosts phrase weight by 1.5×.
- Automatic detection of Devanagari script (`\u0900–\u097F`) to trigger auto-translation before analysis.

### 🌍 Multi-Language Translation
- Powered by **`deep_translator` (Google Translate API)**.
- Users can translate input text to English, Hindi, or Chinese (Simplified) before analysis.
- Backend `/api/translate` endpoint handles translation for both display and analysis purposes.

### 🎤 Voice-to-Text Input
- Uses the browser's **Web Speech API** (`SpeechRecognition`).
- Supports multiple recognition languages selectable via a dropdown (English, Hindi, Spanish, French, Mandarin, etc.).
- Auto-stops on silence; visual waveform animation during recording.
- Interim results displayed in real time as the user speaks.

### 🎨 Live Sentiment Highlighting
- Text in the input area is highlighted in real time: **positive words** in one color, **negative words** in another.
- A transparent overlay layer is synced with the textarea's scroll position.
- Covers both English and Hinglish keyword sets.

### 📊 Rich Results Dashboard
- **Primary Emotion Card**: emoji, label, and descriptive text for the detected emotion.
- **Confidence Ring**: Animated SVG ring showing the confidence percentage.
- **Model Score Breakdown**: Individual scores for Naive Bayes, Sequence Logic, and Combined.
- **Emotion Breakdown Bars**: Sorted horizontal bars for all 11 emotion categories.

### 🗂️ Analysis History
- Last 5 analyses stored in both **localStorage** (client) and **in-memory backend session** (server).
- On page load, the backend history takes precedence over local storage.
- One-click **Clear History** wipes both storage layers simultaneously.

### 📤 Share & Copy
- **Copy Result**: Copies emotion label, confidence, and input text to clipboard.
- **Share as Image**: Renders the result to an off-screen `<canvas>` and downloads it as a PNG (`sentivoice-result.png`).

### 📡 Deployment Ready
- `Procfile` configured for **Gunicorn** WSGI server.
- `render.yaml` present for one-click deployment to **Render.com**.
- Dynamically binds to `PORT` environment variable for cloud compatibility.

---

## Technical Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.x, Flask ≥ 2.2 |
| **WSGI Server** | Gunicorn |
| **Translation** | deep_translator (Google Translate) |
| **Frontend** | HTML5, CSS3 (Vanilla), JavaScript (ES6+) |
| **Speech** | Web Speech API (`SpeechRecognition`) |
| **Typography** | Google Fonts — Inter, Space Grotesk |
| **Storage** | In-memory dict (server) + localStorage (client) |
| **Deployment** | Render.com (render.yaml + Procfile) |

---

## Emotion Categories

The system recognizes **17 distinct emotional states**:

| Positive | Negative | Neutral |
|---|---|---|
| Happy, Joyful, Excited | Sad, Heartbroken | Neutral |
| Grateful, Peaceful | Angry, Furious | Uncertain |
| Hopeful | Fearful, Anxious | |
| | Disgusted, Disappointed | |

---

## Target Audience

- **Customer Support Teams** — Gauge client satisfaction and flag escalating frustration.
- **Content Creators** — Understand the emotional impact of scripts and posts.
- **Educators & Researchers** — Study sentiment patterns in multilingual and code-switched text.
- **Developers** — Use as a foundation for emotion-aware APIs and integrations.
