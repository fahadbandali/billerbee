# BillerBee 🐝

BillerBee is an intelligent receipt processing service that uses Google's Gemini AI to parse physical receipts and invoices. It extracts structured data and makes it available through an API or directly in Google Sheets, making expense tracking and bookkeeping easier.

## Features

- 📸 Process receipt images using Gemini AI
- 📊 Export data to Google Sheets
- 🔄 RESTful API for data access
- 📱 SMS notifications via Twilio
- 🤖 Intelligent data extraction including:
  - Item details
  - Business information
  - Pricing and tax calculations
  - Payment information

## Setup

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)
- Google Cloud account with Gemini API access
- Google Sheets API enabled
- Twilio account (for SMS notifications)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/billerbee.git
   cd billerbee
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip3 install pydantic "fastapi[standard]" google.genai googleapiclient pillow dotenv twilio
   ```

4. Create a `.env` file in the root directory with your configuration:
   ```bash
   touch .env
   ```

5. Start the FastAPI server:
   ```bash
   fastapp dev main.py
   ```

The API will be available at:
- Main application: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## Environment Variables

```env
# Google API Configuration
GOOGLE_API_KEY=your_gemini_api_key
SPREADSHEET_ID=your_google_sheets_id

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
PHONE_NUMBER_FROM=your_twilio_phone_number
```

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Google API key with access to Gemini API |
| `SPREADSHEET_ID` | ID of the Google Sheet where data will be stored |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID for SMS notifications |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token for SMS notifications |
| `PHONE_NUMBER_FROM` | Twilio phone number to send SMS from |

## API Endpoints

- `GET /` - Health check endpoint
- `GET /health` - Service health status
- `POST /message` - Process receipt image and message
- `POST /analyze` - Analyze receipt image using Gemini AI

## Data Structure

The service processes receipts into a structured format:

```python
{
    "Item": str,
    "Business": str,
    "Address": str,
    "Date": str,
    "PaymentType": str,
    "Card_Id": str,
    "Quantity": int,
    "Price": float,
    "Tax": float,
    "Total": float
}
```