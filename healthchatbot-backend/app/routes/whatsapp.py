# 🚦 Person A - WhatsApp webhook integration
# app/routes/whatsapp.py
# 🚦 Person A - WhatsApp webhook integration
# app/routes/whatsapp.py
# app/routes/whatsapp.py
from fastapi import APIRouter, Form, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from decouple import config
from app.db.db import save_chat_history
from app.services.emergency_service import check_emergency_keywords
import logging

router = APIRouter()

# Initialize Twilio client
client = Client(config("TWILIO_ACCOUNT_SID"), config("TWILIO_AUTH_TOKEN"))

# FAQ responses
FAQ_DATA = {
    "fever": "🌡️ Fever: Rest, drink plenty of fluids, take paracetamol. If fever >101°F for 3+ days, consult doctor immediately.",
    "ଜ୍ୱର": "🌡️ ଜ୍ୱର: ବିଶ୍ରାମ ନିଅନ୍ତୁ, ଅଧିକ ପାଣି ପିଅନ୍ତୁ। ୧୦୧°F ଉପରେ ୩ ଦିନ ରହିଲେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",
    "बुखार": "🌡️ बुखार: आराम करें, पानी पिएं। 101°F से ज्यादा 3 दिन तक हो तो डॉक्टर से मिलें।",

    "cough": "😷 Cough: Warm water with honey, steam inhalation. If persistent >2 weeks, see doctor.",
    "କାଶ": "😷 କାଶ: ମହୁ ସହିତ ଗରମ ପାଣି, ବାଷ୍ପ ନିଅନ୍ତୁ। ୨ ସପ୍ତାହରୁ ଅଧିକ ରହିଲେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",
    "खांसी": "😷 खांसी: शहद के साथ गर्म पानी, भाप लें। 2 हफ्ते से ज्यादा हो तो डॉक्टर को दिखाएं।",

    "headache": "🤕 Headache: Rest in dark room, drink water, gentle head massage. If severe, consult doctor.",
    "ମୁଣ୍ଡବିନ୍ଧା": "🤕 ମୁଣ୍ଡବିନ୍ଧା: ଅନ୍ଧାର ଘରେ ବିଶ୍ରାମ, ପାଣି ପିଅନ୍ତୁ। ଯଦି ଅଧିକ ଯନ୍ତ୍ରଣା, ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",

    "appointment": "📅 For appointment booking, share your district name. Available: Kalahandi PHC, Khordha CHC, Cuttack PHC",
    "emergency": "🚨 EMERGENCY NUMBERS:\n- Ambulance: 108\n- Medical Emergency: 102\n- COVID Helpline: 1075\nFor immediate help, call these numbers!",

    "help": "🏥 SWASTHYA SETU - I can help with:\n• Health queries (fever, cough, headache)\n• Book appointments at PHC/CHC\n• Emergency assistance\n• Vaccination info\nType your symptoms or 'appointment' to book.",
}

@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    """Handle incoming WhatsApp messages with detailed logging"""
    try:
        user_message = Body.strip()
        user_phone = From.replace("whatsapp:", "")

        logging.info(f"📞 Received WhatsApp message: '{Body}' from {user_phone}")

        # Check for emergency keywords first
        try:
            is_emergency, emergency_response = await check_emergency_keywords(user_message.lower(), user_phone)
            logging.info(f"🚨 Emergency check: {is_emergency}")
        except Exception as e:
            logging.error(f"Emergency check failed: {str(e)}")
            is_emergency, emergency_response = False, ""

        if is_emergency:
            response_text = emergency_response
            logging.info(f"🚨 Emergency response: {response_text[:100]}...")
        else:
            # LOCAL KEYWORD MATCHING
            response_text = FAQ_DATA["help"]  # Default response
            user_lower = user_message.lower()
            
            matched = False
            for keyword, response in FAQ_DATA.items():
                if keyword.lower() in user_lower:
                    response_text = response
                    logging.info(f"✅ Matched keyword '{keyword}' -> sending response")
                    matched = True
                    break
            
            if not matched:
                logging.info(f"❌ No keywords matched, using default help response")

        logging.info(f"📤 Prepared response: {response_text[:100]}...")

        # Save conversation to database
        try:
            await save_chat_history(user_phone, Body, response_text)
            logging.info("💾 Chat history saved successfully")
        except Exception as e:
            logging.error(f"Failed to save chat history: {str(e)}")

        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        response_xml = str(resp)

        logging.info(f"✅ TwiML response created: {response_xml[:150]}...")
        return Response(content=response_xml, media_type="application/xml")

    except Exception as e:
        logging.error(f"❌ Critical error in WhatsApp webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, I'm having technical difficulties. Please try again later or call 108 for emergencies.")
        return Response(content=str(resp), media_type="application/xml")


@router.get("/send-test")
async def send_test_message(to: str, message: str):
    """Test endpoint to send WhatsApp message via Twilio"""
    try:
        msg = client.messages.create(
            body=message,
            from_=config("TWILIO_WHATSAPP_NUMBER"),
            to=f"whatsapp:{to}"
        )
        return {"status": "sent", "sid": msg.sid, "to": to}
    except Exception as e:
        return {"status": "error", "message": str(e)}
