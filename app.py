import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from gtts import gTTS
import base64
import requests
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Set page config
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

# Persona data
personas = {
    "Hatice Teyze": {
        "image": "persona_profil_fotograflari/hatice_teyze.jpg",
        "description": "Geleneksel Muhafazakar Çekirdek",
        "metrics": {
            "Sosyal Medya Kullanımı": 0.3,
            "Politik İlgi": 0.8,
            "Ekonomik Endişe": 0.7,
            "Kültürel Değerler": 0.9
        },
        "bio": [
            "55 yaşında, ev hanımı",
            "Geleneksel değerlere bağlı",
            "Dini inançları güçlü",
            "Aile odaklı yaşam tarzı"
        ],
        "topics": [
            "Ekonomi ve geçim sıkıntısı",
            "Aile değerleri",
            "Dini ve kültürel konular",
            "Güvenlik ve huzur"
        ],
        "adjectives": ["Muhafazakar", "Geleneksel", "Aile Odaklı", "Dindar"]
    },
    "Kenan Bey": {
        "image": "persona_profil_fotograflari/kenan_bey.jpg",
        "description": "Kentli Laik Modernler",
        "metrics": {
            "Sosyal Medya Kullanımı": 0.8,
            "Politik İlgi": 0.6,
            "Ekonomik Endişe": 0.5,
            "Kültürel Değerler": 0.4
        },
        "bio": [
            "45 yaşında, beyaz yakalı",
            "Kentli ve modern yaşam tarzı",
            "Laik ve seküler değerlere sahip",
            "Profesyonel kariyer odaklı"
        ],
        "topics": [
            "Ekonomik kalkınma",
            "Demokrasi ve özgürlükler",
            "Eğitim ve kültür",
            "Uluslararası ilişkiler"
        ],
        "adjectives": ["Modern", "Laik", "Profesyonel", "Kentli"]
    },
    "Tuğrul Bey": {
        "image": "persona_profil_fotograflari/tugrul_bey.jpg",
        "description": "Ekonomik Kaygılı Milliyetçiler",
        "metrics": {
            "Sosyal Medya Kullanımı": 0.5,
            "Politik İlgi": 0.7,
            "Ekonomik Endişe": 0.9,
            "Kültürel Değerler": 0.6
        },
        "bio": [
            "50 yaşında, esnaf",
            "Milliyetçi değerlere sahip",
            "Ekonomik kaygıları yüksek",
            "Yerel işletme sahibi"
        ],
        "topics": [
            "Ekonomik kriz",
            "Milli değerler",
            "Yerel üretim",
            "İşsizlik"
        ],
        "adjectives": ["Milliyetçi", "Esnaf", "Ekonomik Kaygılı", "Yerel"]
    },
    "Elif": {
        "image": "persona_profil_fotograflari/elif.jpg",
        "description": "Kararsız ve Sisteme Mesafeli Gençler",
        "metrics": {
            "Sosyal Medya Kullanımı": 0.9,
            "Politik İlgi": 0.4,
            "Ekonomik Endişe": 0.8,
            "Kültürel Değerler": 0.3
        },
        "bio": [
            "25 yaşında, üniversite öğrencisi",
            "Sosyal medya bağımlısı",
            "Sisteme karşı mesafeli",
            "Gelecek kaygısı yüksek"
        ],
        "topics": [
            "İş ve kariyer fırsatları",
            "Sosyal medya trendleri",
            "Gençlik sorunları",
            "Gelecek endişeleri"
        ],
        "adjectives": ["Genç", "Sosyal Medya Bağımlısı", "Kararsız", "Modern"]
    }
}

# Function to create persona card
def create_persona_card(name, data):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(data["image"], width=200)
    with col2:
        st.markdown(f"### {name}")
        st.markdown(f"**{data['description']}**")
        st.markdown("---")
        for metric, value in data["metrics"].items():
            st.progress(value, text=metric)
        
        # Bio section
        st.markdown("#### Temel Bilgiler")
        for bio in data["bio"]:
            st.markdown(f"- {bio}")
        
        # Topics section
        st.markdown("#### İlgilendiği Konular")
        for topic in data["topics"]:
            st.markdown(f"- {topic}")
        
        # Adjectives section
        st.markdown("#### Öne Çıkan Özellikler")
        for adj in data["adjectives"]:
            st.markdown(f'<span class="tag">{adj}</span>', unsafe_allow_html=True)

