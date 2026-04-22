from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import re
import math
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mock user for demonstration
USER_CREDENTIALS = {
    "admin": "password123"
}

lexicon = {
    'Happy': ['happy', 'glad', 'pleased', 'delighted', 'cheerful', 'content', 'joyful', 'elated', 'ecstatic', 'thrilled', 'overjoyed', 'blissful', 'radiant', 'beaming', 'wonderful', 'fantastic', 'great', 'amazing', 'awesome', 'brilliant', 'superb', 'excellent', 'love', 'loved', 'beautiful', 'pretty', 'cute', 'adorable'],
    'Joyful': ['joyful', 'jubilant', 'exuberant', 'euphoric', 'exhilarated', 'rejoicing', 'gleeful', 'merry', 'jovial', 'festive', 'celebratory', 'triumphant'],
    'Excited': ['excited', 'thrilled', 'enthusiastic', 'eager', 'pumped', 'hyped', 'energized', 'fired up', 'stoked', 'psyched', 'animated', 'vivacious'],
    'Grateful': ['grateful', 'thankful', 'appreciative', 'blessed', 'fortunate', 'lucky', 'obliged', 'indebted'],
    'Peaceful': ['peaceful', 'calm', 'serene', 'relaxed', 'tranquil', 'composed', 'zen', 'mindful', 'soothed', 'at ease', 'comfortable', 'satisfied'],
    'Hopeful': ['hopeful', 'optimistic', 'positive', 'confident', 'assured', 'encouraged', 'inspired', 'motivated', 'aspiring'],
    'Sad': ['sad', 'unhappy', 'sorrowful', 'depressed', 'gloomy', 'miserable', 'heartbroken', 'dejected', 'downcast', 'melancholy', 'grief', 'mourning', 'crying', 'weeping', 'tears', 'upset', 'hurt', 'broken', 'lost', 'lonely', 'alone', 'abandoned'],
    'Angry': ['angry', 'furious', 'enraged', 'irate', 'livid', 'outraged', 'infuriated', 'fuming', 'mad', 'irritated', 'annoyed', 'agitated', 'frustrated', 'resentful', 'bitter', 'hostile', 'wrathful', 'seething'],
    'Fearful': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'nervous', 'panicked', 'horrified', 'dreadful', 'apprehensive', 'uneasy', 'tense', 'stressed', 'overwhelmed', 'paranoid'],
    'Disgusted': ['disgusted', 'repulsed', 'revolted', 'appalled', 'nauseated', 'horrified', 'offended', 'disturbed'],
    'Disappointed': ['disappointed', 'let down', 'failed', 'hopeless', 'discouraged', 'disheartened', 'defeated', 'disillusioned', 'frustrated']
}

hinglish_lexicon = {
    'positive': ['mast', 'zabardast', 'bindaas', 'badhiya', 'ekdum', 'shandaar', 'kamaal', 'jabardast', 'khush', 'bahut acha', 'bohot acha', 'achi baat', 'maja aa gaya', 'maja aaya', 'full mast', 'ekdum badhiya', 'ek number', 'life set hai', 'sab theek', 'bilkul sahi', 'haan ji', 'wah wah', 'wah bhai', 'superb yaar', 'acha laga', 'pyaar', 'mohabbat', 'dil khush', 'dil bhar aaya', 'khushi', 'anand', 'sukoon', 'shanti', 'maza', 'masti', 'jiyenge', 'jai ho', 'bahut shukriya', 'shukriya', 'dhanyawad', 'meherbani', 'bahut badhiya', 'thoda zyada khush'],
    'negative': ['bura', 'bahut bura', 'bekaar', 'faltu', 'bekar', 'kharab', 'ganda', 'bura laga', 'dil dukha', 'dukh hua', 'dukhi', 'rona aa raha', 'ro raha', 'takleef', 'pareshaan', 'pareshan', 'tension', 'fikr', 'dar', 'dara hua', 'ghabra raha', 'gussa', 'bahut gussa', 'gussa aa raha', 'chilla raha', 'maar dunga', 'nafrat', 'nafrat hai', 'ghrina', 'ghinona', 'sharminda', 'sharm', 'thaka hua', 'haar gaya', 'toot gaya', 'akela', 'udaas', 'bahut udaas', 'dil nahi lag raha', 'mann nahi', 'kuch nahi', 'sab khatam', 'teri wajah se', 'galti', 'mafi', 'maafi maango', 'barbad', 'barbaad'],
    'neutral': ['theek hai', 'chalta hai', 'koi baat nahi', 'sab same', 'pta nahi', 'dekha jayega', 'hoga kuch', 'acha acha', 'hmm', 'are yaar', 'suno']
}

