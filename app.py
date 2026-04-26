from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import re
import math
import os
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mock user for demonstration
USER_CREDENTIALS = {
    "admin": "password123"
}

# In-memory history storage
USER_HISTORY = {}

lexicon = {
    'Happy': ['happy', 'glad', 'pleased', 'delighted', 'cheerful', 'content', 'joyful', 'elated', 'ecstatic', 'thrilled', 'overjoyed', 'blissful', 'radiant', 'beaming', 'wonderful', 'fantastic', 'great', 'amazing', 'awesome', 'brilliant', 'superb', 'excellent', 'love', 'loved', 'beautiful', 'pretty', 'cute', 'adorable', 'good', 'nice', 'pleasant', 'super', 'best', 'fine', 'okay', 'perfect'],
    'Joyful': ['joyful', 'jubilant', 'exuberant', 'euphoric', 'exhilarated', 'rejoicing', 'gleeful', 'merry', 'jovial', 'festive', 'celebratory', 'triumphant', 'heavenly', 'magical', 'blessed'],
    'Excited': ['excited', 'thrilled', 'enthusiastic', 'eager', 'pumped', 'hyped', 'energized', 'fired up', 'stoked', 'psyched', 'animated', 'vivacious', 'energetic', 'hyper'],
    'Grateful': ['grateful', 'thankful', 'appreciative', 'blessed', 'fortunate', 'lucky', 'obliged', 'indebted', 'honored'],
    'Peaceful': ['peaceful', 'calm', 'serene', 'relaxed', 'tranquil', 'composed', 'zen', 'mindful', 'soothed', 'at ease', 'comfortable', 'satisfied', 'quiet', 'still'],
    'Hopeful': ['hopeful', 'optimistic', 'positive', 'confident', 'assured', 'encouraged', 'inspired', 'motivated', 'aspiring', 'promising'],
    'Sad': ['sad', 'unhappy', 'sorrowful', 'depressed', 'gloomy', 'miserable', 'heartbroken', 'dejected', 'downcast', 'melancholy', 'grief', 'mourning', 'crying', 'weeping', 'tears', 'upset', 'hurt', 'broken', 'lost', 'lonely', 'alone', 'abandoned', 'bad', 'awful', 'terrible', 'horrible', 'poor', 'sadly'],
    'Angry': ['angry', 'furious', 'enraged', 'irate', 'livid', 'outraged', 'infuriated', 'fuming', 'mad', 'irritated', 'annoyed', 'agitated', 'frustrated', 'resentful', 'bitter', 'hostile', 'wrathful', 'seething', 'hate', 'hated'],
    'Fearful': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'nervous', 'panicked', 'horrified', 'dreadful', 'apprehensive', 'uneasy', 'tense', 'stressed', 'overwhelmed', 'paranoid', 'fear'],
    'Disgusted': ['disgusted', 'repulsed', 'revolted', 'appalled', 'nauseated', 'horrified', 'offended', 'disturbed', 'gross', 'sick'],
    'Disappointed': ['disappointed', 'let down', 'failed', 'hopeless', 'discouraged', 'disheartened', 'defeated', 'disillusioned', 'frustrated', 'shame', 'unfortunate']
}

