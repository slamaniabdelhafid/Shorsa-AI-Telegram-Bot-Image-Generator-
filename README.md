
<p align="center">
  <img src="assets/screenshots/logo.png" width="200">
</p>

<h1 align="center">Shorsa AI – Telegram Image Generator Bot</h1>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://core.telegram.org/bots/api">
    <img src="https://img.shields.io/badge/Telegram-Bot_API-26A5E4?logo=telegram&logoColor=white" alt="Telegram">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>




##  Overview

**Shorsa AI** is an intelligent **Telegram bot** that generates high-quality AI images from user text prompts using **Sberbank’s GigaChat API**.
The system is designed to be **scalable, fast, and production-ready**, featuring a **credit-based monetization system**, **Redis caching**, and an **administrative dashboard built with FastAPI**.


---

##  Key Features

*  AI image generation from text prompts
*  High-quality images returned directly in Telegram
*  Credit-based usage system
*  Online payments via **Paymaster.ru**
*  Admin dashboard (FastAPI + Swagger UI)
*  Redis for caching, credits, and rate-limiting
*  Scalable backend architecture

---

##  Technologies Used

| Technology                     | Purpose                         |
| ------------------------------ | ------------------------------- |
| **Python 3.10+**               | Core programming language       |
| **Telegram Bot API (Telebot)** | User interaction                |
| **GigaChat API**               | AI image generation             |
| **Redis**                      | Credits, caching, rate limiting |
| **FastAPI**                    | Admin dashboard & backend       |
| **Uvicorn**                    | ASGI server                     |
| **Paymaster.ru**               | Payment processing              |
| **Base64**                     | Image decoding                  |
| **GitHub**                     | Version control                 |

---

##  System Architecture

The project consists of five main components:

1. **Telegram Bot Interface**
2. **GigaChat AI Image Generation Service**
3. **Redis In-Memory Database**
4. **FastAPI Admin Dashboard**
5. **Payment & Credit Management System**

### Image Generation Flow

1. User sends a text prompt
2. Bot checks credit balance (Redis)
3. Request sent to GigaChat API
4. Image received as Base64
5. Image decoded
6. Image sent back to user

---

##  Telegram Bot Commands

| Command    | Description         |
| ---------- | ------------------- |
| `/start`   | Start the bot       |
| `/help`    | Usage instructions  |
| `/credit`  | Show credit balance |
| `/payment` | Buy more credits    |
| `/contact` | Support information |

---

## Admin Dashboard (FastAPI)

The admin panel provides:

*  User management
*  Credit tracking
*  Image generation history

Access it via:

```
http://localhost:8090
```

---

##  Payment System

Integrated with **Paymaster.ru**, supporting:

* Visa / Mastercard / MIR
* SBP (Fast bank transfer)
* Online wallets

### Payment Flow

1. User selects a credit package
2. Payment link is generated
3. User completes payment
4. Paymaster webhook confirms transaction
5. Credits updated automatically
6. User receives confirmation in Telegram

---

##  Installation Guide

### Prerequisites

* Python 3.10+
* Redis (via WSL on Windows or native Linux)
* Telegram Bot Token (BotFather)
* GigaChat API credentials
* Paymaster.ru merchant account (optional)

---

### Installation Steps

####  Clone the repository

```bash
git clone https://github.com/slamaniabdelhafid/shorsa-ai.git
cd shorsa-ai
```

####  Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

####  Install dependencies

```bash
pip install -r requirements.txt
```



####  Start Redis

```bash
redis-server
```

####  Run the bot

```bash
python bot.py
```

####  Run the admin dashboard

```bash
uvicorn dashboard:app --reload
```


---

## License

This project is licensed under the **MIT License**.

---

## Author & Credits

* **Developer:** Slamani Abdelhafid
* **Supervisor:** Prof. R. N. Mokaev
* **Institution:** Saint Petersburg State University
* **Faculty:** Mathematics and Mechanics

