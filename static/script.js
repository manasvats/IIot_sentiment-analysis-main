const inputText = document.getElementById('inputText');
const highlightLayer = document.getElementById('highlightLayer');
const micButton = document.getElementById('micButton');
const stopButton = document.createElement('button');
const recordStatus = document.getElementById('recordStatus');
const recordHint = document.getElementById('recordHint');
const languageToggle = document.getElementById('languageToggle');
const languageMode = document.getElementById('languageMode');
const analyzeButton = document.getElementById('analyzeButton');
const clearButton = document.getElementById('clearButton');
const confidenceIndicator = document.getElementById('confidenceIndicator');
const resultsArea = document.getElementById('resultsArea');
const loadingState = document.getElementById('loadingState');
const primaryEmoji = document.getElementById('primaryEmoji');
const primaryLabel = document.getElementById('primaryLabel');
const primaryText = document.getElementById('primaryText');
const confidenceValue = document.getElementById('confidenceValue');
const ringFill = document.getElementById('ringFill');
const nbValue = document.getElementById('nbValue');
const lstmValue = document.getElementById('lstmValue');
const combinedValue = document.getElementById('combinedValue');
const breakdownBars = document.getElementById('breakdownBars');
const historyList = document.getElementById('historyList');
const charCount = document.getElementById('charCount');
const copyButton = document.getElementById('copyButton');
const shareButton = document.getElementById('shareButton');
const waveform = document.getElementById('waveform');
const shareCanvas = document.getElementById('shareCanvas');

const POSITIVE_WORDS = ['happy','glad','pleased','delighted','cheerful','content','joyful','elated','ecstatic','thrilled','overjoyed','blissful','radiant','beaming','wonderful','fantastic','great','amazing','awesome','brilliant','superb','excellent','love','loved','beautiful','pretty','cute','adorable'];
const NEGATIVE_WORDS = ['sad','unhappy','sorrowful','depressed','gloomy','miserable','heartbroken','dejected','downcast','melancholy','grief','mourning','crying','weeping','tears','upset','hurt','broken','lost','lonely','alone','abandoned','angry','furious','enraged','irate','livid','outraged','infuriated','fuming','mad','irritated','annoyed','agitated','frustrated','resentful','bitter','hostile','wrathful','seething','afraid','scared','frightened','terrified','anxious','worried','nervous','panicked','horrified','dreadful','apprehensive','uneasy','tense','stressed','overwhelmed','paranoid','disgusted','repulsed','revolted','appalled','nauseated','horrified','offended','disturbed','disappointed','let down','failed','hopeless','discouraged','disheartened','defeated','disillusioned'];
const HINGLISH_POSITIVE = ['mast','zabardast','bindaas','badhiya','ekdum','shandaar','kamaal','jabardast','khush','bahut acha','bohot acha','achi baat','maja aa gaya','maja aaya','full mast','ekdum badhiya','ek number','life set hai','sab theek','bilkul sahi','haan ji','wah wah','wah bhai','superb yaar','acha laga','pyaar','mohabbat','dil khush','dil bhar aaya','khushi','anand','sukoon','shanti','maza','masti','jiyenge','jai ho','bahut shukriya','shukriya','dhanyawad','meherbani','bahut badhiya','thoda zyada khush'];
const HINGLISH_NEGATIVE = ['bura','bahut bura','bekaar','faltu','bekar','kharab','ganda','bura laga','dil dukha','dukh hua','dukhi','rona aa raha','ro raha','takleef','pareshaan','pareshan','tension','fikr','dar','dara hua','ghabra raha','gussa','bahut gussa','gussa aa raha','chilla raha','maar dunga','nafrat','nafrat hai','ghrina','ghinona','sharminda','sharm','thaka hua','haar gaya','toot gaya','akela','udaas','bahut udaas','dil nahi lag raha','mann nahi','kuch nahi','sab khatam','teri wajah se','galti','mafi','maafi maango','barbad','barbaad'];

let recognition = null;
let listening = false;
let currentLang = 'en-US';

const emotionColors = {
  Happy: '#ef4444',
  Joyful: '#dc2626',
  Excited: '#b91c1c',
  Loving: '#991b1b',
  Peaceful: '#7f1d1d',
  Grateful: '#f87171',
  Hopeful: '#fca5a5',
  Sad: '#450a0a',
  Heartbroken: '#7f1d1d',
  Angry: '#991b1b',
  Furious: '#b91c1c',
  Fearful: '#dc2626',
  Anxious: '#ef4444',
  Disgusted: '#7f1d1d',
  Disappointed: '#450a0a',
  Neutral: '#71717a',
  Uncertain: '#52525b'
};

