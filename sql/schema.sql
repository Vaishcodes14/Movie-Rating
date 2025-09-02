-- 🎬 Movie Rating Database Schema
-- Filtering | Sorting | Aggregations
-- GROUP BY | AVG | COUNT
-- Foundational logic for IMDb-type platforms ⭐

-- Drop existing tables (for reruns)
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

-- Movies table
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER
);

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT
);

-- Ratings table (relationship between users & movies)
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL CHECK(rating >= 0 AND rating <= 5),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

-- ✅ Sample Queries
-- Top movies by average rating
-- SELECT m.title, AVG(r.rating) as avg_rating
-- FROM ratings r
-- JOIN movies m ON r.movie_id = m.id
-- GROUP BY m.id
-- ORDER BY avg_rating DESC;

-- Top movies by number of ratings
-- SELECT m.title, COUNT(r.rating) as total_ratings
-- FROM ratings r
-- JOIN movies m ON r.movie_id = m.id
-- GROUP BY m.id
-- ORDER BY total_ratings DESC;
