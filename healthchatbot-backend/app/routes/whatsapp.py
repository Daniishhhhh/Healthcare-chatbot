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
from app.services.pipeline import assistant_orchestrator
import logging

router = APIRouter()

# Initialize Twilio client
try:
    client = Client(config("TWILIO_ACCOUNT_SID"), config("TWILIO_AUTH_TOKEN"))
except Exception:
    client = None
    logging.warning("Twilio credentials not configured; outbound WhatsApp disabled.")

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

        # Route through centralized orchestrator for consistency
        orchestrated = await assistant_orchestrator.handle_query(
            message=user_message, user_id=user_phone
        )
        response_text = orchestrated["response"]
        logging.info(f"🔍 Orchestrated response intent={orchestrated['intent']}")

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
    if not client:
        return {"status": "error", "message": "Twilio not configured"}
    try:
        msg = client.messages.create(
            body=message,
            from_=config("TWILIO_WHATSAPP_NUMBER"),
            to=f"whatsapp:{to}"
        )
        return {"status": "sent", "sid": msg.sid, "to": to}
    except Exception as e:
        return {"status": "error", "message": str(e)}