hinglish_lexicon = {
    'positive': [
        'mast', 'zabardast', 'bindaas', 'badhiya', 'ekdum', 'shandaar', 'kamaal', 'jabardast', 'khush', 
        'bahut acha', 'bohot acha', 'achi baat', 'maja aa gaya', 'maja aaya', 'full mast', 'ekdum badhiya', 
        'ek number', 'life set hai', 'sab theek', 'bilkul sahi', 'haan ji', 'wah wah', 'wah bhai', 
        'superb yaar', 'acha laga', 'pyaar', 'mohabbat', 'dil khush', 'dil bhar aaya', 'khushi', 
        'anand', 'sukoon', 'shanti', 'maza', 'masti', 'jiyenge', 'jai ho', 'bahut shukriya', 
        'shukriya', 'dhanyawad', 'meherbani', 'bahut badhiya', 'thoda zyada khush', 'gazab', 'kya baat hai',
        'vadiya', 'sahi hai', 'mubarak', 'tarakki', 'jeet', 'vijayi', 'safal', 'dhinchak', 'paisa wasool',
        'dil jeet liya', 'swagat', 'namaste', 'pranam', 'ashirwad', 'khushboo', 'mehak', 'chamal', 'roshan',
        'achha', 'accha', 'super', 'cool', 'awesome', 'op', 'overpowered', 'jhakaas', 'lajawab'
    ],
    'negative': [
        'bura', 'bahut bura', 'bekaar', 'faltu', 'bekar', 'kharab', 'ganda', 'bura laga', 'dil dukha', 
        'dukh hua', 'dukhi', 'rona aa raha', 'ro raha', 'takleef', 'pareshaan', 'pareshan', 'tension', 
        'fikr', 'dar', 'dara hua', 'ghabra raha', 'gussa', 'bahut gussa', 'gussa aa raha', 'chilla raha', 
        'maar dunga', 'nafrat', 'nafrat hai', 'ghrina', 'ghinona', 'sharminda', 'sharm', 'thaka hua', 
        'haar gaya', 'toot gaya', 'akela', 'udaas', 'bahut udaas', 'dil nahi lag raha', 'mann nahi', 
        'kuch nahi', 'sab khatam', 'teri wajah se', 'galti', 'mafi', 'maafi maango', 'barbad', 'barbaad',
        'bakwas', 'ghatiya', 'dhoka', 'fareb', 'chor', 'badmash', 'jungli', 'bewakoof', 'pagal', 'gadha',
        'ullu', 'lanat', 'shame', 'dhikkar', 'beizzati', 'sharam', 'rona', 'cheekh', 'chilla', 'dard',
        'peeda', 'kasht', 'vipada', 'musibat', 'pareshani', 'laachaar', 'bebas', 'majboor',
        'kharab', 'nikamma', 'nalla', 'chutiya', 'harami', 'kutta'
    ],
    'neutral': [
        'theek hai', 'chalta hai', 'koi baat nahi', 'sab same', 'pta nahi', 'dekha jayega', 'hoga kuch', 
        'acha acha', 'hmm', 'are yaar', 'suno', 'theek thak', 'bas', 'shayad', 'kuch bhi', 'kya pata',
        'thik', 'thek'
    ]
}

hinglish_intensifiers = ['bahut', 'bohot', 'kaafi', 'ekdum', 'bilkul', 'zyada', 'zyaada', 'purely', 'poora', 'paisa wasool', 'so', 'too', 'very']
hinglish_negators = ['nahi', 'nhi', 'ni', 'na', 'mat', 'nhi']

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
    text_lower = text.lower()
    category_counts = {category: 0.0 for category in lexicon}
    pos_score = 0.0
    neg_score = 0.0

    for index, token in enumerate(tokens):
        # English lexicon matching
        for category, words in lexicon.items():
            if token in words:
                category_counts[category] += 1.0 + math.log(1 + index / 6)

    # Improved Hinglish matching logic
    hinglish_to_emotion = {
        'positive': ['Happy', 'Joyful', 'Excited'],
        'negative': ['Sad', 'Angry', 'Fearful', 'Disgusted', 'Disappointed']
    }

    for group, phrases in hinglish_lexicon.items():
        for phrase in phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            matches = re.findall(pattern, text_lower)
            if matches:
                weight = 1.8 if group == 'positive' else 2.0 if group == 'negative' else 0.9
                
                phrase_start = text_lower.find(phrase)
                preceding_text = text_lower[max(0, phrase_start - 10):phrase_start]
                is_negated = any(neg in preceding_text for neg in hinglish_negators)
                is_intensified = any(intns in preceding_text for intns in hinglish_intensifiers)
                if is_intensified: weight *= 1.5

                if is_negated:
                    if group == 'positive': 
                        neg_score += weight * len(matches)
                        category_counts['Sad'] += weight
                    elif group == 'negative': 
                        pos_score += weight * len(matches)
                        category_counts['Happy'] += weight
                else:
                    if group == 'positive': 
                        pos_score += weight * len(matches)
                        # Distribute to sub-categories
                        for emo in hinglish_to_emotion['positive']:
                            category_counts[emo] += weight / 3
                    elif group == 'negative': 
                        neg_score += weight * len(matches)
                        for emo in hinglish_to_emotion['negative']:
                            category_counts[emo] += weight / 5

    pos_total = sum(category_counts[c] for c in ['Happy', 'Joyful', 'Excited', 'Grateful', 'Peaceful', 'Hopeful'])
    neg_total = sum(category_counts[c] for c in ['Sad', 'Angry', 'Fearful', 'Disgusted', 'Disappointed'])
    pos_score += pos_total
    neg_score += neg_total

    likelihood_positive = math.log(1.2 + pos_score) + math.log(0.5)
    likelihood_negative = math.log(1.2 + neg_score) + math.log(0.5)
    
    # Avoid math overflow
    diff = likelihood_negative - likelihood_positive
    
    # Increase sensitivity to polarity
    if pos_score > neg_score + 1: diff -= 0.5
    if neg_score > pos_score + 1: diff += 0.5

    if diff > 100: score = 0.0
    elif diff < -100: score = 1.0
    else: score = 1 / (1 + math.exp(diff))

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
                    # Check for negation in window
                    is_negated = any(neg in window for neg in hinglish_negators)
                    impact = 1.6 if group == 'positive' else -1.6 if group == 'negative' else 0.0
                    if is_negated: impact *= -1
                    sentiment_signal += impact

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

    # Increase sensitivity by giving higher weight to emotional keywords
    for token in tokens:
        for category, words in lexicon.items():
            if token in words:
                scores[category] += 3

    lowered = text.lower()
    for group, phrases in hinglish_lexicon.items():
        for phrase in phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, lowered):
                # Simple negation check for primary emotion
                phrase_start = lowered.find(phrase)
                is_negated = any(neg in lowered[max(0, phrase_start-10):phrase_start] for neg in hinglish_negators)
                
                if is_negated:
                    category = 'Sad' if group == 'positive' else 'Happy' if group == 'negative' else 'Neutral'
                else:
                    category = 'Happy' if group == 'positive' else 'Sad' if group == 'negative' else 'Neutral'
                scores[category] += 2

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


