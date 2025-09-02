import sqlite3
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Database Setup
# -----------------------------
def create_connection():
    conn = sqlite3.connect("data/movie.db")
    return conn

def create_schema(conn):
    schema = """
    DROP TABLE IF EXISTS movies;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS ratings;

    CREATE TABLE movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        year INTEGER
    );

    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        country TEXT
    );

    CREATE TABLE ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        rating REAL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );
    """
    conn.executescript(schema)
    conn.commit()

def seed_data(conn):
    movies = [
        ("Inception", "Sci-Fi", 2010),
        ("The Dark Knight", "Action", 2008),
        ("Interstellar", "Sci-Fi", 2014),
        ("3 Idiots", "Comedy", 2009),
        ("Dangal", "Drama", 2016),
        ("Avengers: Endgame", "Action", 2019),
        ("PK", "Comedy", 2014),
        ("Parasite", "Thriller", 2019),
        ("The Matrix", "Sci-Fi", 1999),
        ("Titanic", "Romance", 1997),
    ]

    users = [
        ("Alice", "USA"),
        ("Bob", "India"),
        ("Charlie", "UK"),
        ("David", "India"),
        ("Eva", "Germany"),
    ]

    ratings = [
        (1, 1, 5), (1, 2, 4), (1, 3, 5),
        (2, 4, 5), (2, 5, 4), (2, 6, 3),
        (3, 1, 4), (3, 7, 5), (3, 8, 5),
        (4, 2, 5), (4, 5, 5), (4, 9, 4),
        (5, 3, 4), (5, 6, 5), (5, 10, 4),
    ]

    conn.executemany("INSERT INTO movies(title, genre, year) VALUES (?, ?, ?)", movies)
    conn.executemany("INSERT INTO users(name, country) VALUES (?, ?)", users)
    conn.executemany("INSERT INTO ratings(user_id, movie_id, rating) VALUES (?, ?, ?)", ratings)
    conn.commit()

# -----------------------------
# SQL Analytics
# -----------------------------
def run_sql_queries(conn):
    print("\n🎥 Top Movies by Avg Rating:")
    q1 = """
    SELECT m.title, AVG(r.rating) as avg_rating
    FROM ratings r
    JOIN movies m ON r.movie_id = m.id
    GROUP BY m.id
    ORDER BY avg_rating DESC
    LIMIT 5;
    """
    print(pd.read_sql(q1, conn))

    print("\n🔝 Top Movies by Number of Ratings:")
    q2 = """
    SELECT m.title, COUNT(r.rating) as rating_count
    FROM ratings r
    JOIN movies m ON r.movie_id = m.id
    GROUP BY m.id
    ORDER BY rating_count DESC
    LIMIT 5;
    """
    print(pd.read_sql(q2, conn))

    print("\n🎬 Best Action Movies (Filtering & Sorting):")
    q3 = """
    SELECT m.title, AVG(r.rating) as avg_rating
    FROM ratings r
    JOIN movies m ON r.movie_id = m.id
    WHERE m.genre = 'Action'
    GROUP BY m.id
    ORDER BY avg_rating DESC;
    """
    print(pd.read_sql(q3, conn))

# -----------------------------
# Machine Learning
# -----------------------------
def prepare_matrix(conn):
    df = pd.read_sql("SELECT * FROM ratings", conn)
    pivot = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return pivot

def content_based(conn, movie_id):
    df = pd.read_sql("SELECT * FROM movies", conn)
    pivot = pd.get_dummies(df[["genre", "year"]])
    similarity = cosine_similarity(pivot)
    sim_scores = list(enumerate(similarity[movie_id - 1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:4]
    print("\n🎭 Content-Based Recommendations for Movie ID", movie_id)
    for idx, score in sim_scores:
        print(f"- {df.iloc[idx]['title']} (Score: {score:.2f})")

def collaborative_filtering(pivot, user_id):
    svd = TruncatedSVD(n_components=2)
    latent = svd.fit_transform(pivot)
    user_vecs = latent[user_id - 1]
    scores = np.dot(user_vecs, svd.components_)
    recommendations = np.argsort(-scores)[:3]
    print(f"\n🤝 Collaborative Filtering Recs for User {user_id}:")
    for r in recommendations:
        print(f"- Movie ID {pivot.columns[r]}")

def regression_prediction(pivot, user_id, movie_id):
    X, y = [], []
    for u in range(pivot.shape[0]):
        for m in range(pivot.shape[1]):
            if pivot.iloc[u, m] > 0:
                X.append([u, m])
                y.append(pivot.iloc[u, m])
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict([[user_id - 1, movie_id - 1]])
    print(f"\n🔮 Predicted Rating for User {user_id} on Movie {movie_id}: {pred[0]:.2f}")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    conn = create_connection()
    create_schema(conn)
    seed_data(conn)

    # Run SQL examples
    run_sql_queries(conn)

    # Prepare pivot matrix
    pivot = prepare_matrix(conn)

    # Run ML examples
    content_based(conn, 1)           # Content-based for Inception
    collaborative_filtering(pivot, 2) # Collab filtering for User 2
    regression_prediction(pivot, 3, 5) # Regression for User 3 on Movie 5

    conn.close()
