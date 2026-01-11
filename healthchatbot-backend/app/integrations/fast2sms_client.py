# app/integrations/fast2sms_client.py
import requests
import logging

logger = logging.getLogger(__name__)

class Fast2SMSClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.fast2sms.com/dev/bulkV2"
    
    def send_sms(self, phone_number: str, message: str) -> dict:
        """Send SMS via Fast2SMS"""
        if not self.api_key or self.api_key == "YOUR_API_KEY_FROM_STEP_2":
            return {
                "status": "error",
                "error": "Fast2SMS API key not configured",
                "status_code": 400
            }
        
        clean_phone = phone_number.replace("+91", "").replace("+", "")
        
        payload = {
            "authorization": self.api_key,
            "message": message,
            "language": "english", 
            "route": "q",
            "numbers": clean_phone,
            "flash": "0"
        }
        
        headers = {'cache-control': "no-cache"}
        
        try:
            response = requests.post(self.base_url, data=payload, headers=headers)
            return {
                "status": "success" if response.status_code == 200 else "error",
                "response": response.json(),
                "status_code": response.status_code
            }
        except Exception as e:
            logger.error(f"Fast2SMS error: {e}")
            return {"status": "error", "error": str(e)}
