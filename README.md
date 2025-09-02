# Movie Rating Database + ML


This project implements a foundational **movie rating database** (like IMDb logic) and extends it with **machine learning**:


- SQL analytics: `GROUP BY`, `AVG`, `COUNT`, filtering, sorting
- Content‑based recommendations (movie similarity by genre/year)
- Collaborative filtering with **TruncatedSVD** (matrix factorization)
- Rating prediction with **Linear Regression** on simple features


## Quickstart


```bash
# 1) Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate


# 2) Install dependencies
pip install -r requirements.txt


# 3) Run the end-to-end demo
python app.py
