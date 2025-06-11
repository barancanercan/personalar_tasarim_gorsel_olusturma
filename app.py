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
from src.models.gemini_handler import GeminiHandler
from src.utils.config import (
    PERSONA_IMAGE_PROMPTS,
    ERROR_MESSAGES,
    STYLE_MAPPINGS
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    .main, .stApp {
        background: #18191a !important;
    }
    .persona-card {
        background: #23272f;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        color: #f1f1f1;
    }
    .persona-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .persona-icon {
        font-size: 2em;
        margin-right: 15px;
    }
    .persona-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #f1f1f1;
    }
    .persona-subtitle {
        color: #b0b3b8;
        font-size: 0.9em;
    }
    .stat-item {
        background: #23272f;
        color: #f1f1f1;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 3px solid #444;
    }
    .tag {
        background: #393e46;
        color: #f1f1f1;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 0.8em;
        border: 1px solid #444;
    }
    .metric-card {
        background: #23272f;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #f1f1f1;
    }
    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #f1f1f1;
    }
    .metric-label {
        color: #b0b3b8;
        font-size: 0.9em;
    }
    .stDataFrame, .stTable {
        background: #23272f !important;
        color: #f1f1f1 !important;
    }
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {
        color: #f1f1f1 !important;
    }
    .image-gen-card {
        background: #23272f;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        padding: 32px 24px;
        margin: 0 auto 32px auto;
        max-width: 800px;
        color: #f1f1f1;
        text-align: center;
    }
    .image-gen-title {
        font-size: 2em;
        font-weight: 700;
        margin-bottom: 24px;
        color: #f1f1f1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .image-gen-subtitle {
        font-size: 1.1em;
        color: #b0b3b8;
        margin-bottom: 32px;
    }
    .image-gen-select {
        background: #393e46;
        color: #f1f1f1;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 8px 16px;
        margin-bottom: 24px;
        width: 100%;
        max-width: 400px;
    }
    .image-gen-btn {
        background: linear-gradient(135deg, #4c51bf 0%, #3e489c 100%);
        color: white;
        padding: 14px 36px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1em;
        border: none;
        margin: 24px 0;
        box-shadow: 0 4px 12px rgba(76, 81, 191, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .image-gen-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(76, 81, 191, 0.4);
    }
    .image-gen-btn:active {
        transform: translateY(0);
    }
    .image-gen-img {
        max-width: 100%;
        border-radius: 12px;
        margin-top: 32px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .image-gen-img:hover {
        transform: scale(1.02);
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 32px;
    }
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #4c51bf;
        border-top: 4px solid transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 16px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .error-message {
        background: rgba(220, 53, 69, 0.1);
        border: 1px solid rgba(220, 53, 69, 0.3);
        color: #dc3545;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Türk Toplumu Seçmen Personaları")
st.markdown("Kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili")

# Initialize Gemini handler
gemini_handler = GeminiHandler(api_key=st.secrets["GOOGLE_API_KEY"])

# Persona image generation prompts
persona_image_prompts = {
    "Geleneksel Muhafazakar Çekirdek": "A portrait of a 55-year-old Turkish woman, wearing a headscarf, looking thoughtful and serene. She is in a traditional Anatolian home setting, with subtle cultural motifs in the background. The image should convey a sense of strong family values and religious faith. Realistic style, portrait photo.",
    "Kentli Laik Modernler": "A stylish portrait of a 30-year-old Turkish professional, gender-neutral, in a modern urban environment like a bustling city street or a contemporary cafe. They are holding a book or a tablet, looking confident and intellectually curious. The image should convey a sense of modern, open-minded, and progressive values. Realistic style, vibrant colors.",
    "Ekonomik Kaygılı Milliyetçiler": "A portrait of a 40-year-old Turkish man, with a serious but determined expression, symbolizing national pride and concern for the economy. He is dressed in casual, practical clothing, perhaps with a subtle Turkish flag emblem. The background suggests a mix of urban and industrial elements, reflecting economic struggles. Realistic style, strong and grounded.",
    "Kararsız ve Sisteme Mesafeli Gençler": "A contemporary portrait of a 20-year-old Turkish student, gender-neutral, with a slightly contemplative or uncertain expression, looking towards the future. They are in a dynamic, possibly abstract urban setting with elements of technology and social media in the background, representing youth, questioning, and a search for direction. The image should capture a blend of hope and skepticism. Modern, somewhat artistic style."
}

# Persona data with enhanced metrics
personas = {
    "Geleneksel Muhafazakar Çekirdek": {
        "icon": "🕌",
        "color": "#e74c3c",
        "subtitle": "Değerlerine bağlı, sadık seçmen",
        "stats": {
            "Yaş Aralığı": "45-60+",
            "Eğitim": "Lise/Ortaokul",
            "Gelir": "Orta-Düşük",
            "Konum": "Anadolu Şehirleri",
            "Medya Tüketimi": "TV ve Yerel Medya",
            "Sosyal Medya Kullanımı": "Düşük",
            "Alışveriş Tercihi": "Yerel Marketler",
            "Boş Zaman Aktiviteleri": "Aile Zamanı, Dini Etkinlikler"
        },
        "metrics": {
            "Dindarlık Endeksi": 85,
            "Parti Bağlılığı": 90,
            "Kurumsal Güven": 75,
            "Ekonomik Endişe": 65,
            "Geleneksel Değerlere Bağlılık": 95,
            "Aile Değerleri": 90,
            "Toplumsal Değişime Açıklık": 40,
            "Teknoloji Adaptasyonu": 35
        },
        "description": "Geleneksel değerlere sıkı sıkıya bağlı, dini inançları güçlü, genellikle orta yaş ve üzeri kadınlardan oluşan bu grup, Anadolu'da yaşayan ve mevcut iktidar partilerine sadık bir seçmen kitlesini temsil eder.",
        "tags": ["AK Parti", "MHP", "Dindar", "Muhafazakar"],
        "trends": {
            "Ekonomi": -20,
            "Özgürlükler": 10,
            "Yolsuzluk": -15,
            "Yaşam Kalitesi": -25,
            "Güvenlik": 5,
            "Eğitim": -10,
            "Sağlık": -15,
            "İstihdam": -20
        },
        "voting_history": {
            "2018": "AK Parti",
            "2019": "AK Parti",
            "2023": "AK Parti"
        },
        "key_issues": [
            "Dini değerlerin korunması",
            "Aile yapısının güçlendirilmesi",
            "Ekonomik istikrar",
            "Güvenlik ve düzen"
        ]
    },
    "Kentli Laik Modernler": {
        "icon": "🏙️",
        "color": "#3498db",
        "subtitle": "Eğitimli, eleştirel düşünür",
        "stats": {
            "Yaş Aralığı": "25-44",
            "Eğitim": "Üniversite+",
            "Gelir": "Orta-Yüksek",
            "Konum": "Büyükşehirler",
            "Medya Tüketimi": "Dijital Medya",
            "Sosyal Medya Kullanımı": "Yüksek",
            "Alışveriş Tercihi": "Online Alışveriş",
            "Boş Zaman Aktiviteleri": "Kültür-Sanat, Spor"
        },
        "metrics": {
            "Dindarlık Endeksi": 30,
            "Parti Bağlılığı": 60,
            "Kurumsal Güven": 40,
            "Ekonomik Endişe": 85,
            "Modern Değerlere Bağlılık": 90,
            "Bireysel Özgürlükler": 95,
            "Toplumsal Değişime Açıklık": 85,
            "Teknoloji Adaptasyonu": 90
        },
        "description": "Modern, kentli yaşam tarzını benimsemiş, eğitimli, laik değerlere önem veren ve mevcut hükümet politikalarına eleştirel yaklaşan kesim. Ekonomik ve özgürlükler konusundaki endişeleri siyasi tercihlerini etkiler.",
        "tags": ["CHP", "İYİ Parti", "Laik", "Modernist"],
        "trends": {
            "Ekonomi": -35,
            "Özgürlükler": -40,
            "Yolsuzluk": -45,
            "Yaşam Kalitesi": -30,
            "Güvenlik": -25,
            "Eğitim": -35,
            "Sağlık": -30,
            "İstihdam": -40
        },
        "voting_history": {
            "2018": "CHP",
            "2019": "CHP",
            "2023": "CHP/İYİ Parti"
        },
        "key_issues": [
            "Demokratik haklar",
            "Ekonomik refah",
            "Eğitim kalitesi",
            "Çevre ve sürdürülebilirlik"
        ]
    },
    "Ekonomik Kaygılı Milliyetçiler": {
        "icon": "🇹🇷",
        "color": "#f39c12",
        "subtitle": "Ulusal değerlere bağlı, ekonomi odaklı",
        "stats": {
            "Yaş Aralığı": "25-50",
            "Eğitim": "Lise/Üniversite",
            "Gelir": "Orta",
            "Konum": "Karma",
            "Medya Tüketimi": "TV ve Sosyal Medya",
            "Sosyal Medya Kullanımı": "Orta",
            "Alışveriş Tercihi": "Yerel ve Online Karma",
            "Boş Zaman Aktiviteleri": "Spor, Sosyal Etkinlikler"
        },
        "metrics": {
            "Dindarlık Endeksi": 50,
            "Parti Bağlılığı": 70,
            "Kurumsal Güven": 60,
            "Ekonomik Endişe": 90,
            "Milliyetçilik": 85,
            "Ekonomik Güvenlik": 75,
            "Toplumsal Değişime Açıklık": 45,
            "Teknoloji Adaptasyonu": 60
        },
        "description": "Ekonomik kaygıları yüksek, milliyetçi değerlere bağlı, mülteci sorununa hassasiyet gösteren kesim. Geleneksel sağ partilere bağlılıkları olsa da ekonomik sıkıntılar ve ulusal kimlik meseleleri öncelik.",
        "tags": ["MHP", "Zafer Partisi", "Milliyetçi", "Ekonomi"],
        "trends": {
            "Ekonomi": -40,
            "Özgürlükler": -20,
            "Yolsuzluk": -35,
            "Yaşam Kalitesi": -35,
            "Güvenlik": -30,
            "Eğitim": -25,
            "Sağlık": -30,
            "İstihdam": -45
        },
        "voting_history": {
            "2018": "MHP",
            "2019": "MHP",
            "2023": "MHP/Zafer Partisi"
        },
        "key_issues": [
            "Ekonomik istikrar",
            "Ulusal güvenlik",
            "İstihdam",
            "Göç politikaları"
        ]
    },
    "Kararsız ve Sisteme Mesafeli Gençler": {
        "icon": "🤔",
        "color": "#9b59b6",
        "subtitle": "Gelecek kaygılı, sistem eleştirisi",
        "stats": {
            "Yaş Aralığı": "18-34",
            "Eğitim": "Lise/Üniversite",
            "Gelir": "Düşük-Orta",
            "Konum": "Çeşitli",
            "Medya Tüketimi": "Sosyal Medya",
            "Sosyal Medya Kullanımı": "Çok Yüksek",
            "Alışveriş Tercihi": "Online Alışveriş",
            "Boş Zaman Aktiviteleri": "Dijital İçerik, Sosyal Etkinlikler"
        },
        "metrics": {
            "Dindarlık Endeksi": 25,
            "Parti Bağlılığı": 20,
            "Kurumsal Güven": 15,
            "Ekonomik Endişe": 95,
            "Sistem Eleştirisi": 90,
            "Değişim Talebi": 85,
            "Toplumsal Değişime Açıklık": 95,
            "Teknoloji Adaptasyonu": 95
        },
        "description": "Ekonomik sıkıntılar, gelecek kaygısı ve kurumsal güvensizlik nedeniyle siyasi sisteme mesafeli duran genç kesim. Geleneksel parti bağlılıkları zayıf, protesto oyu verme veya oy kullanmama eğilimi yüksek.",
        "tags": ["Protesto", "Küçük Partiler", "Sisteme Mesafeli", "Genç"],
        "trends": {
            "Ekonomi": -45,
            "Özgürlükler": -45,
            "Yolsuzluk": -50,
            "Yaşam Kalitesi": -45,
            "Güvenlik": -35,
            "Eğitim": -40,
            "Sağlık": -35,
            "İstihdam": -50
        },
        "voting_history": {
            "2018": "Oy Kullanmadı",
            "2019": "Küçük Partiler",
            "2023": "Kararsız"
        },
        "key_issues": [
            "İş imkanları",
            "Eğitim sistemi",
            "Gelecek kaygısı",
            "Sistem değişikliği"
        ]
    }
}

# Sidebar with enhanced filters
st.sidebar.title("Filtreler ve Analizler")

# Persona selection
selected_persona = st.sidebar.selectbox(
    "Persona Seçin",
    list(personas.keys())
)

# Analysis type selection
analysis_type = st.sidebar.radio(
    "Analiz Türü",
    ["Genel Bakış", "Detaylı Analiz", "Karşılaştırma"]
)

# Sidebar: Add new module option
menu = ["Analizler", "Persona Görsel Oluşturucu"]
selected_menu = st.sidebar.radio("Modül Seçin", menu)

if selected_menu == "Analizler":
    # Main content
    if analysis_type == "Genel Bakış":
        col1, col2 = st.columns([2, 1])

        with col1:
            # Selected persona details
            persona = personas[selected_persona]
            st.markdown(f"""
            <div class="persona-card">
                <div class="persona-header">
                    <span class="persona-icon">{persona['icon']}</span>
                    <div>
                        <div class="persona-title">{selected_persona}</div>
                        <div class="persona-subtitle">{persona['subtitle']}</div>
                    </div>
                </div>
                <div class="persona-description">{persona['description']}</div>
                <div style="margin-top: 15px;">
                    {''.join([f'<span class="tag">{tag}</span>' for tag in persona['tags']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Metrics visualization
            metrics_df = pd.DataFrame({
                'Metrik': list(persona['metrics'].keys()),
                'Değer': list(persona['metrics'].values())
            })
            
            fig = px.bar(metrics_df, x='Metrik', y='Değer',
                         color_discrete_sequence=[persona['color']],
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
        trends = persona['trends']
        trends_df = pd.DataFrame({
            'Kategori': list(trends.keys()),
            'Değişim': list(trends.values())
        })
        
        fig = px.line(trends_df, x='Kategori', y='Değişim',
                      markers=True, color_discrete_sequence=[persona['color']],
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
        persona = personas[selected_persona]
        
        # Metrics cards with enhanced styling
        metrics = list(persona['metrics'].items())
        num_metrics = len(metrics)
        num_cols = 4
        num_rows = (num_metrics + num_cols - 1) // num_cols  # Ceiling division
        
        for row in range(num_rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                idx = row * num_cols + col
                if idx < num_metrics:
                    metric, value = metrics[idx]
                    with cols[col]:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{value}</div>
                            <div class="metric-label">{metric}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Detailed stats with enhanced visualization
        st.markdown("### Demografik Özellikler")
        stats_df = pd.DataFrame({
            'Özellik': list(persona['stats'].keys()),
            'Değer': list(persona['stats'].values())
        })
        st.dataframe(stats_df, use_container_width=True)
        
        # Voting history
        st.markdown("### Seçim Geçmişi")
        voting_df = pd.DataFrame({
            'Yıl': list(persona['voting_history'].keys()),
            'Tercih': list(persona['voting_history'].values())
        })
        st.dataframe(voting_df, use_container_width=True)
        
        # Key issues
        st.markdown("### Öncelikli Konular")
        for issue in persona['key_issues']:
            st.markdown(f"- {issue}")
        
        # Enhanced radar chart for metrics
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(persona['metrics'].values()),
            theta=list(persona['metrics'].keys()),
            fill='toself',
            name=selected_persona,
            line=dict(color=persona['color'])
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
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
        
        # Trend analysis with enhanced visualization
        st.markdown("### Trend Analizi")
        trends = persona['trends']
        trends_df = pd.DataFrame({
            'Kategori': list(trends.keys()),
            'Değişim': list(trends.values())
        })
        
        fig = px.bar(trends_df, x='Kategori', y='Değişim',
                     color='Değişim',
                     color_continuous_scale=['#e74c3c', '#f39c12', '#3498db'],
                     template='plotly_dark')
        fig.update_layout(
            title="Trend Analizi",
            showlegend=False,
            plot_bgcolor='#18191a',
            paper_bgcolor='#18191a',
            font=dict(color='#f1f1f1')
        )
        st.plotly_chart(fig, use_container_width=True)

    else:  # Comparison
        st.markdown("### Personalar Karşılaştırması")
        
        # Select personas to compare
        compare_personas = st.multiselect(
            "Karşılaştırılacak Personalar",
            list(personas.keys()),
            default=[selected_persona]
        )
        
        if len(compare_personas) > 0:
            # Metrics comparison
            metrics_comparison = pd.DataFrame({
                persona: personas[persona]['metrics']
                for persona in compare_personas
            })
            st.markdown("#### Metrik Karşılaştırması")
            st.dataframe(metrics_comparison, use_container_width=True)
            
            # Trends comparison
            trends_comparison = pd.DataFrame({
                persona: personas[persona]['trends']
                for persona in compare_personas
            })
            st.markdown("#### Trend Karşılaştırması")
            st.dataframe(trends_comparison, use_container_width=True)
            
            # Comparison chart
            fig = go.Figure()
            for persona in compare_personas:
                fig.add_trace(go.Scatterpolar(
                    r=list(personas[persona]['metrics'].values()),
                    theta=list(personas[persona]['metrics'].keys()),
                    fill='toself',
                    name=persona
                ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
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

elif selected_menu == "Persona Görsel Oluşturucu":
    st.markdown('<div class="image-gen-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-gen-title">Persona Görsel Oluşturucu</div>', unsafe_allow_html=True)
    st.markdown('<div class="image-gen-subtitle">Seçtiğiniz persona için yapay zeka destekli görsel oluşturun</div>', unsafe_allow_html=True)
    
    persona_choice = st.selectbox("Persona Seçin", list(PERSONA_IMAGE_PROMPTS.keys()), key="persona_image_select")

    if 'image_url' not in st.session_state:
        st.session_state['image_url'] = None
    if 'loading_image' not in st.session_state:
        st.session_state['loading_image'] = False
        
    # Custom prompt input
    st.subheader("Görsel Oluşturma Ayarları")
    custom_prompt = st.text_area(
        "Özel Prompt (İsteğe bağlı)",
        value=PERSONA_IMAGE_PROMPTS[persona_choice],
        help="Görsel oluşturmak için özel bir prompt girebilirsiniz. Boş bırakırsanız varsayılan prompt kullanılır."
    )

    if st.button("Görsel Oluştur", key="imagegen", help="Seçilen persona için yapay zeka ile görsel oluştur.",
                type="primary"):
        st.session_state['loading_image'] = True
        st.session_state['image_url'] = None
        
        # Use custom prompt if provided, otherwise use default
        prompt = custom_prompt if custom_prompt else PERSONA_IMAGE_PROMPTS[persona_choice]
        
        result = gemini_handler.generate_image(prompt)
        
        if result["success"]:
            st.session_state['image_url'] = result["image_url"]
        else:
            st.error(result["error"])
            
        st.session_state['loading_image'] = False
        
    if st.session_state['loading_image']:
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div>Görsel oluşturuluyor, lütfen bekleyin...</div>
        </div>
        """, unsafe_allow_html=True)
        
    if st.session_state.get('image_url'):
        st.image(st.session_state['image_url'], 
                 caption=f"{persona_choice} için oluşturulan görsel", 
                 use_column_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)