import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"

# Model configurations
GEMINI_TEXT_MODEL = "gemini-1.5-flash"

# Persona configurations
PERSONA_IMAGE_PROMPTS = {
    "Geleneksel Muhafazakar Çekirdek": "Create a realistic portrait photo of a 55-year-old Turkish woman wearing a headscarf. She has a calm and thoughtful expression. The background shows a traditional Turkish home with cultural elements. The image should show traditional family values and religious faith.",
    "Kentli Laik Modernler": "Create a realistic portrait photo of a 30-year-old Turkish professional in modern business attire. They are in a modern city setting, perhaps in a cafe or office. They look confident and intelligent, holding a book or tablet. The image shows modern and progressive values.",
    "Ekonomik Kaygılı Milliyetçiler": "Create a realistic portrait photo of a 40-year-old Turkish man with a serious and determined look. He wears casual clothes with a small Turkish flag pin. The background shows urban and industrial areas, representing economic concerns. The image shows national pride.",
    "Kararsız ve Sisteme Mesafeli Gençler": "Create a realistic portrait photo of a 20-year-old Turkish student. They have a thoughtful and uncertain expression. The background shows a modern city with technology and social media elements. The image shows youth searching for direction in life."
}

# Style mappings
STYLE_MAPPINGS = {
    "Çizgi Film": "in cartoon style",
    "Yağlı Boya": "in oil painting style",
    "Fotoğrafik": "in photographic style"
}

# Error messages
ERROR_MESSAGES = {
    "api_key_missing": "API anahtarı bulunamadı. Lütfen Streamlit secrets'a GEMINI_API_KEY ve REPLICATE_API_TOKEN ekleyin.",
    "image_generation_failed": "Görsel oluşturulamadı. Lütfen tekrar deneyin.",
    "quota_exceeded": "Görsel oluşturma kotanız doldu. Lütfen daha sonra tekrar deneyin veya farklı bir API anahtarı kullanın.",
    "api_error": "API hatası oluştu: {}"
} 