# Finosauras – AI-Powered Concall Intelligence Platform

## Overview

Finosauras is an AI-powered Concall Intelligence Platform that collects corporate announcements from NSE and BSE, identifies earnings call transcript announcements, downloads PDF transcripts, extracts text, and generates structured summaries using Google's Gemini API.

The platform stores announcement and summary information in an SQLite database and provides REST APIs and WebSocket notifications for real-time updates.

## Key Features

- Fetch corporate announcements from NSE and BSE.
- Identify announcements related to earnings call transcripts.
- Store announcement metadata in SQLite.
- Download transcript PDF files.
- Extract text from PDF documents using PyMuPDF.
- Generate structured AI summaries using Google Gemini.
- Save summaries in JSON and Markdown formats.
- Provide company-wise summary APIs.
- Support real-time WebSocket notifications.
- Display summaries through a web dashboard.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI Summarization | Google Gemini API |
| Database | SQLite, SQLAlchemy |
| PDF Extraction | PyMuPDF |
| API | REST API |
| Real-time Communication | WebSocket |
| Frontend | HTML, CSS, JavaScript |
| Scheduler | APScheduler |

## Project Architecture

```text
finosauras/
│
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   ├── websocket.py
│   │   └── notifications.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── init_db.py
│   │
│   ├── extraction/
│   │   ├── pdf_downloader.py
│   │   ├── pdf_extractor.py
│   │   ├── process_pending.py
│   │   └── extract_pending.py
│   │
│   ├── ingestion/
│   │   ├── nse_fetcher.py
│   │   ├── bse_fetcher.py
│   │   ├── transcript_filter.py
│   │   ├── transcript_collector.py
│   │   └── scheduler.py
│   │
│   ├── summarization/
│   │   ├── prompts.py
│   │   ├── ai_summarizer.py
│   │   ├── summary_formatter.py
│   │   └── run_summaries.py
│   │
│   ├── static/
│   │   └── index.html
│   │
│   └── main.py
│
├── data/
│   ├── transcripts/
│   ├── extracted_text/
│   ├── summaries/
│   ├── samples/
│   └── finosauras.db
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd finosauras
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never upload your actual API key to GitHub.

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

## Application URLs

| Service | URL |
|---|---|
| Dashboard | http://127.0.0.1:8000/dashboard |
| API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |
| All Summaries | http://127.0.0.1:8000/api/summaries |
| WebSocket | ws://127.0.0.1:8000/ws/updates |

## API Endpoints

### Get all summaries

`GET /api/summaries`

Returns company-wise summaries stored in the database.

### Get a company summary

`GET /api/summaries/{company_name}`

Returns the summary for a particular company.

### Publish a notification

`POST /api/notifications/publish`

Publishes a notification to connected WebSocket clients.

### Test notification

`POST /api/notifications/test`

Sends a test notification.

## Sample Companies

The repository includes sample datasets for:

1. Frontier Springs Ltd
2. Millworks Technologies Ltd
3. NIS Management Ltd

Each sample contains:

- Original transcript PDF
- Extracted transcript text
- Structured JSON summary
- Formatted Markdown summary

## Pipeline Workflow

1. Fetch announcements from NSE and BSE.
2. Filter announcements related to concall transcripts.
3. Store announcement metadata in SQLite.
4. Download transcript PDFs.
5. Extract transcript text.
6. Send transcript text to Gemini for summarization.
7. Generate structured JSON and Markdown summaries.
8. Store summaries in the database.
9. Provide summaries through REST APIs.
10. Notify connected clients through WebSockets.

## Limitations

- NSE and BSE availability depends on their APIs, network connectivity and access restrictions.
- PDF extraction quality depends on the source document. Scanned PDFs may require OCR.
- Gemini API usage is subject to API quotas, rate limits and network availability.
- AI-generated summaries should be checked against the original transcript.
- The current implementation uses SQLite, which is suitable for this prototype but may need a more scalable database in production.
- Transcript downloading, extraction and summarization are available through separate processing scripts; the scheduled collector currently handles announcement collection.

## Future Improvements

- Add OCR support for scanned PDF documents.
- Implement automated end-to-end transcript processing.
- Add retry queues and improved error handling.
- Use PostgreSQL for production deployment.
- Improve dashboard filtering and analytics.
- Add authentication and role-based access control.

## Disclaimer

This project is developed for educational and research purposes. AI-generated summaries may contain inaccuracies and should not be considered investment advice.