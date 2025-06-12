import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests
import google.generativeai as genai
from PIL import Image
import io
import base64
import asyncio
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from src.models.gemini_handler import GeminiHandler
from src.utils.config import (
    ERROR_MESSAGES,
    STYLE_MAPPINGS,
    PERSONA_CARDS,
    PERSONA_IMAGE_PROMPTS
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize Gemini handler
gemini_handler = GeminiHandler(os.getenv("GEMINI_API_KEY"))

# Map persona names to their photo files
photo_mapping = {
    # Original personas
    "Hatice Teyze": "hatice_teyze.jpg",
    "Kenan Bey": "kenan_bey.jpg",
    "Tuğrul Bey": "tugrul_bey.jpg",
    "Elif": "elif.jpg",
    
    # Persona types
    "Geleneksel Muhafazakar Çekirdek": "hatice_teyze.jpg",  # Using Hatice Teyze's photo
    "Geleneksel Muhafazakar": "hatice_teyze.jpg",  # Using Hatice Teyze's photo
    "Genç Modern": "elif.jpg",  # Using Elif's photo
    "Kentsel Aydın": "tugrul_bey.jpg",  # Using Tuğrul Bey's photo
    "Kırsal Kökler": "kenan_bey.jpg"  # Using Kenan Bey's photo
}
default_photo = "persona_profil_fotoğrafları/default.jpg"

def text_to_speech(text, persona_name, lang='tr'):
    """Convert text to speech using gTTS"""
    try:
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Initialize gTTS with Turkish language and faster speed
            tts = gTTS(text=text, lang=lang, slow=False)
            # Save the audio to the temporary file
            tts.save(temp_file.name)
            return temp_file.name
    except Exception as e:
        st.error(f"gTTS hatası: {str(e)}")
        return None

def speech_to_text():
    """Convert speech to text using microphone input"""
    try:
        with sr.Microphone() as source:
            st.info("Dinleniyor... Konuşmaya başlayabilirsiniz.")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="tr-TR")
            return text
    except sr.UnknownValueError:
        st.error("Ses anlaşılamadı")
        return None
    except sr.RequestError as e:
        st.error(f"Google Speech Recognition servisi hatası: {e}")
        return None