negation_patterns = ['not happy', 'not good', 'not well', 'not great', 'not sad', 'nahi khush', 'bilkul nahi', 'nahi acha', 'nahi theek', 'nahi chalta']
intensity_modifiers = ['very', 'extremely', 'really', 'super', 'truly', 'completely', 'absolutely', 'bahut', 'ekdum', 'zyada', 'zyaada', 'bohot']

emotion_meta = {
    'Happy': {'emoji': '😊', 'color': '#ef4444'},
    'Joyful': {'emoji': '🤩', 'color': '#dc2626'},
    'Excited': {'emoji': '😄', 'color': '#b91c1c'},
    'Loving': {'emoji': '🥰', 'color': '#991b1b'},
    'Peaceful': {'emoji': '😌', 'color': '#7f1d1d'},
    'Grateful': {'emoji': '🙏', 'color': '#f87171'},
    'Hopeful': {'emoji': '🌟', 'color': '#fca5a5'},
    'Sad': {'emoji': '😢', 'color': '#450a0a'},
    'Heartbroken': {'emoji': '😭', 'color': '#7f1d1d'},
    'Angry': {'emoji': '😠', 'color': '#991b1b'},
    'Furious': {'emoji': '😡', 'color': '#b91c1c'},
    'Fearful': {'emoji': '😨', 'color': '#dc2626'},
    'Anxious': {'emoji': '😰', 'color': '#ef4444'},
    'Disgusted': {'emoji': '🤢', 'color': '#7f1d1d'},
    'Disappointed': {'emoji': '😞', 'color': '#450a0a'},
    'Neutral': {'emoji': '😐', 'color': '#71717a'},
    'Uncertain': {'emoji': '🤔', 'color': '#52525b'}
}


def tokenize(text):
    normalized = re.sub(r'[^a-z0-9\s\u0900-\u097F]+', ' ', text.lower())
    return [token for token in normalized.split() if token]


def analyze_naive_bayes(text):
    tokens = tokenize(text)
    category_counts = {category: 0.0 for category in lexicon}
    pos_score = 0.0
    neg_score = 0.0

    for index, token in enumerate(tokens):
        for category, words in lexicon.items():
            if token in words:
                category_counts[category] += 1.0 + math.log(1 + index / 6)

    for group, phrases in hinglish_lexicon.items():
        for phrase in phrases:
            if phrase in text.lower():
                weight = 1.3 if group == 'positive' else 1.4 if group == 'negative' else 0.9
                if group == 'positive':
                    pos_score += weight * 2
                elif group == 'negative':
                    neg_score += weight * 2

    pos_total = sum(category_counts[c] for c in ['Happy', 'Joyful', 'Excited', 'Grateful', 'Peaceful', 'Hopeful'])
    neg_total = sum(category_counts[c] for c in ['Sad', 'Angry', 'Fearful', 'Disgusted', 'Disappointed'])
    pos_score += pos_total
    neg_score += neg_total

    likelihood_positive = math.log(1 + pos_score) + math.log(0.5)
    likelihood_negative = math.log(1 + neg_score) + math.log(0.5)
    score = 1 / (1 + math.exp(likelihood_negative - likelihood_positive))

    categories = {**category_counts, 'Positive': pos_total, 'Negative': neg_total}
    return {'score': score, 'categories': categories, 'positive': pos_score, 'negative': neg_score}


