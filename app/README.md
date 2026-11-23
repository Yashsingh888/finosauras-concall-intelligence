# Finosauras – AI-Powered Concall Intelligence Platform

## Overview

Finosauras is an AI-powered Concall Intelligence Platform that collects corporate announcements from the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE), identifies earnings call transcript announcements, downloads transcript PDFs, extracts text, and generates structured summaries using Google's Gemini API.

The platform stores announcement metadata and generated summaries in an SQLite database. It also provides REST APIs, WebSocket notifications, and a web dashboard for accessing transcript summaries.

## Key Features

- Fetch corporate announcements from NSE and BSE.
- Identify earnings call transcript announcements.
- Store announcement metadata in SQLite.
- Download transcript PDF files.
- Extract text from PDF documents using PyMuPDF.
- Generate structured AI summaries using Google Gemini.
- Process long transcripts using text chunking.
- Save summaries in JSON and Markdown formats.
- Store generated summaries in the database.
- Provide company-wise summary APIs.
- Support real-time WebSocket communication.
- Display summaries through a web dashboard.
- Schedule automatic announcement collection and pending transcript processing.

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
| Environment Configuration | Python dotenv |

## Project Architecture

```text
finosauras-concall-intelligence/
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
│   │   └── transcript_processor.py
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
│   │   ├── summary_service.py
│   │   └── run_summaries.py
│   │
│   ├── static/
│   │   └── index.html
│   │
│   └── main.py
│
├── data/
│   └── samples/
│       ├── Frontier_Springs/
│       ├── Millworks_Technologies/
│       └── NIS_Management/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Runtime folders and the SQLite database are created or populated when the application runs.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Yashsingh888/finosauras-concall-intelligence.git
cd finosauras-concall-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file using the provided example:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your Gemini API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
```

**Security:** Never upload your actual `.env` file or Gemini API key to GitHub. The `.env` file is excluded through `.gitignore`.

### 5. Start the application

Run the following command from the project root:

```bash
uvicorn app.main:app --reload
```

The FastAPI application starts the scheduled transcript pipeline automatically.

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

Returns generated transcript summaries stored in the database.

### Get a company summary

`GET /api/summaries/{company_name}`

Returns the summary associated with a particular company.

### Publish a notification

`POST /api/notifications/publish`

Publishes a notification to connected WebSocket clients.

### Test notification

`POST /api/notifications/test`

Sends a test notification to connected clients.

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

These samples demonstrate the transcript extraction and summarization output formats.

## Pipeline Workflow

1. Fetch corporate announcements from NSE and BSE.
2. Filter announcements related to earnings call transcripts.
3. Store announcement metadata in SQLite.
4. Identify pending transcript announcements.
5. Download transcript PDF files.
6. Extract transcript text using PyMuPDF.
7. Divide long transcripts into manageable chunks.
8. Send transcript content to Gemini for summarization.
9. Generate structured JSON and Markdown summaries.
10. Store generated summaries in SQLite.
11. Provide summaries through REST APIs.
12. Send WebSocket notifications when transcript processing completes or fails.

The scheduler runs the pipeline automatically at configured intervals.

## Limitations

- NSE and BSE data availability depends on network connectivity, exchange access restrictions, and source availability.
- PDF extraction quality depends on the source document. Scanned PDFs may require OCR.
- Gemini API usage is subject to API quotas, rate limits, and network availability.
- AI-generated summaries may contain inaccuracies and should be checked against the original transcript.
- SQLite is suitable for this prototype but may need replacement with a more scalable database in production.
- Failed announcements require improved retry and recovery handling.
- WebSocket notifications depend on the application server and active client connections.

## Future Improvements

- Add OCR support for scanned PDF documents.
- Implement retry queues and automatic recovery for failed transcripts.
- Improve logging and error tracking.
- Use PostgreSQL for production deployment.
- Improve dashboard filtering and financial analytics.
- Add authentication and role-based access control.
- Support more advanced financial metrics and company comparisons.

## Disclaimer

This project is developed for educational and research purposes. AI-generated summaries may contain inaccuracies and should not be considered investment advice.
