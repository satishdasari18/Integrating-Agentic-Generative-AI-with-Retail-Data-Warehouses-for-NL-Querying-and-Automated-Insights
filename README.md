# Integrating Agentic Generative AI with Retail Data Warehouses for Natural Language Querying and Automated Insights





## 📖 Overview

This repository contains the implementation of an **agentic generative AI framework** for natural language to SQL (NL2SQL) querying over a retail data warehouse. The system enables non-technical retail professionals to query complex PostgreSQL databases using plain English, with automatic SQL generation, execution-guided refinement, and business-oriented narrative explanations.

**Key Features:**
- Schema-aware LLM prompting for accurate SQL generation
- Execution-guided agentic refinement loop for error correction
- Automated narrative generation for non-technical users
- FastAPI REST endpoint + CLI interface
- Comprehensive evaluation framework with metrics

---

## 🏗️ Architecture

The framework implements a **6-layer agentic architecture**:

1. **User Query Interface** — FastAPI REST API + CLI
2. **Schema-Aware LLM Translation** — Prompt engineering with PostgreSQL schema metadata
3. **Agentic Validation & Refinement Loop** — Execution-guided error correction
4. **PostgreSQL Execution Layer** — Query execution over Retail Rocket warehouse
5. **Insight Generation Module** — LLM-based narrative summaries
6. **Feedback & Logging Layer** — CSV logging for analysis

---

## 📊 Dataset

**Retail Rocket E-commerce Dataset** from Kaggle
- 2.7M+ user interaction events (view, add-to-cart, transaction)
- 20M+ item property records
- 1,669 category tree entries

Dataset is modeled as a star schema in PostgreSQL with:
- `fact_events` (main fact table)
- `dim_item` (item dimension)
- `dim_time` (time dimension)
- Base tables: `events`, `item_properties`, `category_tree`

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Database | PostgreSQL 14+ |
| Language | Python 3.9+ |
| LLM Runtime | Ollama (llama3:latest) |
| API Framework | FastAPI |
| Database Driver | psycopg2 |
| Data Processing | pandas |

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/satishdasari18/Integrating-Agentic-Generative-AI-with-Retail-Data-Warehouses-for-NL-Querying-and-Automated-Insights.git
cd Integrating-Agentic-Generative-AI-with-Retail-Data-Warehouses-for-NL-Querying-and-Automated-Insights
```

### 2. Install dependencies
```bash
conda create -n nl2sql python=3.9
conda activate nl2sql
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
```bash
# Create database
createdb retailrocket

# Load schema and data
psql -d retailrocket -f setup/schema.sql
python setup/load_data.py
```

### 4. Configure environment
Create `.env` file in project root:
