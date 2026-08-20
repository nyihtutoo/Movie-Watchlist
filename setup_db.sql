-- Database setup for the Movie Watchlist app.
-- Run this once as the PostgreSQL superuser (postgres):
--   psql -U postgres -f setup_db.sql
-- IMPORTANT: replace the placeholder password below with a strong password,
-- and set the SAME value as DB_PASSWORD in your .env file.

-- CREATEDB lets Django create/drop the temporary test database (manage.py test).
CREATE USER movie_user WITH PASSWORD 'change_me_to_match_env' CREATEDB;
CREATE DATABASE movie_watchlist OWNER movie_user;
GRANT ALL PRIVILEGES ON DATABASE movie_watchlist TO movie_user;

-- Django 6 / PostgreSQL: ensure the app user can create objects in the
-- public schema of the new database.
\connect movie_watchlist
GRANT ALL ON SCHEMA public TO movie_user;
