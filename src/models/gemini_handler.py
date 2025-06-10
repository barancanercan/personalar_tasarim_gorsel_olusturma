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
        """Initialize handler with API keys."""
        genai.configure(api_key=api_key)
        self.text_model = genai.GenerativeModel(GEMINI_TEXT_MODEL)
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using Gemini Pro."""
        try:
            response = self.text_model.generate_content(
                prompt,
                generation_config={
                    "temperature": kwargs.get("temperature", 0.95),
                    "top_p": kwargs.get("top_p", 1),
                    "top_k": kwargs.get("top_k", 32),
                    "max_output_tokens": kwargs.get("max_output_tokens", 2048),
                }
            )
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_image(self, prompt: str) -> Dict[str, Any]:
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