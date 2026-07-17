"""
=========================================================
Saad Python Project
api_manager.py
Version : 4.6
=========================================================
"""

import asyncio
import time
import os
import random
from typing import Dict, List

from litellm import acompletion
from config import RESPONDENT_MODELS, AVAILABLE_MODELS


class APIManager:
    """Central API Manager for all AI models."""

    def __init__(self):
        # Create mapping from model ID to display name
        self.model_display_map = {}
        for display, model_id in zip(AVAILABLE_MODELS, RESPONDENT_MODELS):
            self.model_display_map[model_id] = display

    async def ask_model(self, model_name: str, prompt: str) -> Dict:
        start = time.perf_counter()

        try:
            # Add slight temperature variation for duplicates
            temp_variation = random.uniform(0.3, 0.7)
            
            # Prepare kwargs for the API call
            kwargs = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temp_variation,
            }
            
            # Special handling for different providers
            if "groq" in model_name:
                kwargs["api_key"] = os.getenv("GROQ_API_KEY")
                
            elif "mistral" in model_name and "openrouter" not in model_name:
                kwargs["api_key"] = os.getenv("MISTRAL_API_KEY")
                
            elif "openrouter" in model_name:
                kwargs["api_key"] = os.getenv("OPENROUTER_API_KEY")
                kwargs["api_base"] = "https://openrouter.ai/api/v1"
                kwargs["extra_headers"] = {
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "Rajco AI Orchestrator",
                }
                
            elif "xai" in model_name or "grok" in model_name.lower():
                kwargs["api_base"] = "https://api.x.ai/v1"
                kwargs["api_key"] = os.getenv("GROK_API_KEY")
                
            elif "deepseek" in model_name and "openrouter" not in model_name:
                kwargs["api_key"] = os.getenv("DEEPSEEK_API_KEY")
                kwargs["api_base"] = "https://api.deepseek.com/v1"
                
            elif "gemini" in model_name and "openrouter" not in model_name:
                kwargs["api_key"] = os.getenv("GEMINI_API_KEY")
            
            response = await acompletion(**kwargs)

            answer = response.choices[0].message.content
            elapsed = round(time.perf_counter() - start, 2)
            
            # Get display name
            display_name = self.model_display_map.get(model_name, model_name)

            return {
                "model": display_name,
                "model_id": model_name,
                "status": "success",
                "response": answer,
                "time": elapsed,
            }

        except Exception as e:
            elapsed = round(time.perf_counter() - start, 2)
            error_msg = str(e)
            
            # Get display name
            display_name = self.model_display_map.get(model_name, model_name)
            
            # Provide more helpful error messages
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                error_msg = f"⚠️ Rate limit exceeded. Try again in a moment."
            elif "insufficient balance" in error_msg.lower():
                error_msg = f"⚠️ Insufficient balance. Please add credits."
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                error_msg = f"⚠️ Invalid API key. Please check your key."
            elif "model not found" in error_msg.lower():
                error_msg = f"⚠️ Model temporarily unavailable."
            elif "rate limit" in error_msg.lower():
                error_msg = f"⚠️ Rate limit exceeded. Try again in a moment."
            
            return {
                "model": display_name,
                "model_id": model_name,
                "status": "failed",
                "response": error_msg,
                "time": elapsed,
            }

    async def ask_all_models(self, prompt: str) -> List[Dict]:
        tasks = [
            self.ask_model(model, prompt)
            for model in RESPONDENT_MODELS
        ]

        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    async def demo():
        manager = APIManager()

        results = await manager.ask_all_models(
            "What is Artificial Intelligence? Answer in 2 sentences."
        )

        for item in results:
            print("=" * 60)
            print(f"Model : {item['model']}")
            print(f"Status: {item['status']}")
            print(f"Time  : {item['time']} sec")
            if item["status"] == "success":
                print(f"Response: {item['response'][:200]}...")
            else:
                print(f"Error: {item['response']}")

    asyncio.run(demo())