import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from gtts import gTTS
from datetime import datetime

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
        
class Character:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        # Combine bio and lore for summary
        bio = getattr(self, 'bio', [])
        lore = getattr(self, 'lore', [])
        if isinstance(bio, str):
            bio = [bio]
        if isinstance(lore, str):
            lore = [lore]
        self.bio_lore = bio + lore
        # For backward compatibility
        self.name = getattr(self, 'name', getattr(self, 'isim', None))
        self.description = getattr(self, 'description', getattr(self, 'aciklama', ''))
        self.metrics = getattr(self, 'metrics', getattr(self, 'metrikler', {}))
        self.topics = getattr(self, 'topics', getattr(self, 'konular', []))
        self.adjectives = getattr(self, 'adjectives', getattr(self, 'sifatlar', []))
        self.image = getattr(self, 'profil_fotografi', getattr(self, 'image', None))
        # Add gender attribute
        self.gender = getattr(self, 'gender', 'female' if self.name in ['Hatice Teyze', 'Elif'] else 'male')

# Karakterleri JSON dosyalarından yükle
def load_personas():
    personas = {}
    personas_dir = os.path.join(os.path.dirname(__file__), 'personas')
    for filename in os.listdir(personas_dir):
        if filename.endswith('.json'):
            with open(os.path.join(personas_dir, filename), 'r', encoding='utf-8') as f:
                persona_data = json.load(f)
                persona = Character(persona_data)
                personas[persona.name] = persona
    return personas

personas = load_personas()

# Persona Card Template
def create_persona_card(persona):
    """Create a persona card with the specified structure"""
    with st.expander(f"{persona.name}", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Resim gösterimi
            turkish_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
            name = persona.name.lower()
            for turkish_char, latin_char in turkish_chars.items():
                name = name.replace(turkish_char, latin_char)
            image_path = f"persona_profil_fotograflari/{name.replace(' ', '_')}.jpg"
            try:
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.error(f"Resim bulunamadı: {image_path}")
                    st.image("https://via.placeholder.com/150", use_container_width=True)
            except Exception as e:
                st.error(f"Resim yüklenirken hata oluştu: {str(e)}")
                st.image("https://via.placeholder.com/150", use_container_width=True)
        
        with col2:
            # İsim
            st.markdown(f"### {persona.name}")
            
            # Biyografi
            st.markdown("#### Biyografi")
            for item in persona.bio:
                st.markdown(f"- {item}")
            
            # Lore
            st.markdown("#### Lore")
            for item in persona.lore:
                st.markdown(f"- {item}")
            
            # Knowledge
            st.markdown("#### Knowledge")
            for item in persona.knowledge:
                st.markdown(f"- {item}")
            
            # Topics
            st.markdown("#### Topics")
            for item in persona.topics:
                st.markdown(f"- {item}")
            
            # Style
            st.markdown("#### Style")
            
            # All
            st.markdown("##### All")
            for item in persona.style['all']:
                st.markdown(f"- {item}")
            
            # Chat
            st.markdown("##### Chat")
            for item in persona.style['chat']:
                st.markdown(f"- {item}")
            
            # Post
            st.markdown("##### Post")
            for item in persona.style['post']:
                st.markdown(f"- {item}")
            
            # Adjectives
            st.markdown("#### Adjectives")
            for item in persona.adjectives:
                st.markdown(f"- {item}")
            
            # Clients
            st.markdown("#### Clients")
            for item in persona.clients:
                st.markdown(f"- {item}")

# PersonaGPT prompt function
def get_persona_response(persona: Character, user_input):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Sen {persona.name} olarak yanıt ver. {persona.description}\n\n"
        if persona.bio_lore:
            prompt += ' '.join(persona.bio_lore) + "\n\n"
        if persona.topics:
            prompt += f"İlgilendiği Konular: {', '.join(persona.topics)}\n"
        if persona.adjectives:
            prompt += f"Öne Çıkan Özellikler: {', '.join(persona.adjectives)}\n"
        if getattr(persona, 'modelProvider', None):
            prompt += f"Model Sağlayıcı: {persona.modelProvider}\n"
        if getattr(persona, 'clients', None):
            prompt += f"Kullandığı Platformlar: {', '.join(persona.clients)}\n"
        prompt += f"\nKullanıcı: {user_input}\n"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Hatası: {str(e)}\nLütfen API anahtarınızı ve model adını kontrol edin."

# Function to text-to-speech (female voice only)
def text_to_speech(text, persona=None):
    tts = gTTS(text=text, lang='tr', slow=False)
    audio_file = "temp_audio.mp3"
    tts.save(audio_file)
    return audio_file

def download_chat_history(messages, persona_name):
    if not messages:
        return None
    
    # Create chat history text
    chat_text = f"Konuşma Geçmişi - {persona_name}\n"
    chat_text += f"Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    chat_text += "=" * 50 + "\n\n"
    
    for message in messages:
        role = "Kullanıcı" if message["role"] == "user" else persona_name
        chat_text += f"{role}: {message['content']}\n\n"
    
    return chat_text

# Main app
def main():
    st.title("🗳️ Türk Seçmen Personaları")
    st.sidebar.title("Modüller")
    module = st.sidebar.radio("Seçiniz:", ["PersonaGPT", "Persona Kartları"])

    if module == "PersonaGPT":
        st.header("🤖 PersonaGPT")
        selected_persona_name = st.selectbox("Persona Seçin:", list(personas.keys()))
        persona = personas[selected_persona_name]
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Add download button if there are messages
        if st.session_state.messages:
            chat_text = download_chat_history(st.session_state.messages, persona.name)
            st.download_button(
                label="📥 Konuşmayı İndir",
                data=chat_text,
                file_name=f"konusma_{persona.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Mesajınızı yazın..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            response = get_persona_response(persona, prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
            audio_file = text_to_speech(response, persona)
            st.audio(audio_file)

    else:  # Persona Kartları
        st.header("👥 Persona Kartları")
        for persona in personas.values():
            create_persona_card(persona)

if __name__ == "__main__":
    main()