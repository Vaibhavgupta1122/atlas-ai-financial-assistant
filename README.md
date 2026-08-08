# 🤖 Atlas AI Financial Assistant

Atlas is an AI-powered financial assistant that allows users to interact naturally with financial data through a Telegram bot.

It combines **financial market data, financial news, company research, intent detection, conversation history, PostgreSQL persistence, and Gemini-powered AI analysis** into a single assistant.

---

## 🚀 Features

- 💬 Natural-language financial conversations
- 🤖 AI-powered financial analysis
- 📊 Real-time stock market quotes
- 🏢 Company research
- 📰 Latest financial news
- 📚 Financial concept explanations
- 🧠 AI-based intent detection
- 📱 Telegram Bot integration
- 💾 PostgreSQL conversation and user storage
- 👤 Telegram user management
- 🗂️ Conversation history
- 🔎 Company ticker detection
- ⚡ FastAPI-ready backend architecture
- 🛡️ Environment-based configuration
- 🔄 Graceful fallback when Gemini API quota is unavailable

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Telegram       │
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Telegram Bot      │
                         │  telegram_bot.py    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Atlas Service    │
                         │  Request Orchestrator│
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
              ┌────────────┐ ┌────────────┐ ┌────────────┐
              │   Intent   │ │   Market   │ │    News    │
              │  Service   │ │  Service   │ │  Service   │
              └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │   Research Service  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AI Service       │
                         │  Google Gemini API   │
                         └─────────────────────┘

                                    │
                                    ▼

                         ┌─────────────────────┐
                         │     PostgreSQL      │
                         │ Users + Conversations│
                         └─────────────────────┘
🧠 How Atlas Works

When a user sends a message, Atlas processes the request through multiple services.

Example

User:

Give me a quick rundown on Apple

Atlas identifies:

Intent: company_research
Company: Apple
Ticker: AAPL

The system then retrieves:

Current market price
Previous closing price
Price change
Recent financial news
Relevant company information

The collected information is passed to the AI service for analysis.

The final response is then returned to Telegram and stored in PostgreSQL.

🎯 Supported Intents

Atlas currently supports the following intent categories:

Intent	Example
company_research	Give me a quick rundown on Apple
market_quote	What is Microsoft's stock price?
financial_news	Show me the latest financial news
general_finance	What is an IPO?
general_conversation	Hello Atlas
📱 Telegram Commands

Atlas provides the following Telegram commands:

/start

Starts the Atlas assistant.

/news

Retrieves the latest financial news.

/help

Displays available commands and example queries.

💬 Example Queries
Market Data
What's Apple's stock price?
How is NVIDIA doing?
What is Microsoft's stock price?
Company Research
Give me a quick rundown on Apple
What's happening with Nvidia?
Tell me about Microsoft
Financial News
Show me the latest financial news
What's the latest news about NVIDIA?
Financial Concepts
What is an IPO?
Explain P/E ratio
What is market capitalization?
🛠️ Technology Stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
AI / Generative AI
Google Gemini API
Google GenAI SDK
LLM-based intent detection
AI-powered financial analysis
Telegram
Python Telegram Bot
Financial Data
Market data APIs
Financial news APIs
Development
VS Code
Python Virtual Environment
Git
GitHub Desktop
PostgreSQL
📂 Project Structure
atlas-ai-financial-assistant/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── bot/
│   ├── __init__.py
│   └── telegram_bot.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── init_db.py
│
├── models/
│   ├── __init__.py
│   └── ...
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── atlas_service.py
│   ├── conversation_service.py
│   ├── intent_service.py
│   ├── market_service.py
│   ├── news_service.py
│   ├── research_service.py
│   ├── user_service.py
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/atlas-ai-financial-assistant.git

Move into the project:

cd atlas-ai-financial-assistant
2. Create Virtual Environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in the project root.

Example:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/atlas_finance

Add any additional API keys required by the configured market/news services.

⚠️ Important

Never commit .env to GitHub.

Your .gitignore should contain:

.env
.env.*
.venv/
__pycache__/
*.pyc
*.log
🗄️ Database Setup

Make sure PostgreSQL is installed and running.

Create the Atlas database.

Then initialize the database:

python -m database.init_db

The application uses PostgreSQL for persistent storage of:

Telegram users
Usernames
Conversation messages
Assistant responses
🤖 Telegram Bot Setup

Create a Telegram bot using BotFather.

Obtain the bot token and place it inside .env:

TELEGRAM_BOT_TOKEN=your_token_here

Start the bot:

python -m bot.telegram_bot

Expected output:

======================================================================
ATLAS TELEGRAM BOT IS STARTING...
======================================================================
Telegram command menu configured successfully.
Bot is running and waiting for Telegram messages.
Available commands:
  /start
  /news
  /help
Press Ctrl+C to stop the bot.
======================================================================
🧪 Testing

The project contains individual service tests to verify different components independently.

