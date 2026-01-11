# whatsapp_simulator.py - WhatsApp Testing Simulator
import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def simulate_whatsapp_message(message, phone="+917889850326"):
    """Simulate WhatsApp message and show formatted response"""
    print(f"\n📱 User: {message}")
    print("⏳ Processing...")
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", data={
            "Body": message,
            "From": f"whatsapp:{phone}"
        })
        
        if response.status_code == 200:
            # Extract message from Twilio XML response
            response_text = response.text
            if "<Message>" in response_text and "</Message>" in response_text:
                message_content = response_text.split("<Message>")[1].split("</Message>")[0]
                print(f"🤖 Swasthya Setu: {message_content}")
            else:
                print(f"🤖 Raw Response: {response_text}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    print("-" * 60)
    return response.text if 'response' in locals() else None

def run_complete_demo():
    """Complete demo simulation for hackathon presentation"""
    print("🎪" + "=" * 58 + "🎪")
    print("🏥        SWASTHYA SETU - WhatsApp Demo        🏥")
    print("🎪" + "=" * 58 + "🎪")
    print(f"⏰ Demo Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Demo Flow
    test_cases = [
        # 1. Language Selection
        ("language", "🌐 Show language menu"),
        
        # 2. Select English
        ("1", "🇺🇸 Select English language"),
        
        # 3. Fever Query
        ("I have high fever and headache", "🤒 English health query"),
        
        # 4. Emergency Case
        ("chest pain emergency help", "🚨 Emergency situation"),
        
        # 5. Switch to Hindi
        ("2", "🇮🇳 Switch to Hindi"),
        
        # 6. Hindi Health Query
        ("मुझे बुखार है और सिरदर्द हो रहा है", "🤒 Hindi health query"),
        
        # 7. Switch to Odia
        ("3", "🌾 Switch to Odia"),
        
        # 8. Odia Health Query
        ("ମୋର ଜ୍ୱର ଅଛି", "🤒 Odia health query"),
        
        # 9. General Help
        ("What services do you provide?", "ℹ️ Service information"),
    ]
    
    for i, (message, description) in enumerate(test_cases, 1):
        print(f"🔹 Test {i}/9: {description}")
        simulate_whatsapp_message(message)
        time.sleep(1.5)  # Pause between requests
    
    print("🎯 DEMO COMPLETE! Your chatbot is working perfectly! 🎉")
    print("Ready for hackathon presentation! 🏆")

def interactive_mode():
    """Interactive testing mode"""
    print("🔄 Interactive Mode - Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        user_input = input("\n📱 You: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        simulate_whatsapp_message(user_input)

if __name__ == "__main__":
    print("🚀 Swasthya Setu - WhatsApp Simulator")
    print("Choose mode:")
    print("1. Complete Demo (for presentation)")
    print("2. Interactive Testing")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == "1":
        run_complete_demo()
    elif choice == "2":
        interactive_mode()
    else:
        print("Running complete demo...")
        run_complete_demo()