# Page config
st.set_page_config(
    page_title="Türk Seçmen Personaları",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode
st.markdown("""
<style>
    /* Global Styles */
    body {
        color: #f1f1f1;
        background-color: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0a0a0a;
    }
    .css-1d391kg {
        background-color: #0a0a0a;
    }
    .css-1y4pm5y {
        background-color: #1a1a1a;
    }

    /* Button Styles */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 8px 4px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }

    /* Input Styles */
    .stSelectbox, .stRadio, .stTextInput, .stTextArea {
        background-color: #1a1a1a;
        color: #f1f1f1;
        border-radius: 12px;
        border: 1px solid #333;
        padding: 8px;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a;
    }
    .stSelectbox div[data-baseweb="select"] input {
        color: #f1f1f1;
    }

    /* Card Styles */
    .persona-card {
        background-color: #1a1a1a;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 1px solid #333;
    }
    .persona-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.3);
    }
    .persona-card h3 {
        color: #f1f1f1;
        text-align: center;
        margin-bottom: 16px;
        font-size: 1.5em;
        font-weight: 600;
    }
    .persona-card .subtitle {
        color: #bbb;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.1em;
    }

    /* Metric Card Styles */
    .metric-card {
        background-color: #1a1a1a;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        text-align: center;
        color: #f1f1f1;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 1px solid #333;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .metric-card .value {
        font-size: 2em;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 8px;
    }
    .metric-card .label {
        font-size: 1em;
        color: #ccc;
    }

    /* Profile Container Styles */
    .profile-container {
        text-align: center;
        margin: 24px 0;
        padding: 24px;
        background-color: #1a1a1a;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        border: 1px solid #333;
        transition: all 0.3s ease;
    }
    .profile-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.3);
    }
    .profile-image {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4CAF50;
        margin: 0 auto;
        display: block;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .profile-image:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    .profile-name {
        color: #f1f1f1;
        font-size: 1.6em;
        margin-top: 20px;
        font-weight: 600;
    }
    .profile-bio {
        color: #ccc;
        font-size: 1.1em;
        margin-top: 12px;
        padding: 0 24px;
        line-height: 1.6;
    }

    /* Chat Styles */
    .stChatMessage {
        border-radius: 20px;
        padding: 16px 20px;
        margin-bottom: 16px;
        max-width: 80%;
        position: relative;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stChatMessage.user {
        background-color: #4CAF50;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    .stChatMessage.assistant {
        background-color: #1a1a1a;
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #333;
    }

    /* Section Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f1f1;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* List Styles */
    ul, ol {
        padding-left: 24px;
    }
    li {
        margin-bottom: 8px;
        line-height: 1.6;
    }

    /* Tag Styles */
    .tag {
        background-color: #333;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        display: inline-block;
        font-size: 0.9em;
        transition: all 0.3s ease;
    }
    .tag:hover {
        background-color: #4CAF50;
        transform: translateY(-2px);
    }

    /* Chart Styles */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title
    st.title("Türk Toplumu Seçmen Personaları")
    st.markdown("Kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili")

    # Sidebar with enhanced filters
    st.sidebar.title("Filtreler ve Analizler")

    # Persona selection
    selected_persona = st.sidebar.selectbox(
        "Persona Seçin",
        list(PERSONA_CARDS.keys()),
        key="sidebar_persona_select"
    )

    # Analysis type selection
    analysis_type = st.sidebar.radio(
        "Analiz Türü",
        ["Genel Bakış", "Detaylı Analiz", "Karşılaştırma"],
        key="analysis_type_radio"
    )

    # Module selection under analysis type
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Modül Seçimi")
    selected_menu = st.sidebar.radio(
        "Modül Seçin",
        ["PersonaGPT", "Analizler", "Persona Kartları"],
        key="menu_radio"
    )

    if selected_menu == "PersonaGPT":
        st.title("PersonaGPT")
        st.markdown("### Persona ile Sohbet")

        # Create two columns for layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Persona selection with modern styling
            st.markdown("""
            <div style="background-color: #2b2b2b; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center;">
                <h3 style="color: #f1f1f1; margin-top: 0;">Persona Seçin</h3>
            """, unsafe_allow_html=True)
            
            persona_choice = st.selectbox(
                "",
                list(PERSONA_CARDS.keys()),
                key="personagpt_persona_select"
            )
            persona = PERSONA_CARDS[persona_choice]
            
            # Display profile photo and name in Instagram style
            photo_file = photo_mapping.get(persona_choice)
            if photo_file and os.path.exists(f"persona_profil_fotoğrafları/{photo_file}"):
                photo_path = f"persona_profil_fotoğrafları/{photo_file}"
                img_data = base64.b64encode(open(photo_path, 'rb').read()).decode()
                st.markdown(f"""
                <div class="profile-container">
                    <img src="data:image/png;base64,{img_data}" class="profile-image">
                    <div class="profile-name">{persona['name']}</div>
                    <div class="profile-bio">{persona['bio'][0]}</div>
                </div>
                """, unsafe_allow_html=True)
            elif os.path.exists(default_photo):
                photo_path = default_photo
                img_data = base64.b64encode(open(default_photo, 'rb').read()).decode()
                st.markdown(f"""
                <div class="profile-container">
                    <img src="data:image/png;base64,{img_data}" class="profile-image">
                    <div class="profile-name">{persona['name']}</div>
                    <div class="profile-bio">{persona['bio'][0]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Profil fotoğrafı bulunamadı.")
                
            # Display persona bio with modern card design
            st.markdown("""
            <style>
                .basic-info-container {
                    background-color: #2b2b2b;
                    padding: 20px;
                    border-radius: 15px;
                    margin: 20px 0;
                    border: 1px solid #4CAF50;
                }
                .basic-info-title {
                    color: #f1f1f1;
                    text-align: center;
                    margin-bottom: 15px;
                    font-size: 1.2em;
                    font-weight: bold;
                }
                .basic-info-content {
                    color: #ccc;
                    line-height: 1.6;
                    text-align: left;
                    padding: 0 20px;
                }
                .chat-input-container {
                    background-color: #2b2b2b;
                    padding: 15px;
                    border-radius: 15px;
                    margin: 20px auto;
                    border: 1px solid #4CAF50;
                    max-width: 600px;
                    width: 100%;
                    text-align: center;
                }
                .stChatInput {
                    background-color: #333 !important;
                    border-radius: 25px !important;
                    padding: 12px 15px !important;
                    border: 1px solid #4CAF50 !important;
                    color: white !important;
                    font-size: 1em !important;
                    width: 70% !important;
                    margin: 0 auto !important;
                }
            </style>
            <div class="basic-info-container">
                <div class="basic-info-title">Temel Bilgiler</div>
                <div class="basic-info-content">
            """, unsafe_allow_html=True)
            for bio in persona['bio']:
                st.markdown(f"• {bio}")
            st.markdown("</div></div>", unsafe_allow_html=True)

        with col2:
            # Chat interface with modern styling
            st.markdown("""
            <div style="background-color: #2b2b2b; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
                <h3 style="color: #f1f1f1; margin-top: 0; text-align: center;">Sohbet</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Display chat history with modern styling
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat type selection with modern styling
            st.markdown("""
            <style>
                .chat-type-container {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin: 30px 0;
                }
                .chat-type-button {
                    background-color: #2b2b2b;
                    color: white;
                    border: 2px solid #4CAF50;
                    padding: 20px 40px;
                    border-radius: 15px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 500;
                    font-size: 1.2em;
                    min-width: 200px;
                    text-align: center;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                .chat-type-button:hover {
                    background-color: #4CAF50;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
                }
                .chat-type-button.active {
                    background-color: #4CAF50;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
                }
                .chat-type-icon {
                    font-size: 1.5em;
                    margin-bottom: 10px;
                    display: block;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Chat type buttons
            col1, col2 = st.columns(2)
            with col1:
                text_chat = st.button("✍️ Yazılı Sohbet", key="text_chat_button", use_container_width=True)
            with col2:
                voice_chat = st.button("🎤 Sesli Sohbet", key="voice_chat_button", use_container_width=True)
            
            # Set chat type based on button clicks
            if text_chat:
                st.session_state.chat_type = "text"
            elif voice_chat:
                st.session_state.chat_type = "voice"
            
            # Initialize chat type if not set
            if "chat_type" not in st.session_state:
                st.session_state.chat_type = "text"
            
            if st.session_state.chat_type == "text":
                # Text chat input with modern styling
                st.markdown("""
                <div class="chat-input-container">
                """, unsafe_allow_html=True)
                
                if prompt := st.chat_input("Mesajınızı yazın...", key="chat_input"):
                    # Add user message to chat history
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    
                    # Generate persona response using Gemini Flash
                    persona_prompt = f"""
                    Sen {persona['name']} olarak konuşuyorsun. Aşağıdaki özelliklere sahipsin:
                    Temel Bilgiler:
                    {', '.join(persona['bio'])}
                    Geçmiş ve Değerler:
                    {', '.join(persona['lore'])}
                    Bilgi ve Görüşler:
                    {', '.join(persona['knowledge'])}
                    Sohbet Tarzı:
                    {', '.join(persona['style']['chat'])}
                    Lütfen bu özelliklere uygun şekilde yanıt ver. Kendi karakterine uygun bir dille konuş.
                    Yanıtını tek bir bütün halinde ver, maddeler halinde değil.
                    """
                    response = gemini_handler.generate_text(persona_prompt + "\n\nKullanıcı: " + prompt)

                    # Add assistant message to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

                    # Display assistant message
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    
                    # Voice response option with modern styling
                    st.markdown("""
                    <div style="text-align: center; margin: 20px 0;">
                    """, unsafe_allow_html=True)
                    if st.button("🎤 Sesli Yanıt", key="voice_response_button", help="Yanıtı sesli olarak dinle"):
                        audio_file = text_to_speech(response, persona_choice)
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
                            os.unlink(audio_file)  # Delete temporary file
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:  # Voice chat
                st.markdown("""
                <div style="background-color: #2b2b2b; padding: 20px; border-radius: 15px; margin: 20px 0; text-align: center;">
                    <h4 style="color: #f1f1f1; margin-top: 0;">Sesli Sohbet</h4>
                    <p style="color: #ccc; margin-bottom: 20px;">Konuşmak için butona basılı tutun</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎤 Konuşmak için basılı tutun", key="voice_input_button", use_container_width=True):
                    user_input = speech_to_text()
                    if user_input:
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        with st.chat_message("user"):
                            st.markdown(user_input)

                        # Generate persona response using Gemini Flash
                        persona_prompt = f"""
                        Sen {persona['name']} olarak konuşuyorsun. Aşağıdaki özelliklere sahipsin:
                        Temel Bilgiler:
                        {', '.join(persona['bio'])}
                        Geçmiş ve Değerler:
                        {', '.join(persona['lore'])}
                        Bilgi ve Görüşler:
                        {', '.join(persona['knowledge'])}
                        Sohbet Tarzı:
                        {', '.join(persona['style']['chat'])}
                        Lütfen bu özelliklere uygun şekilde yanıt ver. Kendi karakterine uygun bir dille konuş.
                        Yanıtını tek bir bütün halinde ver, maddeler halinde değil.
                        """
                        response = gemini_handler.generate_text(persona_prompt + "\n\nKullanıcı: " + user_input)

                        # Add assistant message to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})

                        # Display assistant message
                        with st.chat_message("assistant"):
                            st.markdown(response)

                        # Convert response to speech
                        audio_file = text_to_speech(response, persona_choice)
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
                            os.unlink(audio_file)  # Delete temporary file

    elif selected_menu == "Analizler":
        # Main content
        if analysis_type == "Genel Bakış":
            col1, col2 = st.columns([2, 1])
            with col1:
                # Selected persona details
                persona = PERSONA_CARDS[selected_persona]
                
                # Display profile photo
                photo_file = photo_mapping.get(selected_persona)
                if photo_file and os.path.exists(f"persona_profil_fotoğrafları/{photo_file}"):
                    photo_path = f"persona_profil_fotoğrafları/{photo_file}"
                    img_data = base64.b64encode(open(photo_path, 'rb').read()).decode()
                    st.markdown(f"""
                    <div class="profile-container">
                        <img src="data:image/png;base64,{img_data}" class="profile-image">
                        <div class="profile-name">{persona['name']}</div>
                        <div class="profile-bio">{persona['bio'][0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif os.path.exists(default_photo):
                    photo_path = default_photo
                    img_data = base64.b64encode(open(default_photo, 'rb').read()).decode()
                    st.markdown(f"""
                    <div class="profile-container">
                        <img src="data:image/png;base64,{img_data}" class="profile-image">
                        <div class="profile-name">{persona['name']}</div>
                        <div class="profile-bio">{persona['bio'][0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Profil fotoğrafı bulunamadı.")

                st.markdown(f"""
                <div class="persona-card">
                    <h3>{selected_persona}</h3>
                    <div class="subtitle">{persona['name']}</div>
                    <p style="color: #ccc; text-align: center;">{', '.join(persona['bio'])}</p>
                    <div style="text-align: center;">
                        {''.join([f'<span style="background-color: #555; color: white; padding: 5px 10px; border-radius: 5px; margin: 2px; display: inline-block; font-size: 0.8em;">{tag}</span>' for tag in persona['adjectives']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # Metrics visualization
                metrics_df = pd.DataFrame({
                    'Metrik': ['Sosyal Medya Kullanımı', 'Politik İlgi', 'Ekonomik Endişe', 'Kültürel Değerler'],
                    'Değer': [len(persona['clients']), len(persona['topics']), len(persona['knowledge']), len(persona['lore'])]
                })
                fig = px.bar(metrics_df, x='Metrik', y='Değer',
                             color_discrete_sequence=['#4CAF50'],
                             template='plotly_dark')
                fig.update_layout(
                    title="Metrikler",
                    showlegend=False,
                    plot_bgcolor='#18191a',
                    paper_bgcolor='#18191a',
                    font=dict(color='#f1f1f1')
                )
                st.plotly_chart(fig, use_container_width=True)

            # Trend analysis
            st.markdown("### Trend Analizi")
            trends = {
                'Sosyal Medya': len(persona['clients']),
                'Politik İlgi': len(persona['topics']),
                'Ekonomik Endişe': len(persona['knowledge']),
                'Kültürel Değerler': len(persona['lore'])
            }
            trends_df = pd.DataFrame({
                'Kategori': list(trends.keys()),
                'Değişim': list(trends.values())
            })
            fig = px.line(trends_df, x='Kategori', y='Değişim',
                          markers=True, color_discrete_sequence=['#4CAF50'],
                          template='plotly_dark')
            fig.update_layout(
                title="Trend Analizi",
                showlegend=False,
                plot_bgcolor='#18191a',
                paper_bgcolor='#18191a',
                font=dict(color='#f1f1f1')
            )
            st.plotly_chart(fig, use_container_width=True)

        elif analysis_type == "Detaylı Analiz":
            persona = PERSONA_CARDS[selected_persona]
            # Metrics cards with enhanced styling
            metrics = {
                'Sosyal Medya': len(persona['clients']),
                'Politik İlgi': len(persona['topics']),
                'Ekonomik Endişe': len(persona['knowledge']),
                'Kültürel Değerler': len(persona['lore'])
            }
            num_metrics = len(metrics)
            num_cols = 2
            num_rows = (num_metrics + num_cols - 1) // num_cols  # Ceiling division
            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < num_metrics:
                        metric, value = list(metrics.items())[idx]
                        with cols[col]:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="value">{value}</div>
                                <div class="label">{metric}</div>
                            </div>
                            """, unsafe_allow_html=True)

            # Detailed stats with enhanced visualization
            st.markdown("### Temel Bilgiler")
            for bio in persona['bio']:
                st.markdown(f"- {bio}")

            # Key issues
            st.markdown("### Öncelikli Konular")
            for topic in persona['topics']:
                st.markdown(f"- {topic}")

            # Enhanced radar chart for metrics
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=list(metrics.values()),
                theta=list(metrics.keys()),
                fill='toself',
                name=selected_persona,
                line=dict(color='#4CAF50')
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(metrics.values())],
                        gridcolor='#444',
                        linecolor='#888',
                        tickfont_color='#f1f1f1',
                    ),
                    bgcolor='#18191a',
                ),
                showlegend=False,
                title="Metrikler Radar Grafiği",
                paper_bgcolor='#18191a',
                font=dict(color='#f1f1f1')
            )
            st.plotly_chart(fig, use_container_width=True)

        else:  # Comparison
            st.markdown("### Personalar Karşılaştırması")
            # Select personas to compare
            compare_personas = st.multiselect(
                "Karşılaştırılacak Personalar",
                list(PERSONA_CARDS.keys()),
                default=[selected_persona]
            )
            if len(compare_personas) > 0:
                # Metrics comparison
                metrics_comparison = pd.DataFrame({
                    persona: {
                        'Sosyal Medya': len(PERSONA_CARDS[persona]['clients']),
                        'Politik İlgi': len(PERSONA_CARDS[persona]['topics']),
                        'Ekonomik Endişe': len(PERSONA_CARDS[persona]['knowledge']),
                        'Kültürel Değerler': len(PERSONA_CARDS[persona]['lore'])
                    }
                    for persona in compare_personas
                })
                st.markdown("#### Metrik Karşılaştırması")
                st.dataframe(metrics_comparison, use_container_width=True)

                # Comparison chart
                fig = go.Figure()
                max_value = 0
                for persona in compare_personas:
                    metrics = {
                        'Sosyal Medya': len(PERSONA_CARDS[persona]['clients']),
                        'Politik İlgi': len(PERSONA_CARDS[persona]['topics']),
                        'Ekonomik Endişe': len(PERSONA_CARDS[persona]['knowledge']),
                        'Kültürel Değerler': len(PERSONA_CARDS[persona]['lore'])
                    }
                    max_value = max(max_value, max(metrics.values()))
                    fig.add_trace(go.Scatterpolar(
                        r=list(metrics.values()),
                        theta=list(metrics.keys()),
                        fill='toself',
                        name=persona
                    ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max_value],
                            gridcolor='#444',
                            linecolor='#888',
                            tickfont_color='#f1f1f1',
                        ),
                        bgcolor='#18191a',
                    ),
                    showlegend=True,
                    title="Metrikler Karşılaştırma Grafiği",
                    paper_bgcolor='#18191a',
                    font=dict(color='#f1f1f1')
                )
                st.plotly_chart(fig, use_container_width=True)

        # Footer
        st.markdown("---")
        st.markdown("Bu analiz, kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili üzerine yapılmıştır.")

    elif selected_menu == "Persona Kartları":
        st.title("Persona Kartları")

        # Persona selection
        persona_choice = st.selectbox(
            "Persona Seçin",
            list(PERSONA_CARDS.keys()),
            key="persona_cards_select"
        )
        persona = PERSONA_CARDS[persona_choice]

        # Create two columns for layout
        col1, col2 = st.columns([1, 2])
        with col1:
            # Display persona profile photo
            photo_file = photo_mapping.get(persona_choice)
            if photo_file and os.path.exists(f"persona_profil_fotoğrafları/{photo_file}"):
                photo_path = f"persona_profil_fotoğrafları/{photo_file}"
                img_data = base64.b64encode(open(photo_path, 'rb').read()).decode()
                st.markdown(f"""
                <div class="profile-container">
                    <img src="data:image/png;base64,{img_data}" class="profile-image">
                    <div class="profile-name">{persona['name']}</div>
                    <div class="profile-bio">{persona['bio'][0]}</div>
                </div>
                """, unsafe_allow_html=True)
            elif os.path.exists(default_photo):
                photo_path = default_photo
                img_data = base64.b64encode(open(default_photo, 'rb').read()).decode()
                st.markdown(f"""
                <div class="profile-container">
                    <img src="data:image/png;base64,{img_data}" class="profile-image">
                    <div class="profile-name">{persona['name']}</div>
                    <div class="profile-bio">{persona['bio'][0]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Profil fotoğrafı bulunamadı.")

            # Analysis type selection
            analysis_type = st.radio(
                "Analiz Türü",
                ["Genel Bakış", "Detaylı Analiz", "Karşılaştırma"],
                key="persona_cards_analysis_type"
            )

            if analysis_type == "Detaylı Analiz":
                # Metrics cards with enhanced styling
                metrics = {
                    'Sosyal Medya': len(persona['clients']),
                    'Politik İlgi': len(persona['topics']),
                    'Ekonomik Endişe': len(persona['knowledge']),
                    'Kültürel Değerler': len(persona['lore'])
                }
                num_metrics = len(metrics)
                num_cols = 2
                num_rows = (num_metrics + num_cols - 1) // num_cols
                for row in range(num_rows):
                    cols = st.columns(num_cols)
                    for col in range(num_cols):
                        idx = row * num_cols + col
                        if idx < num_metrics:
                            metric, value = list(metrics.items())[idx]
                            with cols[col]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="value">{value}</div>
                                    <div class="label">{metric}</div>
                                </div>
                                """, unsafe_allow_html=True)

                # Enhanced radar chart for metrics
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=list(metrics.values()),
                    theta=list(metrics.keys()),
                    fill='toself',
                    name=persona_choice,
                    line=dict(color='#4CAF50')
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(metrics.values())],
                            gridcolor='#444',
                            linecolor='#888',
                            tickfont_color='#f1f1f1',
                        ),
                        bgcolor='#18191a',
                    ),
                    showlegend=False,
                    title="Metrikler Radar Grafiği",
                    paper_bgcolor='#18191a',
                    font=dict(color='#f1f1f1')
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Add custom CSS for expandable sections
            st.markdown("""
            <style>
                .expandable-section {
                    background-color: #1a1a1a;
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    border: 1px solid #333;
                    transition: all 0.3s ease;
                }
                .expandable-section:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                }
                .section-header {
                    color: #4CAF50;
                    font-size: 1.4em;
                    font-weight: 600;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                }
                .section-content {
                    color: #f1f1f1;
                    padding-left: 20px;
                }
                .section-content ul {
                    list-style-type: none;
                    padding-left: 0;
                }
                .section-content li {
                    margin-bottom: 10px;
                    padding-left: 20px;
                    position: relative;
                }
                .section-content li:before {
                    content: "•";
                    color: #4CAF50;
                    position: absolute;
                    left: 0;
                }
                .tag-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }
                .tag {
                    background-color: #333;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    transition: all 0.3s ease;
                }
                .tag:hover {
                    background-color: #4CAF50;
                    transform: translateY(-2px);
                }
            </style>
            """, unsafe_allow_html=True)

            # Bio section
            with st.expander("Temel Bilgiler", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                """, unsafe_allow_html=True)
                for bio in persona['bio']:
                    st.markdown(f"- {bio}")
                st.markdown("</div></div>", unsafe_allow_html=True)

            # Adjectives section
            with st.expander("Öne Çıkan Özellikler", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                        <div class="tag-container">
                """, unsafe_allow_html=True)
                for adj in persona['adjectives']:
                    st.markdown(f'<span class="tag">{adj}</span>', unsafe_allow_html=True)
                st.markdown("</div></div></div>", unsafe_allow_html=True)

            # Social media usage
            with st.expander("Sosyal Medya Kullanımı", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                """, unsafe_allow_html=True)
                for client in persona['clients']:
                    st.markdown(f"- {client}")
                st.markdown("</div></div>", unsafe_allow_html=True)

            # Lore section
            with st.expander("Geçmiş ve Değerler", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                """, unsafe_allow_html=True)
                for lore in persona['lore']:
                    st.markdown(f"- {lore}")
                st.markdown("</div></div>", unsafe_allow_html=True)

            # Knowledge section
            with st.expander("Bilgi ve Görüşler", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                """, unsafe_allow_html=True)
                for knowledge in persona['knowledge']:
                    st.markdown(f"- {knowledge}")
                st.markdown("</div></div>", unsafe_allow_html=True)

            # Topics section
            with st.expander("İlgilendiği Konular", expanded=True):
                st.markdown("""
                <div class="expandable-section">
                    <div class="section-content">
                """, unsafe_allow_html=True)
                for topic in persona['topics']:
                    st.markdown(f"- {topic}")
                st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()