const emotionEmojis = {
  Happy: '😊',
  Joyful: '🤩',
  Excited: '😄',
  Loving: '🥰',
  Peaceful: '😌',
  Grateful: '🙏',
  Hopeful: '🌟',
  Sad: '😢',
  Heartbroken: '😭',
  Angry: '😠',
  Furious: '😡',
  Fearful: '😨',
  Anxious: '😰',
  Disgusted: '🤢',
  Disappointed: '😞',
  Neutral: '😐',
  Uncertain: '🤔'
};

function setStatus(text) {
  recordStatus.textContent = text;
}

function updateCharCount() {
  charCount.textContent = `${inputText.value.length} / 800`;
}

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(Boolean);
}

function highlightText() {
  const text = inputText.value;
  const words = text.split(/(\s+)/);
  let html = words.map(token => {
    const clean = token.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (POSITIVE_WORDS.includes(clean) || HINGLISH_POSITIVE.includes(token.toLowerCase())) {
      return `<span class="positive">${token}</span>`;
    }
    if (NEGATIVE_WORDS.includes(clean) || HINGLISH_NEGATIVE.includes(token.toLowerCase())) {
      return `<span class="negative">${token}</span>`;
    }
    return token.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }).join('');
  highlightLayer.innerHTML = html;
}

function animateRing(percent, color) {
  const circumference = 2 * Math.PI * 52;
  const offset = circumference * (1 - percent / 100);
  ringFill.style.strokeDashoffset = offset;
  ringFill.style.stroke = color;
}

function renderBreakdown(breakdown) {
  breakdownBars.innerHTML = '';
  Object.entries(breakdown).sort((a, b) => b[1] - a[1]).forEach(([name, value]) => {
    const color = emotionColors[name] || '#94a3b8';
    const item = document.createElement('div');
    item.className = 'breakdown-item';
    item.innerHTML = `
      <span>${name} <strong>${value}%</strong></span>
      <div class="bar-shell"><div class="bar-fill" style="width: ${value}%; background: ${color};"></div></div>
    `;
    breakdownBars.appendChild(item);
  });
}

function renderHistory(items) {
  historyList.innerHTML = '';
  if (!items.length) {
    historyList.innerHTML = '<div class="history-item">No history yet.</div>';
    return;
  }
  items.forEach(item => {
    const row = document.createElement('div');
    row.className = 'history-item';
    row.innerHTML = `<strong>${item.primary} • ${item.confidence}%</strong><span>${item.text}</span>`;
    historyList.appendChild(row);
  });
}

function getHistory() {
  const raw = localStorage.getItem('sentiVoiceHistory');
  try { return raw ? JSON.parse(raw) : []; } catch { return []; }
}

function saveHistory(record) {
  const history = [record, ...getHistory()].slice(0, 5);
  localStorage.setItem('sentiVoiceHistory', JSON.stringify(history));
  renderHistory(history);
}

function updateUI(result) {
  primaryEmoji.textContent = result.emoji;
  primaryLabel.textContent = result.primary.toUpperCase();
  primaryText.textContent = `Detected ${result.primary} sentiment with ${result.confidence}% confidence.`;
  confidenceValue.textContent = `${result.confidence}%`;
  confidenceIndicator.textContent = `Confidence: ${result.confidence}%`;
  animateRing(result.confidence, result.color);
  nbValue.textContent = `${result.naive_bayes}%`;
  lstmValue.textContent = `${result.lstm}%`;
  combinedValue.textContent = `${result.combined}%`;
  renderBreakdown(result.breakdown);
  loadingState.classList.add('hidden');
  resultsArea.classList.remove('hidden');
}

async function analyzeText() {
  const text = inputText.value.trim();
  if (!text) {
    setStatus('Enter text or record your voice before analysis.');
    return;
  }
  loadingState.classList.remove('hidden');
  resultsArea.classList.add('hidden');
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const json = await response.json();
    if (response.ok) {
      updateUI(json);
      saveHistory({ text, primary: json.primary, confidence: json.confidence });
    } else {
      setStatus(json.error || 'Analysis failed.');
    }
  } catch (err) {
    setStatus('Backend unavailable.');
  }
}

