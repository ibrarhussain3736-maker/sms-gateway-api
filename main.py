from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="SMS OTP Gateway API")

SMS_DATABASE = {
    "aaData": [
        [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Pakistan",
            "+923001234567",
            "WhatsApp",
            "Your WhatsApp verification code is: 456-123. Do not share this code."
        ]
    ]
}

class SMSModel(BaseModel):
    number: str
    service: str
    message: str
    country: str = "Pakistan"

@app.get("/api")
def get_sms_logs(number: str = None):
    if number:
        for record in SMS_DATABASE["aaData"]:
            if number in record[2]:
                return {
                    "status": "success",
                    "number": record[2],
                    "service": record[3],
                    "message": record[4]
                }
        raise HTTPException(status_code=404, detail="Number not found")
    return SMS_DATABASE

@app.post("/api/add")
def add_sms_log(data: SMSModel):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_record = [timestamp, data.country, data.number, data.service, data.message]
    SMS_DATABASE["aaData"].insert(0, new_record)
    if len(SMS_DATABASE["aaData"]) > 100:
        SMS_DATABASE["aaData"].pop()
    return {"status": "success", "message": "SMS recorded successfully"}
