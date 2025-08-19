#!/usr/bin/env python3
"""
O3 Model Configuration Script
Configure which O3 model to use based on cost preferences and test API access
"""

import os
from dotenv import load_dotenv, set_key
from openai import OpenAI

def main():
    print("🚀 O3 Model Configuration for Ali 2025 Campaign Bot")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Model options with pricing
    models = {
        "1": {
            "name": "o3-mini",
            "cost": "$0.30-0.60 per 1M tokens",
            "description": "Cost-effective O3 reasoning - Great for most campaign interactions"
        },
        "2": {
            "name": "o3", 
            "cost": "$15-60 per 1M tokens",
            "description": "Premium O3 reasoning - Best for complex policy discussions"
        }
    }
    
    print("\n📋 Available O3 Models:")
    for key, model in models.items():
        print(f"{key}. {model['name']}")
        print(f"   Cost: {model['cost']}")
        print(f"   {model['description']}\n")
    
    # Get user choice
    choice = input("Which model would you like to use? (1 or 2): ").strip()
    
    if choice not in models:
        print("❌ Invalid choice. Defaulting to o3-mini")
        choice = "1"
    
    selected_model = models[choice]["name"]
    print(f"\n🎯 Selected model: {selected_model}")
    
    # Test the selected model
    print(f"\n🧪 Testing {selected_model}...")
    try:
        test_response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "user", "content": "Hello! Can you confirm you're working properly?"}
            ],
            max_completion_tokens=50
        )
        
        print(f"✅ {selected_model} is working!")
        print(f"Test response: {test_response.choices[0].message.content}")
        
        # Save model preference to .env
        env_file = ".env"
        set_key(env_file, "O3_MODEL", selected_model)
        print(f"\n💾 Model preference saved to {env_file}")
        
        # Show cost estimate
        print(f"\n💰 Cost Information:")
        print(f"Selected model: {selected_model}")
        print(f"Cost: {models[choice]['cost']}")
        print(f"Typical campaign response: ~500 tokens")
        
        if selected_model == "o3-mini":
            print("Estimated cost per response: $0.0003 - $0.0006 (very affordable)")
        else:
            print("Estimated cost per response: $0.0075 - $0.03 (premium)")
            
        print("\n🎉 O3 integration is ready!")
        print("You can now run: python test_complete_system.py")
        
    except Exception as e:
        print(f"❌ Error testing {selected_model}: {str(e)}")
        print("Falling back to o3-mini...")
        set_key(".env", "O3_MODEL", "o3-mini")

if __name__ == "__main__":
    main()