def analyze_lstm(text):
    tokens = tokenize(text)
    sequence_score = 0.0
    count = 0

    for i in range(len(tokens)):
        window_tokens = tokens[i:i + 3]
        window = ' '.join(window_tokens)
        if not window_tokens:
            continue

        window_score = 0.0
        sentiment_signal = 0.0

        for phrase in negation_patterns:
            if phrase in window:
                sentiment_signal -= 2.0

        for modifier in intensity_modifiers:
            if modifier in window_tokens:
                window_score += 0.6

        for token in window_tokens:
            for category, words in lexicon.items():
                if token in words:
                    sentiment_signal += -1.1 if category in ['Sad', 'Angry', 'Fearful', 'Disgusted', 'Disappointed'] else 1.1

        for group, phrases in hinglish_lexicon.items():
            for phrase in phrases:
                if phrase in window:
                    sentiment_signal += 1.2 if group == 'positive' else -1.2 if group == 'negative' else 0.0

        if sentiment_signal != 0:
            window_score += sentiment_signal
            sequence_score += window_score
            count += 1

    if count == 0:
        neutral_ratio = min(1.0, len(tokens) / 10.0)
        return 0.5 + (neutral_ratio - 0.5) * 0.15

    normalized = 1 / (1 + math.exp(-sequence_score / count))
    return normalized


def get_primary_emotion(text):
    tokens = tokenize(text)
    scores = {category: 0 for category in lexicon}

    for token in tokens:
        for category, words in lexicon.items():
            if token in words:
                scores[category] += 1

    lowered = text.lower()
    for group, phrases in hinglish_lexicon.items():
        for phrase in phrases:
            if phrase in lowered:
                category = 'Happy' if group == 'positive' else 'Sad' if group == 'negative' else 'Neutral'
                scores[category] += 1

    best = max(scores.items(), key=lambda item: item[1])
    if best[1] == 0:
        return 'Neutral'
    category = best[0]
    if category == 'Sad' and 'heartbroken' in lowered:
        return 'Heartbroken'
    if category == 'Angry' and 'furious' in lowered:
        return 'Furious'
    if category == 'Fearful' and any(word in lowered for word in ['anxious', 'worried']):
        return 'Anxious'
    return category


def build_breakdown(categories):
    normalized = {}
    for name, value in categories.items():
        if name in ['Positive', 'Negative']:
            continue
        normalized[name] = min(1.0, value * 0.18 + 0.05)
    normalized['Neutral'] = 0.08
    return normalized


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if USER_CREDENTIALS.get(username) == password:
            session['user'] = username
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('index')})
            return redirect(url_for('index'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    if username in USER_CREDENTIALS:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    USER_CREDENTIALS[username] = password
    return jsonify({'success': True, 'message': 'Registration successful! You can now login.'})



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text required'}), 400

    nb_result = analyze_naive_bayes(text)
    lstm_score = analyze_lstm(text)
    combined_score = nb_result['score'] * 0.6 + lstm_score * 0.4
    confidence = round(min(99, max(10, combined_score * 100 * 0.97)))
    primary = get_primary_emotion(text)
    breakdown = build_breakdown(nb_result['categories'])
    emotion = emotion_meta.get(primary, emotion_meta['Neutral'])

    return jsonify({
        'naive_bayes': round(nb_result['score'] * 100),
        'lstm': round(lstm_score * 100),
        'combined': round(combined_score * 100),
        'confidence': confidence,
        'primary': primary,
        'emoji': emotion['emoji'],
        'color': emotion['color'],
        'breakdown': {k: round(v * 100) for k, v in breakdown.items()}
    })


if __name__ == '__main__':
    app.run(debug=True)
