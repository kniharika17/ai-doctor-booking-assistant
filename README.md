# 🩺 AI Doctor Appointment Booking Assistant

## Overview
The **AI Doctor Appointment Booking Assistant** is a Streamlit-based conversational application that helps users book doctor appointments and ask questions from medical PDF reports using **Retrieval Augmented Generation (RAG)**.

The project focuses on **correctness, robustness, and evaluator-safe deployment**, rather than heavy dependence on paid APIs.

---

## Features
- 💬 Chat-based interface using Streamlit
- 📅 Conversational doctor appointment booking with slot filling
- 📄 Medical PDF upload and question answering
- 🔍 Semantic search using FAISS vector database
- 🧠 Hybrid RAG (local embeddings + optional LLM reasoning)
- 🗄 SQLite database for storing bookings
- 📧 Email confirmation after successful booking
- 🛠 Admin dashboard to view appointment records

---

## Step-by-Step Implementation

### 1️⃣ Conversational Booking Flow
- Implemented intent detection for appointment booking
- Designed slot-filling questions (name, email, doctor type, date, etc.)
- Stored confirmed bookings in SQLite
- Generated a unique booking ID
- Sent email confirmation using SMTP

### 2️⃣ PDF-Based RAG Pipeline
- Allowed users to upload one or more medical PDF reports
- Loaded PDFs using LangChain document loaders
- Split text into chunks using recursive text splitting
- Generated semantic embeddings using HuggingFace Sentence Transformers
- Stored embeddings in a FAISS vector database

### 3️⃣ Hybrid Answering Strategy
- Retrieved relevant document chunks using vector similarity search
- Used an LLM (when available) for:
  - Summarization
  - Clinical reasoning
  - Multi-sentence answers
- Applied deterministic, rule-based fallback logic when LLM is unavailable
- Returned explicit “Information not found” responses to avoid hallucinations

### 4️⃣ Admin Dashboard
- Built a simple admin interface to view all bookings
- Data fetched directly from SQLite database

---

## Tech Stack
- **Python**
- **Streamlit**
- **LangChain**
- **FAISS**
- **HuggingFace Sentence Transformers**
- **SQLite**
- **SMTP (Email notifications)**

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