Test Intent Detection
python -m services.test_intent

Example:

User:
Give me a quick rundown on Apple

Detected intent:
{
    'intent': 'company_research',
    'company': 'Apple',
    'ticker': 'AAPL',
    'query': 'Give me a quick rundown on Apple'
}
Test Research Service
python -m services.test_research

The research service verifies:

Company identification
Stock ticker
Market data
Financial news
AI analysis
Test Atlas Service
python -m services.test_atlas

This tests the complete Atlas orchestration layer.

Test News Service
python -m services.test_news

This verifies retrieval of recent financial news.

🧩 Service Architecture
Atlas Service

The Atlas service acts as the main orchestration layer.

It determines which services need to be called based on the detected intent.

User Request
     │
     ▼
Intent Detection
     │
     ├── Market Quote
     │
     ├── Company Research
     │
     ├── Financial News
     │
     └── General Finance
     │
     ▼
Service Processing
     │
     ▼
AI Analysis
     │
     ▼
Final Response
Intent Service

The intent service uses Gemini to classify user requests.

Example:

"What is Microsoft's stock price?"

becomes:

intent: market_quote
company: Microsoft
ticker: MSFT
Market Service

The market service retrieves stock information such as:

Symbol
Price
Previous Close
Change
Change %

Example:

{
    "symbol": "AAPL",
    "price": 313.33,
    "previous_close": 312.41,
    "change": 0.92,
    "change_percent": 0.29
}
News Service

The news service retrieves recent financial articles and provides:

Title
Source
Publication date
URL

Example:

Title: Nvidia sells RTX 50-series GPUs at MSRP during QuakeCon 2026
Source: Tom's Hardware
Published: 2026-08-07
Research Service

The research service combines:

Company
+
Market Data
+
Financial News
+
AI Analysis

to produce a company research response.

AI Service

The AI service connects Atlas with Google's Gemini API.

It is responsible for:

Natural-language understanding
Intent classification
Financial explanations
Company analysis
Response generation

If the Gemini API is temporarily unavailable or the API quota is exhausted, Atlas gracefully falls back to available financial market and news data.

🛡️ Error Handling

Atlas includes fallback handling for AI service failures.

For example, if the Gemini API returns:

429 RESOURCE_EXHAUSTED

Atlas can still return available financial information instead of completely failing.

Example:

📊 Apple (AAPL)

Price: $313.33
Change: 0.92 (0.29%)

I can currently retrieve financial market data
and recent financial news, but my advanced AI
analysis service is temporarily unavailable.

This keeps the financial-data portion of the application functional even when the AI service is unavailable.

🔒 Security

The project uses environment variables for sensitive configuration.

Sensitive values include:

Telegram Bot Token
Gemini API Key
Database credentials
Financial API credentials

These values should never be hardcoded into Python source files.

Never commit:

.env

to GitHub.

📈 Example Atlas Workflow
User
 │
 │ "What's happening with Nvidia?"
 ▼
Telegram Bot
 │
 ▼
Atlas Service
 │
 ▼
Intent Service
 │
 └── company_research
        │
        ├── Company: NVIDIA
        └── Ticker: NVDA
                │
                ▼
        ┌──────────────────┐
        │  Market Service  │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   News Service   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   AI Service     │
        │     Gemini       │
        └────────┬─────────┘
                 │
                 ▼
             Response
                 │
                 ▼
             Telegram
🎯 Project Goals

Atlas was designed to demonstrate how multiple backend and AI services can be integrated into a practical financial assistant.

The project focuses on:

AI-powered applications
Financial data integration
LLM-based intent detection
Service-oriented architecture
REST API development
Database persistence
Telegram bot development
Generative AI integration
Graceful API failure handling
🚧 Future Improvements

Potential future improvements include:

📈 Interactive stock charts
📊 Portfolio tracking
💰 Personal portfolio analysis
🔔 Price alerts
📉 Technical indicators
📰 Personalized news feeds
📋 Watchlists
🔐 User authentication
☁️ Cloud deployment
🐳 Docker support
⚡ Redis caching
🔄 Background jobs with Celery
📊 Financial dashboards
🧠 Multi-model AI support
⚠️ Disclaimer

Atlas is an educational and software-development project.

Financial information provided by the application may be delayed, incomplete, or inaccurate.

Atlas should not be considered a substitute for professional financial advice.

Always verify important financial information using reliable sources before making investment decisions.

👨‍💻 Author

Vaibhav Gupta

AI / ML Engineer | Python Developer | Generative AI

⭐ Project Highlights
Python
FastAPI
PostgreSQL
SQLAlchemy
Telegram Bot
Google Gemini
Generative AI
LLM Intent Detection
Financial APIs
REST APIs
Conversation Memory
Service-Oriented Architecture

If you find this project useful, consider giving the repository a ⭐.


### GitHub note

For your repository, **do not include the actual `.env` contents**. Keep `.env` ignored and use something li
