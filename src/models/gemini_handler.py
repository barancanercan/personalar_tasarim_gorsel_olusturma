import google.generativeai as genai
import base64
import requests
import os
from typing import Optional, Dict, Any
from ..utils.config import (
    GEMINI_TEXT_MODEL,
    ERROR_MESSAGES,
    PERSONA_IMAGE_PROMPTS
)

class GeminiHandler:
    def __init__(self, api_key: str):
        """Initialize Gemini handler with API key."""
        genai.configure(api_key=api_key)
        self.text_model = genai.GenerativeModel('gemini-1.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash-vision')
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

    def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini Flash."""
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {str(e)}"

    def generate_image(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Gemini Flash Vision."""
        try:
            response = self.vision_model.generate_content(prompt)
            return {"success": True, "image_url": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_image_stable_diffusion(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Stable Diffusion via Hugging Face API."""
        try:
            if not isinstance(prompt, str) or not prompt.strip():
                return {"success": False, "error": "Geçersiz prompt. Lütfen geçerli bir metin girin."}

            # Hugging Face API endpoint
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}

            # Prepare the payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": "blurry, low quality, distorted, deformed",
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }

            # Make the API request
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code != 200:
                return {"success": False, "error": f"API yanıt hatası: {response.status_code}"}

            # Convert the image to base64
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            return {
                "success": True,
                "image_url": f"data:image/jpeg;base64,{image_base64}"
            }

        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'quota' in error_msg.lower():
                return {"success": False, "error": ERROR_MESSAGES["quota_exceeded"]}
            elif '400' in error_msg:
                return {"success": False, "error": "API yanıt hatası. Lütfen daha sonra tekrar deneyin."}
            elif '403' in error_msg:
                return {"success": False, "error": "API erişim hatası. API anahtarınızı kontrol edin."}
            return {"success": False, "error": ERROR_MESSAGES["api_error"].format(error_msg)} 