# Function to create metrics visualization
def create_metrics_viz(persona_name, data):
    metrics_df = pd.DataFrame({
        'Metric': list(data["metrics"].keys()),
        'Value': list(data["metrics"].values())
    })
    
    fig = px.bar(metrics_df, x='Metric', y='Value',
                 title=f"{persona_name} - Metrikler",
                 color='Value',
                 color_continuous_scale='RdYlBu_r')
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#f1f1f1'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Function to create comparison visualization
def create_comparison_viz(selected_personas):
    comparison_data = []
    for name in selected_personas:
        for metric, value in personas[name]["metrics"].items():
            comparison_data.append({
                'Persona': name,
                'Metric': metric,
                'Value': value
            })
    
    df = pd.DataFrame(comparison_data)
    
    fig = px.bar(df, x='Metric', y='Value', color='Persona',
                 title='Persona Karşılaştırması',
                 barmode='group')
    
    fig.update_layout(
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#f1f1f1'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Function to get persona response
def get_persona_response(persona_name, user_input):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Sen {persona_name} olarak yanıt ver. {personas[persona_name]['description']} 
    özelliklerine sahip bir seçmen olarak düşün ve yanıtla. Kısa ve öz yanıtlar ver.
    
    Temel Bilgiler:
    {', '.join(personas[persona_name]['bio'])}
    
    İlgilendiği Konular:
    {', '.join(personas[persona_name]['topics'])}
    
    Kullanıcı: {user_input}
    """
    
    response = model.generate_content(prompt)
    return response.text

# Function to text-to-speech
def text_to_speech(text, lang='tr'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = "temp_audio.mp3"
    tts.save(audio_file)
    return audio_file

# Main app
def main():
    st.title("🗳️ Türk Seçmen Personaları")
    
    # Sidebar
    st.sidebar.title("Modüller")
    module = st.sidebar.radio("Seçiniz:", ["PersonaGPT", "Analizler", "Persona Kartları"])
    
    if module == "PersonaGPT":
        st.header("🤖 PersonaGPT")
        
        # Persona selection
        selected_persona = st.selectbox(
            "Persona Seçin:",
            list(personas.keys())
        )
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Mesajınızı yazın..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get persona response
            response = get_persona_response(selected_persona, prompt)
            
            # Add persona response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
                
                # Text-to-speech
                audio_file = text_to_speech(response)
                st.audio(audio_file)
    
    elif module == "Analizler":
        st.header("📊 Analizler")
        
        analysis_type = st.selectbox(
            "Analiz Türü:",
            ["Genel Bakış", "Detaylı Analiz", "Karşılaştırma"]
        )
        
        if analysis_type == "Genel Bakış":
            st.subheader("Tüm Personaların Genel Bakışı")
            for name, data in personas.items():
                create_metrics_viz(name, data)
        
        elif analysis_type == "Detaylı Analiz":
            selected_persona = st.selectbox(
                "Persona Seçin:",
                list(personas.keys())
            )
            
            # Create two columns for layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Display persona profile
                st.image(personas[selected_persona]["image"], width=200)
                st.markdown(f"### {selected_persona}")
                st.markdown(f"**{personas[selected_persona]['description']}**")
                
                # Display metrics
                st.markdown("#### Metrikler")
                for metric, value in personas[selected_persona]["metrics"].items():
                    st.progress(value, text=metric)
            
            with col2:
                # Display bio
                st.markdown("#### Temel Bilgiler")
                for bio in personas[selected_persona]["bio"]:
                    st.markdown(f"- {bio}")
                
                # Display topics
                st.markdown("#### İlgilendiği Konular")
                for topic in personas[selected_persona]["topics"]:
                    st.markdown(f"- {topic}")
                
                # Display adjectives
                st.markdown("#### Öne Çıkan Özellikler")
                for adj in personas[selected_persona]["adjectives"]:
                    st.markdown(f'<span class="tag">{adj}</span>', unsafe_allow_html=True)
            
            # Create metrics visualization
            create_metrics_viz(selected_persona, personas[selected_persona])
        
        else:  # Karşılaştırma
            selected_personas = st.multiselect(
                "Karşılaştırılacak Personaları Seçin:",
                list(personas.keys()),
                default=list(personas.keys())[:2]
            )
            if len(selected_personas) >= 2:
                create_comparison_viz(selected_personas)
            else:
                st.warning("Lütfen en az iki persona seçin.")
    
    else:  # Persona Kartları
        st.header("👥 Persona Kartları")
        
        for name, data in personas.items():
            with st.expander(f"{name} - {data['description']}"):
                create_persona_card(name, data)

if __name__ == "__main__":
    main()