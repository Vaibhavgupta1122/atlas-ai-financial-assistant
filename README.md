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
