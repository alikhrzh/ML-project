# NU Club Finder

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://nuclubs.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

*A smart recommendation system that helps Nazarbayev University students discover student clubs that match their interests and goals.*

🔗 **Live App**: [nuclubs.streamlit.app](https://nuclubs.streamlit.app)

> **Status:** student project and working prototype. The current ranking is a
> manually weighted hybrid baseline; recommendation quality has not yet been
> validated on a labelled offline test set or through a controlled user study.

---

## Overview

NU Club Finder combines semantic search with interest-based filtering to surface the most relevant student clubs from a simple natural language query. Instead of browsing a long list manually, students describe what they're looking for and the system returns the top 5 clubs ranked by relevance.

The ranking blends two signals:

- **Semantic similarity (70%)** — how closely a club's description matches the user's query, computed via sentence embeddings and cosine similarity
- **Interest match (30%)** — how many of the user's selected interest categories overlap with the club's tagged areas

Queries can be written in **English or Russian** — a translation layer automatically handles Russian input before it reaches the embedding model.

The 70/30 weighting is a product hypothesis, not a learned or experimentally
optimal value. A planned evaluation will compare semantic-only,
interest-only, and combined baselines using a small reviewed query set.

---

## Features

- **Natural language search** — describe your ideal club experience in plain text
- **Interest area filtering** — narrow results by selecting from 12 categories (Sports, Technology, Arts, etc.)
- **Multilingual input** — Russian queries are auto-translated to English before processing
- **Query expansion** — short queries are enriched with WordNet synonyms for better recall
- **Social links** — each result card links directly to the club's Telegram and Instagram
- **Optional usage feedback** — users can explicitly opt in to sharing a search
  with a separately configured analytics endpoint

---

## How It Works

```
User query (text + selected interests)
        │
        ▼
  Russian? → Translate to English (Helsinki-NLP/opus-mt-ru-en)
        │
        ▼
  Short query? → Expand with WordNet synonyms
        │
        ▼
  Encode query with paraphrase-multilingual-MiniLM-L12-v2
        │
        ▼
  Cosine similarity vs. pre-computed club embeddings
        │
        ▼
  Blend: 0.7 × semantic_score + 0.3 × interest_match_score
        │
        ▼
  Return top 5 clubs
```

---

## Project Structure

```
ML-project/
├── app.py                          # Streamlit UI and app entry point
├── recomandation_model.py          # Scoring and ranking logic
├── club_rec_recsys.py              # Embedding, translation, similarity search
├── data/
│   ├── clubs_with_interest_areas.csv   # Club dataset with metadata
│   └── club_embeddings.npy             # Pre-computed club embeddings
├── notebooks/                      # Exploratory notebooks
├── requirements.txt
├── runtime.txt
└── setup.py
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

```bash
git clone https://github.com/alikhrzh/ML-project.git
cd ML-project

pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> **Note:** On first run the sentence-transformer and translation models will be downloaded automatically (~500MB total). This is a one-time step.

Usage feedback is disabled by default. To operate a project-controlled
analytics endpoint, set `NU_CLUB_ANALYTICS_URL` in the deployment environment.
Even when an endpoint is configured, a search is sent only after the user
selects the opt-in checkbox. The payload contains the query, selected interests,
recommended club names, and a timestamp.

### Run the lightweight tests

```bash
python -m unittest discover -s tests
```

These tests cover the pure ranking calculations without downloading the NLP
models. GitHub Actions runs them on every push and pull request.

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web interface |
| `sentence-transformers` | Multilingual sentence embeddings |
| `transformers` | Helsinki-NLP translation model |
| `keybert` | Keyword extraction |
| `scikit-learn` | Cosine similarity |
| `nltk` | WordNet query expansion |
| `pandas` / `numpy` | Data handling |
| `requests` | Optional, consent-based analytics request |

---

## Team and contribution disclosure

NU Club Finder is a collaborative student project by **Alikhan Rakhymzhan**
and **Nurdaulet**. Based on the public commit history, Alikhan contributed the
hybrid recommendation logic, interest mapping and data-cleaning iterations,
the Streamlit application, and the original analytics integration. Nurdaulet
contributed data and notebook experiments and earlier README iterations.
Commit counts are not used as a measure of effort.

Pretrained models provide translation and text embeddings; the team did not
train those foundation models. The project-specific work is the club dataset,
interest taxonomy, ranking logic, application integration, and evaluation plan.

## Known limitations

- No labelled recommendation benchmark is published yet.
- WordNet expansion can introduce unrelated senses for short or ambiguous queries.
- Russian input depends on machine translation before ranking.
- Model downloads make the first start slow and require network access.
- Club metadata and social links can become outdated and need periodic review.
- The repository does not currently declare an open-source license.
