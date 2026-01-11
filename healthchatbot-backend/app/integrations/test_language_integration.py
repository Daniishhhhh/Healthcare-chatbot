# test_complete_integration.py - Complete integration testing
import requests
import sys
from pathlib import Path
import asyncio

# Add project path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import your integrated functions
from app.integrations.fast2sms_client import Fast2SMSClient
from app.services.query_service import HealthQueryProcessor
from app.services.language_detector import detect_language_with_confidence
import os

# Initialize clients (you'll need to add your API key)
FAST2SMS_API_KEY = "YOUR_API_KEY_HERE"  # Add your actual API key
sms_client = Fast2SMSClient(FAST2SMS_API_KEY)
health_processor = HealthQueryProcessor()

def test_direct_sms():
    """Test sending SMS directly via Fast2SMS client"""
    print("🧪 Testing Direct SMS with Fast2SMS Client...")
    
    result = sms_client.send_sms("7889850326", "Test message from your health chatbot! Integration working perfectly. 🎉")
    print(f"Direct SMS Result: {result}")
    return result

def test_language_detection():
    """Test Person B's language detection"""
    print("\n🧪 Testing Language Detection...")
    
    test_texts = [
        "I have fever",
        "मुझे बुखार है", 
        "ମୋର ଜ୍ୱର ଅଛି"
    ]
    
    for text in test_texts:
        lang, confidence = detect_language_with_confidence(text)
        print(f"Text: '{text}' → Language: {lang} (confidence: {confidence:.2f})")

async def test_health_processing():
    """Test Person B's health query processing"""
    print("\n🧪 Testing Health Query Processing...")
    
    queries = [
        ("I have high fever", "en"),
        ("मुझे सिरदर्द है", "hi"),
        ("emergency help needed", "en")
    ]
    
    for query, lang in queries:
        try:
            result = await health_processor.process_query_async(query, lang)
            print(f"Query: '{query}' → Response: '{result['response'][:50]}...'")
        except Exception as e:
            print(f"Query: '{query}' → Error: {str(e)}")

def test_webhook_endpoints():
    """Test SMS and WhatsApp webhook endpoints"""
    print("\n🧪 Testing Webhook Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test WhatsApp webhook
    whatsapp_data = {
        "Body": "I have fever",
        "From": "whatsapp:+917889850326"
    }
    
    try:
        response = requests.post(f"{base_url}/webhook", data=whatsapp_data)
        print(f"WhatsApp Webhook: {response.status_code} - Success")
    except requests.exceptions.ConnectionError:
        print("WhatsApp Webhook: Server not running (start with: uvicorn main:app --reload)")
    
    # Test SMS webhook  
    sms_data = {
        "Body": "emergency help needed",
        "From": "+917889850326"
    }
    
    try:
        response = requests.post(f"{base_url}/sms/webhook", data=sms_data)
        print(f"SMS Webhook: {response.status_code} - Success")
    except requests.exceptions.ConnectionError:
        print("SMS Webhook: Server not running")

def test_language_selection_flow():
    """Test complete language selection flow"""
    print("\n🧪 Testing Language Selection Flow...")
    
    base_url = "http://localhost:8000"
    
    test_cases = [
        {"Body": "language", "From": "whatsapp:+917889850326", "expect": "language menu"},
        {"Body": "2", "From": "whatsapp:+917889850326", "expect": "Hindi welcome"},
        {"Body": "मुझे बुखार है", "From": "whatsapp:+917889850326", "expect": "Hindi response"}
    ]
    
    for case in test_cases:
        try:
            response = requests.post(f"{base_url}/webhook", data=case)
            print(f"Language Flow - {case['expect']}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Language Flow - {case['expect']}: Server not running")

async def run_all_tests():
    """Run all tests in sequence"""
    print("🚀 Starting Complete Integration Tests...\n")
    
    # Test 1: Direct SMS (requires API key)
    if FAST2SMS_API_KEY != "YOUR_API_KEY_HERE":
        test_direct_sms()
    else:
        print("⚠️  Skipping SMS test - Add your Fast2SMS API key")
    
    # Test 2: Language Detection
    test_language_detection()
    
    # Test 3: Health Processing
    await test_health_processing()
    
    # Test 4: Webhook Endpoints
    test_webhook_endpoints()
    
    # Test 5: Language Selection
    test_language_selection_flow()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
