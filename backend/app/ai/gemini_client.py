# pyrefly: ignore [missing-import]
import httpx
from app.utils.settings import settings


class GeminiClient:
    def is_configured(self) -> bool:
        return settings.ai_provider.lower() == "gemini" and bool(settings.gemini_api_key)

    def generate(self, prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "analysis": {"type": "STRING"},
                        "explanation": {"type": "STRING"},
                        "recommendations": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        },
                        "evidence": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        }
                    },
                    "required": ["analysis", "explanation", "recommendations", "evidence"]
                }
            }
        }
        
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                # Extract the text component from Gemini response
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            raise RuntimeError(f"Gemini API invocation failed: {str(e)}")


gemini_client = GeminiClient()

