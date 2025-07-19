import streamlit as st
from google.cloud import translate_v2 as translate
from gtts import gTTS
import os
import base64
from datetime import datetime

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_google_credentials.json"

# Initialize Translate API client
translate_client = translate.Client()

# Supported languages with emojis
languages = {
    '🇺🇸 English': 'en',
    '🇫🇷 French': 'fr',
    '🇪🇸 Spanish': 'es',
    '🇩🇪 German': 'de',
    '🇮🇳 Hindi': 'hi',
    '🇮🇳 Telugu': 'te',
    '🇨🇳 Chinese (Simplified)': 'zh-CN',
    '🇯🇵 Japanese': 'ja'
}

# Translation history stored in session
if 'history' not in st.session_state:
    st.session_state.history = []

# 🧼 Clean UI
st.set_page_config(page_title="EchoTranslate Pro", page_icon="🌍")
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0;'>🌍EchoTranslate Pro</h1>
    <h4 style='text-align: center; color: gray; margin-top: 5px;'>Translate & listen to your text in any language.</h4>
    """,
    unsafe_allow_html=True
)

# Layout
col1, col2 = st.columns(2)
with col1:
    text_input = st.text_area("Enter text:", height=150)
with col2:
    target_lang = st.selectbox("Translate to:", list(languages.keys()))
    speak = st.checkbox("🔊 Play translation", value=True)

# Translate Button
if st.button("🚀 Translate"):
    if text_input.strip():
        lang_code = languages[target_lang]

        # Translate
        result = translate_client.translate(text_input, target_language=lang_code)
        translated_text = result['translatedText']
        detected_lang_code = result.get('detectedSourceLanguage', 'unknown')
        code_to_name = {
        'en': 'English',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'hi': 'Hindi',
        'te': 'Telugu',
        'zh-CN': 'Chinese (Simplified)',
        'ja': 'Japanese'
        }
        detected_lang_name = code_to_name.get(detected_lang_code, detected_lang_code)

        # Display translation
        st.markdown(f"#### 💬 Translated Text:\n**{translated_text}**")

        # Save to history
        st.session_state.history.append({
        'input': text_input,
        'output': translated_text,
        'lang': target_lang,
        'detected': detected_lang_name,
        'time': datetime.now().strftime("%H:%M:%S")
        })


        # Text-to-speech
        tts = gTTS(text=translated_text, lang=lang_code)
        audio_path = f"translation_{datetime.now().strftime('%H%M%S')}.mp3"
        tts.save(audio_path)

        if speak:
            audio_file = open(audio_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3")

        # Download link
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(
                f'<a href="data:audio/mp3;base64,{b64}" download="{audio_path}">⬇️ Download Audio</a>',
                unsafe_allow_html=True,
            )
    else:
        st.warning("Please enter some text.")

# 🕘 Show History
if st.session_state.history:
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'> Translation History</h3>", unsafe_allow_html=True)

    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        <div style="padding: 10px 15px; border-radius: 10px; background-color: #f4f4f4; margin-bottom: 15px;">
            <p>⏰ <code>{item['time']}</code></p>
            <p>🔤 <strong>Input ({item['detected']}):</strong> {item['input']}</p>
            <p>🌐 <strong>{item['lang']} →</strong> {item['output']}</p>
        </div>
        """, unsafe_allow_html=True)