function copyResult() {
  const data = `SentiVoice AI\nEmotion: ${primaryLabel.textContent} (${confidenceValue.textContent})\nText: ${inputText.value}`;
  navigator.clipboard.writeText(data).then(() => setStatus('Result copied.'));
}

function shareImage() {
  const ctx = shareCanvas.getContext('2d');
  const w = shareCanvas.width;
  const h = shareCanvas.height;
  ctx.fillStyle = '#050505';
  ctx.fillRect(0, 0, w, h);
  ctx.font = 'bold 48px Space Grotesk';
  ctx.fillStyle = '#fff';
  ctx.fillText('SentiVoice AI', 48, 80);
  ctx.font = '24px Inter';
  ctx.fillStyle = '#94a3b8';
  ctx.fillText('Dual-Model Sentiment Intelligence', 48, 120);
  ctx.font = '96px Arial';
  ctx.fillText(primaryEmoji.textContent, 48, 220);
  ctx.font = '40px Space Grotesk';
  ctx.fillText(primaryLabel.textContent, 180, 220);
  ctx.font = '28px Inter';
  ctx.fillStyle = '#ff3333';
  ctx.fillText(`Confidence: ${confidenceValue.textContent}`, 180, 260);
  ctx.fillStyle = '#fff';
  ctx.font = '24px Inter';
  const text = inputText.value.trim() || 'No text provided.';
  const preview = text.length > 260 ? text.slice(0, 260) + '...' : text;
  const lines = preview.match(/.{1,60}(\s|$)/g) || [];
  let y = 320;
  lines.forEach(line => {
    ctx.fillText(line.trim(), 48, y);
    y += 34;
  });
  shareCanvas.toBlob(blob => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'sentivoice-result.png';
    link.click();
  });
}

function initSpeech() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    recordHint.textContent = 'Speech API not supported.';
    micButton.disabled = true;
    return;
  }
  recognition = new SpeechRecognition();
  recognition.lang = currentLang;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  recognition.continuous = false;

  recognition.onstart = () => {
    listening = true;
    micButton.classList.add('active');
    setStatus('Listening...');
    waveform.classList.add('listening');
  };

  recognition.onresult = event => {
    const text = Array.from(event.results).map(r => r[0].transcript).join('');
    inputText.value = text;
    updateCharCount();
    highlightText();
    setStatus('Processing...');
  };

  recognition.onspeechend = () => stopSpeech();
  recognition.onend = () => { if (listening) stopSpeech(); };
  recognition.onerror = event => { stopSpeech(); setStatus(`Speech error: ${event.error}`); };
}

function startSpeech() {
  if (!recognition) return;
  recognition.lang = currentLang;
  try {
    recognition.start();
    recordHint.textContent = 'Auto-stops on silence';
  } catch {
    setStatus('Unable to start microphone.');
  }
}

function stopSpeech() {
  if (!recognition || !listening) return;
  recognition.stop();
  listening = false;
  micButton.classList.remove('active');
  setStatus('Done');
  waveform.classList.remove('listening');
}

inputText.addEventListener('input', () => {
  updateCharCount();
  highlightText();
});

languageToggle.addEventListener('change', () => {
  currentLang = languageToggle.checked ? 'hi-IN' : 'en-US';
  languageMode.textContent = languageToggle.checked ? 'Hinglish' : 'EN';
  setStatus(`Language set to ${languageMode.textContent}`);
});

micButton.addEventListener('click', () => {
  if (listening) {
    stopSpeech();
  } else {
    startSpeech();
  }
});

analyzeButton.addEventListener('click', analyzeText);
clearButton.addEventListener('click', () => {
  inputText.value = '';
  updateCharCount();
  highlightText();
  loadingState.classList.add('hidden');
  resultsArea.classList.add('hidden');
  setStatus('Ready to record');
});
copyButton.addEventListener('click', copyResult);
shareButton.addEventListener('click', shareImage);

updateCharCount();
highlightText();
initSpeech();
renderHistory(getHistory());

window.addEventListener('load', () => {
  if (!getHistory().length) renderHistory([]);
});

inputText.addEventListener('scroll', () => {
  highlightLayer.scrollTop = inputText.scrollTop;
});
