# Software Requirements Specification (SRS)
# SentiVoice AI — Sentiment Analysis Web Application

**Version**: 2.0  
**Date**: April 2026  
**Status**: Active  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [System Architecture](#5-system-architecture)
6. [API Specification](#6-api-specification)
7. [Data Models](#7-data-models)
8. [Algorithms & Logic](#8-algorithms--logic)
9. [UI / UX Specifications](#9-ui--ux-specifications)
10. [Deployment Specification](#10-deployment-specification)
11. [Constraints & Assumptions](#11-constraints--assumptions)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the full software requirements for **SentiVoice AI**, a multilingual, multi-modal sentiment analysis web application. It covers functional capabilities, non-functional constraints, API design, algorithmic logic, and deployment configuration.

### 1.2 Scope
SentiVoice AI accepts text and voice input, analyzes emotional content using a hybrid dual-model approach, and presents results through an interactive dashboard. It supports English and Hinglish (Romanized Hindi + English) natively, and any language via auto-translation powered by Google Translate.

### 1.3 Definitions

| Term | Definition |
|---|---|
| Hinglish | Romanized Hindi mixed with English, common in informal Indian digital communication. |
| Naive Bayes | A probabilistic classification model using token-level lexicon matching. |
| Sequence Logic | A sliding-window analysis engine simulating sequential (LSTM-like) context awareness. |
| Confidence Score | A percentage (10–99%) representing the model's certainty in its primary emotion prediction. |
| Primary Emotion | The single emotion label with the highest aggregate score across both models. |

### 1.4 References
- Flask Documentation: https://flask.palletsprojects.com
- deep_translator: https://pypi.org/project/deep-translator/
- Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- Render.com Deployment: https://render.com/docs

---

## 2. Overall Description

### 2.1 Product Perspective
SentiVoice AI is a standalone web application. It operates as a monolithic Flask server serving both HTML templates and a JSON REST API. There is no external ML model dependency — all analysis logic is implemented as custom Python algorithms.

### 2.2 Product Functions (Summary)

| # | Function |
|---|---|
| F1 | User registration and session-based authentication |
| F2 | Text input with real-time sentiment highlighting |
| F3 | Voice-to-text input via browser Speech API |
| F4 | Multilingual text translation via Google Translate |
| F5 | Dual-model sentiment analysis (Naive Bayes + Sequence Logic) |
| F6 | Hinglish lexicon analysis with negation and intensifier handling |
| F7 | Auto-detection of Devanagari script and translation to English before analysis |
| F8 | Granular emotion breakdown across 11 categories |
| F9 | Per-user analysis history (in-memory + localStorage) |
| F10 | One-click history clear (client + server) |
| F11 | Copy result to clipboard |
| F12 | Export result as PNG image via Canvas API |

### 2.3 User Classes

| User Class | Description |
|---|---|
| **Authenticated User** | Has registered/logged in; can access the analysis dashboard and history. |
| **Unauthenticated Visitor** | Redirected to login page. Cannot access any analysis features. |
| **Admin (default)** | Pre-seeded account (`admin` / `password123`) for demonstration. |

### 2.4 Operating Environment
- **Server**: Python 3.x runtime with Gunicorn WSGI server.
- **Client**: Any modern browser supporting ES6+, the Web Speech API, and Canvas API.
- **Deployment**: Render.com (or any platform supporting Gunicorn).

---

## 3. Functional Requirements

### 3.1 User Authentication

| ID | Requirement |
|---|---|
| **FR-1** | The system SHALL allow new users to register with a unique username and password via `POST /register`. |
| **FR-2** | The system SHALL validate that the username does not already exist before creating an account. |
| **FR-3** | The system SHALL allow registered users to log in via `POST /login` (form or JSON body). |
| **FR-4** | The system SHALL store session identity using a cryptographically secure secret key (`os.urandom(24)`). |
| **FR-5** | The system SHALL redirect unauthenticated requests to `/login`. |
| **FR-6** | The system SHALL invalidate the session on `GET /logout` and redirect to `/login`. |

### 3.2 Text Input & Highlighting

| ID | Requirement |
|---|---|
| **FR-7** | The text input area SHALL accept up to 800 characters. |
| **FR-8** | The system SHALL display a live character count in the format `N / 800`. |
| **FR-9** | The system SHALL highlight positive-sentiment words in the input area in real time using a transparent overlay layer. |
| **FR-10** | The system SHALL highlight negative-sentiment words distinctly from positive words. |
| **FR-11** | Highlighting SHALL cover both English keywords and Hinglish multi-word phrases. |

### 3.3 Voice Input

| ID | Requirement |
|---|---|
| **FR-12** | The system SHALL provide a microphone button that activates the browser's `SpeechRecognition` API. |
| **FR-13** | The system SHALL support language selection from a dropdown (including en-US, hi-IN, es-ES, fr-FR, zh-CN). |
| **FR-14** | The system SHALL display interim transcription results in real time as the user speaks. |
| **FR-15** | The system SHALL auto-stop recording on silence and update the input area with the final transcript. |
| **FR-16** | The system SHALL display a visual waveform animation while recording is active. |
| **FR-17** | If the browser does not support `SpeechRecognition`, the microphone button SHALL be disabled and a message shown. |

### 3.4 Translation

| ID | Requirement |
|---|---|
| **FR-18** | The system SHALL provide a "Translate" button that sends the current input text to `POST /api/translate`. |
| **FR-19** | The backend SHALL use `deep_translator.GoogleTranslator` to translate text to the selected target language. |
| **FR-20** | The translated text SHALL replace the content of the input area upon success. |
| **FR-21** | If translation fails, the system SHALL display an error message in the status bar. |

### 3.5 Sentiment Analysis

| ID | Requirement |
|---|---|
| **FR-22** | The system SHALL send input text to `POST /api/analyze` on clicking the "Analyze" button. |
| **FR-23** | The backend SHALL detect Devanagari characters (`\u0900–\u097F`) and auto-translate to English before analysis. |
| **FR-24** | The system SHALL run the Naive Bayes model and produce a positivity score (0.0–1.0). |
| **FR-25** | The system SHALL run the Sequence Logic model over 3-token sliding windows and produce a positivity score (0.0–1.0). |
| **FR-26** | The system SHALL compute a combined score as: `NB_score × 0.6 + LSTM_score × 0.4`. |
| **FR-27** | The system SHALL compute a confidence value: `min(99, max(10, combined_score × 100 × 0.97))`. |
| **FR-28** | The system SHALL determine a Primary Emotion from 11 categories using the `get_primary_emotion()` function. |
| **FR-29** | The system SHALL return a breakdown of all emotion category scores as percentages. |
| **FR-30** | The system SHALL handle Hinglish negation by inverting the polarity contribution of a phrase if a negator (`nahi`, `mat`, etc.) appears within 10 characters before it. |
| **FR-31** | The system SHALL multiply phrase weight by 1.5× when a Hinglish intensifier (`bahut`, `ekdum`, etc.) precedes it. |

### 3.6 Results Display

| ID | Requirement |
|---|---|
| **FR-32** | The system SHALL display a Primary Emotion card with emoji, label, and descriptive text. |
| **FR-33** | The system SHALL animate an SVG ring to visualize the confidence percentage in the result's accent color. |
| **FR-34** | The system SHALL display individual model scores (Naive Bayes %, Sequence Logic %, Combined %). |
| **FR-35** | The system SHALL render a sorted list of emotion breakdown bars, each with a percentage and colored fill. |

### 3.7 History

| ID | Requirement |
|---|---|
| **FR-36** | The backend SHALL store the last 5 analysis results per user in `USER_HISTORY` (in-memory). |
| **FR-37** | The frontend SHALL store the last 5 analyses in `localStorage` under the key `sentiVoiceHistory`. |
| **FR-38** | On page load, the frontend SHALL call `GET /api/history`; if backend history is non-empty, it SHALL override localStorage. |
| **FR-39** | The "Clear History" button SHALL call `POST /api/clear_history` AND clear `localStorage` simultaneously. |

### 3.8 Export & Share

| ID | Requirement |
|---|---|
| **FR-40** | The "Copy" button SHALL copy the result summary (emotion, confidence, input text) to the clipboard. |
| **FR-41** | The "Share" button SHALL render the result onto an off-screen `<canvas>` element and trigger a download of `sentivoice-result.png`. |

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID | Requirement |
|---|---|
| **NFR-1** | The `/api/analyze` endpoint SHALL return a response within **500ms** for inputs up to 800 characters (excluding translation latency). |
| **NFR-2** | Frontend animations and transitions SHALL target **60 FPS**. |
| **NFR-3** | Real-time text highlighting SHALL update with **no perceptible lag** on input events. |

### 4.2 Security

| ID | Requirement |
|---|---|
| **NFR-4** | All analysis and history endpoints SHALL require an active authenticated session; unauthenticated requests return `401` or redirect. |
| **NFR-5** | The Flask secret key SHALL be generated at runtime using `os.urandom(24)`. |
| **NFR-6** | User passwords SHALL be stored in plaintext in the current in-memory store (acceptable for prototype); a production deployment MUST replace this with salted bcrypt hashing. |

### 4.3 Usability

| ID | Requirement |
|---|---|
| **NFR-7** | The interface SHALL be fully responsive across Desktop (≥1024px), Tablet (768px–1023px), and Mobile (<768px). |
| **NFR-8** | All user-facing error conditions (network failure, empty input, speech error) SHALL display a human-readable message in the status bar. |
| **NFR-9** | The application SHALL be operable without a mouse (keyboard-accessible form controls). |

### 4.4 Maintainability

| ID | Requirement |
|---|---|
| **NFR-10** | The emotion lexicons (`lexicon`, `hinglish_lexicon`) SHALL be defined as module-level dictionaries, editable without modifying core analysis logic. |
| **NFR-11** | All API routes SHALL return JSON responses with consistent structure. |

---

## 5. System Architecture

```
┌─────────────────────────────────────────┐
│              Browser Client              │
│  HTML (index.html / login.html)          │
│  CSS  (style.css)                        │
│  JS   (script.js)                        │
│   ├─ SpeechRecognition API               │
│   ├─ Canvas API (share image)            │
│   └─ localStorage (history cache)        │
└───────────────┬─────────────────────────┘
                │ HTTP / JSON
┌───────────────▼─────────────────────────┐
│         Flask Application (app.py)       │
│   ├─ Auth routes (/login, /register,     │
│   │               /logout)               │
│   ├─ Analysis route (/api/analyze)        │
│   ├─ Translation route (/api/translate)  │
│   └─ History routes (/api/history,       │
│                       /api/clear_history) │
│                                          │
│   ├─ analyze_naive_bayes(text)           │
│   ├─ analyze_lstm(text)                  │
│   ├─ get_primary_emotion(text)           │
│   └─ build_breakdown(categories)         │
│                                          │
│   External: GoogleTranslator (HTTP)      │
└─────────────────────────────────────────┘
```

---

## 6. API Specification

### `POST /login`
- **Body**: `{ "username": str, "password": str }` (JSON or form)
- **Success**: `{ "success": true, "redirect": "/" }` — sets session cookie
- **Failure**: `{ "success": false, "message": "Invalid credentials" }` — HTTP 401

### `POST /register`
- **Body**: `{ "username": str, "password": str }` (JSON)
- **Success**: `{ "success": true, "message": "Registration successful! You can now login." }`
- **Failure**: `{ "success": false, "message": "Username already exists" }` — HTTP 400

### `GET /logout`
- Clears session; redirects to `/login`.

### `POST /api/analyze`
- **Auth**: Required (session)
- **Body**: `{ "text": str, "lang": str }` (e.g., `"lang": "hi-IN"`)
- **Response**:
```json
{
  "naive_bayes": 72,
  "lstm": 68,
  "combined": 71,
  "confidence": 69,
  "primary": "Happy",
  "emoji": "😊",
  "color": "#ef4444",
  "primary_text": "Strong Happy signals detected (23% match).",
  "breakdown": { "Happy": 23, "Sad": 6, "Angry": 5, ... }
}
```

### `POST /api/translate`
- **Auth**: Required (session)
- **Body**: `{ "text": str, "target_lang": "en" | "hi" | "zh" }`
- **Success**: `{ "success": true, "translated_text": str }`
- **Failure**: `{ "success": false, "error": str }` — HTTP 500

### `GET /api/history`
- **Auth**: Required (session)
- **Response**: Array of last 5 analysis records for the current user.

### `POST /api/clear_history`
- **Auth**: Required (session)
- **Response**: `{ "success": true, "message": "History cleared from backend" }`

---

## 7. Data Models

### User Credentials (In-Memory)
```python
USER_CREDENTIALS: dict[str, str]
# { "username": "plain_password" }
```

### User History (In-Memory)
```python
USER_HISTORY: dict[str, list[dict]]
# { "username": [ { "text": str, "primary": str, "confidence": int, "timestamp": None }, ... ] }
# Max 5 entries per user (FIFO).
```

### History Record (localStorage)
```json
{ "text": "string", "primary": "Happy", "confidence": 85 }
```

---

## 8. Algorithms & Logic

### 8.1 Tokenization
```
normalize(text) → lowercase, strip non-alphanumeric/Devanagari → split on whitespace
```

### 8.2 Naive Bayes Engine (`analyze_naive_bayes`)
1. Tokenize input.
2. For each token at index `i`, match against 11-category English lexicon. Add `1.0 + log(1 + i/6)` to matched category.
3. Match Hinglish phrases with regex `\b<phrase>\b`. Apply weight (1.8 positive / 2.0 negative / 0.9 neutral).
4. Check for negators within 10 chars before phrase → flip polarity.
5. Check for intensifiers within 10 chars before phrase → multiply weight by 1.5.
6. Aggregate `pos_score` and `neg_score`. Compute logistic sigmoid of their log-likelihood difference.

### 8.3 Sequence Logic Engine (`analyze_lstm`)
1. Slide a 3-token window over all tokens.
2. Per window: check negation patterns (−2.0), check intensity modifiers (+0.6), match English lexicon (±1.1), match Hinglish phrases (±1.6, negation flips).
3. Accumulate weighted `sequence_score`; normalize with sigmoid over `count` windows.

### 8.4 Hybrid Scoring
```
combined_score = NB_score × 0.6 + LSTM_score × 0.4
confidence     = clamp(combined_score × 97, 10, 99)
```

### 8.5 Primary Emotion Detection (`get_primary_emotion`)
1. Token-level scoring across all lexicon categories (weight: 3 per match).
2. Hinglish phrase scoring (weight: 2 per match, negation-aware).
3. Highest-scoring category becomes the primary emotion.
4. Special sub-emotion rules: `heartbroken → Heartbroken`, `furious → Furious`, `anxious/worried → Anxious`.

---

## 9. UI / UX Specifications

### 9.1 Design System
- **Color Palette**: Red (`#ef4444`) and Black (`#050505`) as primary accents; zinc grays for surfaces.
- **Typography**: `Inter` (body), `Space Grotesk` (headings/labels) — loaded from Google Fonts.
- **Aesthetic**: Glassmorphism panels, smooth CSS transitions, high-contrast text.

### 9.2 Layout
- **Login Page** (`login.html`): Centered card with login and registration tabs. Red/black theme.
- **Dashboard** (`index.html`): Two-column layout on desktop — left panel (input + voice) / right panel (results + history). Single-column stack on mobile.

### 9.3 Interactive Elements

| Element | Behavior |
|---|---|
| Text Textarea | Live highlight overlay, scroll-synced. |
| Mic Button | Toggles recording; pulses + waveform animation while active. |
| Language Select | Updates speech recognition language and translate target. |
| Analyze Button | Triggers `/api/analyze`; shows loading spinner during request. |
| Translate Button | Triggers `/api/translate`; replaces textarea content. |
| Clear Button | Clears textarea and hides results panel. |
| Confidence Ring | SVG `stroke-dashoffset` animation to fill percentage. |
| Emotion Bars | Sorted horizontal `<div>` bars with color per emotion. |
| Copy Button | `navigator.clipboard.writeText(...)`. |
| Share Button | Canvas render → PNG download. |
| Clear History | Confirmation dialog → clears localStorage + backend. |

---

## 10. Deployment Specification

### Procfile
```
web: gunicorn app:app
```

### render.yaml
```yaml
services:
  - type: web
    name: sentivoice-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

### requirements.txt
```
Flask>=2.2
gunicorn
deep_translator
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PORT` | Port for the Gunicorn server | `5000` |
| `SECRET_KEY` | Flask session secret (recommended for production) | `os.urandom(24)` at startup |

---

## 11. Constraints & Assumptions

1. **No persistent database**: All user credentials and history are stored in-memory. Data is lost on server restart. A production version must integrate a database (e.g., PostgreSQL, MongoDB).
2. **Translation dependency**: The translation feature requires outbound internet access to Google Translate servers via `deep_translator`.
3. **Speech API**: Voice-to-text requires HTTPS or `localhost` in Chrome/Edge. It will not function over plain HTTP in production.
4. **Password security**: The current implementation stores passwords as plaintext strings. This MUST be replaced with bcrypt or Argon2 hashing before any production deployment.
5. **Lexicon coverage**: Sentiment analysis accuracy is bounded by the scope of the manually curated lexicons. Extended coverage requires lexicon expansion or integration of a trained ML model.
6. **Browser compatibility**: The `SpeechRecognition` API and `Canvas.toBlob()` are not supported in all browsers (Firefox partial, Safari limited). Graceful degradation is implemented.
