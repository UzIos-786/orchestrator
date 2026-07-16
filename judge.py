"""
=========================================================
Saad Python Project
judge.py
Version : 3.0
=========================================================
"""

import os
import asyncio
from typing import List, Dict
from litellm import acompletion


class Judge:
    """
    AI-powered response judge using Gemini.
    
    Version 3.0:
    - Uses Gemini to judge and select the best response
    - Falls back to length-based selection if Gemini fails
    """

    def __init__(self):
        self.gemini_model = "gemini/gemini-1.5-flash"
        self.api_key = os.getenv("GEMINI_API_KEY")

    async def select_best_async(self, responses: List[Dict]) -> Dict:
        """Use Gemini to select the best response."""
        
        # Filter successful responses
        successful = [
            r for r in responses
            if r.get("status") == "success" and r.get("response", "").strip()
        ]

        if not successful:
            return {
                "model": "None",
                "response": "No successful response received.",
                "time": 0,
            }

        if len(successful) == 1:
            return successful[0]

        # Prepare the prompt for Gemini
        prompt = self._build_judge_prompt(successful)
        
        try:
            # Call Gemini
            response = await acompletion(
                model=self.gemini_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert judge evaluating AI responses. Select the best response based on accuracy, completeness, clarity, and helpfulness. Return ONLY the model name exactly as shown in the list, nothing else."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                api_key=self.api_key,
            )
            
            # Extract the selected model name
            selected_model = response.choices[0].message.content.strip()
            
            # Find the matching response
            for resp in successful:
                if resp.get("model") == selected_model:
                    return resp
                # Try fuzzy match if exact match fails
                if selected_model.lower() in resp.get("model", "").lower():
                    return resp
            
            # If no match found, fallback to length-based
            return self._fallback_select(successful)
            
        except Exception as e:
            print(f"Gemini judge error: {e}")
            # Fallback to length-based selection
            return self._fallback_select(successful)

    def _build_judge_prompt(self, responses: List[Dict]) -> str:
        """Build the prompt for Gemini."""
        prompt = "Here are responses from different AI models:\n\n"
        
        for i, resp in enumerate(responses, 1):
            model_name = resp.get("model", f"Model {i}")
            content = resp.get("response", "")
            prompt += f"Model {i}: {model_name}\n"
            prompt += f"Response: {content}\n\n"
        
        prompt += """
Please evaluate these responses and select the BEST one based on:
1. Accuracy and factual correctness
2. Completeness of the answer
3. Clarity and readability
4. Helpfulness and relevance

Return ONLY the model name from the list above (e.g., "Groq Llama 3.1" or "Mistral Small").
Do not add any explanation, just the model name.
"""
        return prompt

    def _fallback_select(self, responses: List[Dict]) -> Dict:
        """Fallback: select the longest response."""
        return max(
            responses,
            key=lambda r: len(r.get("response", ""))
        )

    def select_best(self, responses: List[Dict]) -> Dict:
        """Synchronous wrapper for select_best_async."""
        return asyncio.run(self.select_best_async(responses))

    def summary(self, responses: List[Dict]) -> Dict:
        """Generate a summary of responses."""
        best = self.select_best(responses)
        return {
            "total_models": len(responses),
            "successful": sum(r["status"] == "success" for r in responses),
            "failed": sum(r["status"] == "failed" for r in responses),
            "best_model": best.get("model", "None"),
            "best_response": best.get("response", ""),
        }


if __name__ == "__main__":
    import asyncio
    
    sample = [
        {
            "model": "Groq Llama 3.1",
            "status": "success",
            "response": "Artificial Intelligence is the simulation of human intelligence by machines.",
            "time": 1.2,
        },
        {
            "model": "Mistral Small",
            "status": "success",
            "response": "AI enables machines to learn, reason, solve problems, and assist humans in many industries through data-driven algorithms. It has applications in healthcare, finance, and transportation.",
            "time": 1.8,
        },
        {
            "model": "OpenRouter Pro",
            "status": "success",
            "response": "Artificial Intelligence is a broad field of computer science focused on creating systems that can perform tasks that typically require human intelligence.",
            "time": 1.5,
        },
        {
            "model": "Gemini",
            "status": "failed",
            "response": "API Error",
            "time": 0.6,
        },
    ]

    judge = Judge()

    print("=" * 60)
    print("Gemini Judge Test")
    print("=" * 60)

    best = judge.select_best(sample)
    print(f"\n🏆 Best Model : {best['model']}")
    print(f"📝 Response   : {best['response']}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(judge.summary(sample))