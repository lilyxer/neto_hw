CREATE DATABASE musical;

-- \c musical;

CREATE TABLE IF NOT EXISTS genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL);

CREATE TABLE IF NOT EXISTS artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(50) NOT NULL UNIQUE);

CREATE TABLE IF NOT EXISTS genre_artist (
    genre_artist SERIAL NOT NULL PRIMARY KEY,
    genre_id INT,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR(50) NOT NULL,
    release_year INTEGER CHECK(release_year > 1800 AND release_year <= EXTRACT(year from CURRENT_DATE)));

CREATE TABLE IF NOT EXISTS album_artist (
    genre_artist SERIAL PRIMARY KEY,
    album_id INT,
    FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    track_name VARCHAR(50) NOT NULL,
    track_time time NOT NULL,
    album_id INT,
    FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL PRIMARY KEY,
    collection_name VARCHAR(50) NOT NULL,
    release_year INTEGER CHECK(release_year > 1800 AND release_year <= EXTRACT(year from CURRENT_DATE)));

CREATE TABLE IF NOT EXISTS track_collections (
    track_collections_id SERIAL PRIMARY KEY,
    track_id INT,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    collection_id INT,
    FOREIGN KEY (collection_id) REFERENCES collections(collection_id) ON DELETE CASCADE);