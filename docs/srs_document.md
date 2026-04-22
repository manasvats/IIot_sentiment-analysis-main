# Software Requirements Specification (SRS) for SentiVoice AI

## 1. Introduction
### 1.1 Purpose
The purpose of this document is to provide a detailed overview of the requirements for **SentiVoice AI**, a sentiment analysis web application. It outlines the functional and non-functional requirements, system architecture, and user interface specifications.

### 1.2 Scope
SentiVoice AI is a tool designed to analyze the sentiment of text and voice inputs. It provides users with emotional breakdowns, confidence scores, and historical tracking of analyzed sentiments.

---

## 2. Overall Description
### 2.1 Product Perspective
SentiVoice AI is a standalone web application built using Python (Flask) and modern frontend technologies. It serves as an intelligence dashboard for emotional analysis.

### 2.2 Product Functions
- User registration and secure login.
- Text-based sentiment analysis.
- Voice-to-text sentiment analysis.
- Real-time sentiment breakdown (Positive, Negative, Neutral).
- Emotion detection (Happy, Sad, Angry, etc.).
- Analysis history tracking.

---

## 3. Functional Requirements
### 3.1 User Authentication
- **FR-1**: Users must be able to create an account with a unique username and password.
- **FR-2**: Users must be able to log in securely to access the dashboard.
- **FR-3**: Session management must ensure that only authenticated users can access the analysis features.

### 3.2 Sentiment Analysis Engine
- **FR-4**: The system shall process text input using a hybrid Naive Bayes and Sequence Logic model.
- **FR-5**: The system shall support Hinglish (Hindi + English) text processing.
- **FR-6**: The system shall provide a confidence score (0-100%) for every analysis.
- **FR-7**: The system shall identify a "Primary Emotion" based on keyword intensity and contextual negation.

### 3.3 Voice Integration
- **FR-8**: The system shall provide a microphone interface for voice recording.
- **FR-9**: The system shall convert voice to text before processing it through the sentiment engine.

---

## 4. Non-Functional Requirements
### 4.1 Performance
- **NFR-1**: Analysis results should be returned within 500ms of submission.
- **NFR-2**: The UI must maintain 60FPS for all animations and transitions.

### 4.2 Security
- **NFR-3**: User passwords must be stored securely (simulated in memory for this version, salted/hashed in production).
- **NFR-4**: Session tokens must be cryptographically secure.

### 4.3 Usability
- **NFR-5**: The interface must be fully responsive (Desktop, Tablet, Mobile).
- **NFR-6**: The system must provide clear error feedback for invalid inputs or connection failures.

---

## 5. Technical Specifications
- **Framework**: Flask (Python)
- **Frontend**: ES6 JavaScript, HTML5, CSS3
- **Storage**: In-memory dictionary (simulated database)
- **Algorithms**: Naive Bayes, Custom Sequence Weighting (LSTM simulation)
