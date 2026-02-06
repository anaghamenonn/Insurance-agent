# Autonomous Insurance Claims Processing Agent

## Overview
This project implements a lightweight AI-powered agent that processes FNOL (First Notice of Loss) documents.  
The system extracts key claim information, identifies missing fields, applies routing rules, and returns a structured JSON response.

The agent supports both **PDF and TXT claim documents**.

## Features
- Extracts key claim fields from FNOL documents
- Detects missing mandatory fields
- Classifies and routes claims based on business rules
- Provides reasoning for routing decisions
- Supports PDF and text inputs
- AI-based extraction with rule-based fallback

## Routing Logic
The claim is routed based on the following rules:

| Condition | Route |
|-----------|-------|
| Estimated damage < 25,000 | Fast-track |
| Missing mandatory fields | Manual Review |
| Description contains fraud-related keywords | Investigation Flag |
| Claim type is injury | Specialist Queue |

## Output Format
The system returns the following JSON:

```json
{
  "extractedFields": {},
  "missingFields": [],
  "recommendedRoute": "",
  "reasoning": ""
}
```

## Tech Stack
Python  
FastAPI  
OpenAI API (for AI extraction)  
PyPDF (PDF text extraction)

## Setup Instructions
### 1. Clone the repository
```
git clone https://github.com/anaghamenonn/Insurance-agent.git
cd insurance-agent
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Configure environment variables
Create a .env file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```
If no API key is provided, the system will automatically use rule-based extraction.

### 4. Run the server
uvicorn app.main:app --reload

### 5. Open API docs
Open in browser:  
http://127.0.0.1:8000/docs  
Use the /process-claim endpoint to upload a PDF or TXT file.  

Example Test  
Upload:  
sample_docs/sample.txt  
Expected output:  

{  
  "extractedFields": {  
    "policyNumber": "P123456",  
    "incidentDate": "01/15/2026",  
    "estimatedDamage": 12000,  
    "claimType": "vehicle"  
  },  
  "missingFields": [],  
  "recommendedRoute": "Fast-track",  
  "reasoning": "Damage below threshold"  
}  
