# NU Club Finder

NU Club Finder is a student project that helps Nazarbayev University students
discover clubs from a free-text query and selected interest areas. It is a
working prototype, not a validated recommender system.

## Problem

Club information is spread across descriptions and social links, so students
must browse many options manually. This project ranks a local catalogue of NU
clubs and returns five candidates that may match a student's interests.

## Approach

The current ranking is a manually weighted hybrid baseline:

1. Russian queries are translated to English with
   `Helsinki-NLP/opus-mt-ru-en`.
2. Short queries are expanded with WordNet synonyms.
3. `paraphrase-multilingual-MiniLM-L12-v2` produces a query embedding.
4. Cosine similarity compares the query with pre-computed club embeddings.
5. The final score is `0.7 * semantic_similarity + 0.3 * interest_match`.

The 70/30 split is a product hypothesis. It was not learned from interaction
data or selected through an offline benchmark.

## Results

No recommendation-quality metric is reported yet. The repository contains
example queries, but they do not include reviewed relevance labels, so they
cannot support Recall@K, NDCG@K, or a defensible comparison with a baseline.

- Ranking calculation tests: **4/4 passing**.
- Offline ranking result: **[TODO: offline ranking metric against semantic-only
  and simple popularity/random baselines]**.
- Public demo: **[TODO: public demo URL]**.

The previously used `nuclubs.streamlit.app` address currently redirects to a
Streamlit sign-in page and is therefore not presented as a public demo.

## Interface preview

**[TODO: add a Streamlit screenshot after the public deployment is verified]**

## How to run

Python 3.11 is declared in `runtime.txt`.

```bash
git clone https://github.com/alikhrzh/ML-project.git
cd ML-project
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the embedding and translation models. Usage analytics
are disabled unless `NU_CLUB_ANALYTICS_URL` is configured, and a search is sent
only after the user explicitly opts in.

Run the lightweight ranking tests without downloading the NLP models:

```bash
python -m unittest discover -s tests
```

Deployment instructions are in
[`docs/deploy-streamlit.md`](docs/deploy-streamlit.md).

## Project structure

```text
app.py                         Streamlit interface
ranking.py                     Pure hybrid-scoring functions
recomandation_model.py         Recommendation orchestration
club_rec_recsys.py             Translation, embeddings, and retrieval
data/                          Club metadata and pre-computed embeddings
notebooks/                     Exploration and prototype notebooks
tests/                         Lightweight ranking tests
```

## Limitations

- There is no labelled recommendation benchmark or controlled user study.
- The hybrid weight is manually chosen and may not generalize.
- WordNet expansion can add unrelated meanings to ambiguous queries.
- Russian input depends on machine translation before ranking.
- The first start requires network access and substantial model downloads.
- Club metadata and social links need periodic review.
- The repository does not currently declare an open-source license.

## Roadmap

- Label a small query-to-club relevance set with at least two reviewers.
- Compare semantic-only, interest-only, hybrid, and simple popularity/random
  baselines using Recall@5 and NDCG@5.
- Publish a public, unauthenticated Streamlit deployment and screenshot.
- Add an explicit user-feedback signal without collecting queries by default.
- Pin compatible dependency versions after the deployment environment is
  reproduced.

## Team and model disclosure

NU Club Finder is a collaborative student project by **Alikhan Rakhymzhan**
and **Nurdaulet**. Based on the public commit history, Alikhan contributed the
hybrid recommendation logic, interest mapping and data-cleaning iterations,
the Streamlit application, and the original analytics integration. Nurdaulet
contributed data and notebook experiments and earlier README iterations.
Commit counts are not used as a measure of effort.

The project uses pretrained translation and sentence-embedding models; the
team did not train those foundation models. AI assistants may have supported
documentation and implementation review, while the repository authors remain
responsible for the code, evaluation claims, and final decisions.
