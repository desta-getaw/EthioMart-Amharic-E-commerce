# EthioMart FinTech Engine 🚀

![Project Banner](https://via.placeholder.com/1200x400?text=EthioMart+FinTech+Engine+%7C+Telegram+Data+to+Loan+Decisions)

Transform Ethiopian Telegram e-commerce data into intelligent vendor scoring for micro-lending decisions.

---

## 📌 Table of Contents

- [EthioMart FinTech Engine 🚀](#ethiomart-fintech-engine-)
  - [📌 Table of Contents](#-table-of-contents)
  - [🌍 Project Overview](#-project-overview)
  - [✨ Key Features](#-key-features)
    - [📊 Data Processing](#-data-processing)
    - [🤖 Machine Learning](#-machine-learning)
    - [📈 Analytics Engine](#-analytics-engine)
  - [🏗 Technical Architecture](#-technical-architecture)

---

## 🌍 Project Overview

This project addresses **EthioMart's challenge** of decentralized Telegram-based commerce in Ethiopia by:

1. **Centralizing Vendor Data**: Aggregating product listings from multiple Telegram channels.
2. **Structured Entity Extraction**: Identifying business-critical information (e.g. product, price, location) from Amharic messages.
3. **Vendor Assessment**: Scoring vendors using real-world KPIs for micro-loan eligibility.

💼 **Business Impact**: Enables EthioMart to offer capital to high-potential vendors using actual performance data — improving access to micro-finance.

---

## ✨ Key Features

### 📊 Data Processing

- ✅ Multi-Channel Ingestion: Scrapes 5+ Ethiopian Telegram e-commerce channels.
- 🧠 Amharic NLP Pipeline: Preprocessing tailored for Amharic and mixed-language messages.
- 🖼️ Multi-Modal Input: Supports both text and images with OCR integration.

### 🤖 Machine Learning

- 📌 Fine-Tuned NER Models:
  - `XLM-Roberta`
  - `mBERT`
  - `bert-tiny-amharic`
- 💬 Model Interpretability: SHAP and LIME support for explainable ML.
- 🧪 Performance Benchmarking: Compares multiple model architectures.

### 📈 Analytics Engine

- 📊 12+ Vendor KPIs:
  - Posting frequency (weekly/monthly)
  - Average price points
  - Customer engagement scores
- 🧮 Dynamic Scoring System: Weight-adjustable metrics tailored for lending eligibility.

---

## 🏗 Technical Architecture

```mermaid
graph TD
    A[Telegram Channels] --> B[Data Ingestion]
    B --> C[Amharic Text Processing]
    C --> D[NER Model Training]
    D --> E[Entity Database]
    E --> F[Vendor Analytics]
    F --> G[Scorecard Generation]
    G --> H[Loan Decision Dashboard]