@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    target_lang = data.get('target_lang', 'en')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    try:
        # Map some common codes to deep-translator format
        lang_map = {
            'zh': 'zh-CN',
            'hi': 'hi',
            'en': 'en'
        }
        actual_target = lang_map.get(target_lang, target_lang)
        
        translated = GoogleTranslator(source='auto', target=actual_target).translate(text)
        print(f"Translation successful: {text[:20]}... -> {translated[:20]}...")
        return jsonify({'success': True, 'translated_text': translated})
    except Exception as e:
        print(f"Translation Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    lang_code = data.get('lang', 'en-US')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400

    analysis_text = text
    
    # Check if text contains Devanagari (Hindi script)
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    
    # If it's pure Hindi script OR not English/Hinglish, translate for analysis
    if has_devanagari or not (lang_code.startswith('en') or lang_code == 'hi-IN'):
        try:
            # Always translate to English for the most accurate sentiment match
            analysis_text = GoogleTranslator(source='auto', target='en').translate(text)
        except Exception as e:
            print(f"Analysis Translation Failed: {e}")
            pass 

    nb_result = analyze_naive_bayes(analysis_text)
    lstm_score = analyze_lstm(analysis_text)
    combined_score = nb_result['score'] * 0.6 + lstm_score * 0.4
    confidence = round(min(99, max(10, combined_score * 100 * 0.97)))
    
    # Get breakdown
    breakdown_raw = build_breakdown(nb_result['categories'])
    
    # Get the emotion with the absolute highest score in the breakdown
    primary = max(breakdown_raw.items(), key=lambda x: x[1])[0]
    
    # Ensure it's not neutral if others have significant scores
    if primary == 'Neutral':
        others = {k: v for k, v in breakdown_raw.items() if k != 'Neutral'}
        if others:
            strongest_other = max(others.items(), key=lambda x: x[1])
            if strongest_other[1] > 0.08:
                primary = strongest_other[0]

    emotion = emotion_meta.get(primary, emotion_meta['Neutral'])

    result_data = {
        'naive_bayes': round(nb_result['score'] * 100),
        'lstm': round(lstm_score * 100),
        'combined': round(combined_score * 100),
        'confidence': confidence,
        'primary': primary,
        'emoji': emotion['emoji'],
        'color': emotion['color'],
        'primary_text': f"Strong {primary} signals detected ({round(breakdown_raw[primary]*100)}% match).",
        'breakdown': {k: round(v * 100) for k, v in breakdown_raw.items()}
    }

    # Save to backend history
    if 'user' in session:
        user = session['user']
        if user not in USER_HISTORY:
            USER_HISTORY[user] = []
        USER_HISTORY[user].insert(0, {
            'text': text,
            'primary': primary,
            'confidence': confidence,
            'timestamp': None # Could add real timestamp if needed
        })
        USER_HISTORY[user] = USER_HISTORY[user][:5] # Keep last 5

    return jsonify(result_data)


@app.route('/api/history')
def get_backend_history():
    if 'user' not in session:
        return jsonify([])
    
    user = session['user']
    return jsonify(USER_HISTORY.get(user, []))


@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    if user in USER_HISTORY:
        USER_HISTORY[user] = []
    
    return jsonify({'success': True, 'message': 'History cleared from backend'})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

