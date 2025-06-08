
from fastapi import BackgroundTasks, FastAPI, Form, Response
from twilio.rest import Client as TwilioClient
from google.genai import Client as GoogleClient
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import os
from googleapiclient.discovery import build

from models import Invoice

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
twilio_client = TwilioClient(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
PHONE_NUMBER_FROM = os.getenv("PHONE_NUMBER_FROM")
client = GoogleClient(api_key=GOOGLE_API_KEY)

app = FastAPI(title="Billerbee API", description="A simple FastAPI application", version="1.0.0")

@app.get("/")
async def read_root():
    return {"message": "Hello World", "project": "Billerbee"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/message")
async def receive_message(background_tasks: BackgroundTasks, message: str = Form(), sender: str = Form(), image_path: str = Form()):
    print(f"Received message: {message}")

    background_tasks.add_task(analyze_message, message, sender, image_path)
    read_write_sheet(SPREADSHEET_ID, "A:I", message)
    
    return {"status": "message received"}

@app.post("/analyze")
async def analyze_message(image_path: str):
    try:
        image = Image.open(image_path)

        contents=[
            "Here is an image of an invoice: ",
            image,
        ]

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Invoice,
                system_instruction=open("system-prompt.txt").read()
            ),
        )

        return Response(content=response.text, media_type="text/plain", status_code=200)
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=500)

def read_write_sheet(spreadsheet_id: str, range_name: str, value: str):
    """
    Reads and writes to a Google Sheet using the Google Sheets API.
    
    Args:
        spreadsheet_id (str): The ID of the spreadsheet to access
        range_name (str): The A1 notation of the values to read/write
        value (str): The value to write to the sheet
    """
    try:
        # Use API key for authentication
        service = build('sheets', 'v4', 
                       developerKey=GOOGLE_API_KEY)
        
        # Read the current value
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            majorDimension="ROWS"
        ).execute()

        data_list = list(result.values())
        print(f"Data list: {data_list[-1][0]}")
        ## Write the new value
        #body = {
        #    'values': [[value]]
        #}
        #result = sheet.values().update(
        #    spreadsheetId=spreadsheet_id,
        #    range=range_name,
        #    valueInputOption='RAW',
        #    body=body
        #).execute()
        
        return {"status": "success", "message": f"Updated {range_name} with value: {value}"}
        
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

def send_message(message: str, sender: str):
    twilio_client.messages.create(from_=PHONE_NUMBER_FROM,
                        to=sender,
                        body=message)
    print(f"Sent message: {message} to {sender}")
