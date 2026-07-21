"""
Test models to find more working ones
"""

import asyncio
import os
from dotenv import load_dotenv
from litellm import acompletion

load_dotenv()

# Set API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY", "")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")

# Models to test - try different variations
MODELS = [
    # CONFIRMED WORKING
    ("Groq", "groq/llama-3.1-8b-instant", None),
    ("Mistral", "mistral/mistral-small-latest", None),
    ("OpenRouter Router", "openrouter/openrouter/free", "https://openrouter.ai/api/v1"),
    ("Nemotron", "openrouter/nvidia/nemotron-3-super-120b-a12b:free", "https://openrouter.ai/api/v1"),
    
    # Try without :free suffix
    ("Llama 3.1", "openrouter/meta-llama/llama-3.1-8b-instruct", "https://openrouter.ai/api/v1"),
    ("Mistral 7B", "openrouter/mistralai/mistral-7b-instruct", "https://openrouter.ai/api/v1"),
    ("Gemma 2", "openrouter/google/gemma-2-9b-it", "https://openrouter.ai/api/v1"),
    ("Phi 3", "openrouter/microsoft/phi-3-mini-128k", "https://openrouter.ai/api/v1"),
    ("Qwen 2.5", "openrouter/qwen/qwen-2.5-7b-instruct", "https://openrouter.ai/api/v1"),
    ("DeepSeek", "openrouter/deepseek/deepseek-v3", "https://openrouter.ai/api/v1"),
]

async def test_models():
    print("=" * 70)
    print("Testing Alternative Models")
    print("=" * 70)
    
    results = []
    
    for name, model_id, api_base in MODELS:
        print(f"\nTesting {name} ({model_id})...")
        print("-" * 50)
        
        try:
            kwargs = {
                "model": model_id,
                "messages": [{"role": "user", "content": "What is the capital of France? Answer in one word."}],
                "temperature": 0.3,
            }
            
            if api_base:
                kwargs["api_base"] = api_base
                kwargs["api_key"] = os.getenv("OPENROUTER_API_KEY")
                kwargs["extra_headers"] = {
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "AI Orchestrator",
                }
            
            response = await acompletion(**kwargs)
            answer = response.choices[0].message.content
            print(f"✅ SUCCESS!")
            print(f"   Response: {answer}")
            results.append((name, True, answer))
            
        except Exception as e:
            error_msg = str(e)[:150]
            print(f"❌ FAILED")
            print(f"   Error: {error_msg}")
            results.append((name, False, error_msg))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    
    working = [name for name, success, _ in results if success]
    failed = [name for name, success, _ in results if not success]
    
    print(f"✅ Working ({len(working)}):")
    for name in working:
        print(f"   ✓ {name}")
    
    if failed:
        print(f"\n❌ Failed ({len(failed)}):")
        for name in failed:
            print(f"   ✗ {name}")

if __name__ == "__main__":
    asyncio.run(test_models())