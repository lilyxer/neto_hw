CREATE DATABASE musical;

CREATE TABLE IF NOT EXISTS Genre(
    id SERIAL PRIMARY KEY,
    genre_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Artist(
    id SERIAL PRIMARY KEY,
    artist_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS GenreArtist(
    genre_id INTEGER REFERENCES Genre(id),
    artist_id INTEGER REFERENCES Artist(id),
    CONSTRAINT pk_genre_artist PRIMARY KEY(genre_id, artist_id)
);

CREATE TABLE IF NOT EXISTS Album(
    id SERIAL PRIMARY KEY,
    album_name VARCHAR(60) NOT NULL,
    release_year INTEGER CHECK(release_year > 1800 AND release_year <= EXTRACT(year from CURRENT_DATE))
);

CREATE TABLE IF NOT EXISTS AlbumArtist(
    album_id INTEGER REFERENCES Album(id),
    artist_id INTEGER REFERENCES Artist(id),
    CONSTRAINT pk_album_artist PRIMARY KEY(album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS track(
    id SERIAL PRIMARY KEY,
    track_name VARCHAR(60) NOT NULL,
    album_id INTEGER NOT NULL REFERENCES Album(id)
);

CREATE TABLE IF NOT EXISTS Collections(
    id SERIAL PRIMARY KEY,
    collections_name VARCHAR(60) NOT NULL,
    release_year INTEGER CHECK(release_year > 1800 AND release_year <= EXTRACT(year from CURRENT_DATE))
);

CREATE TABLE IF NOT EXISTS CollectionsTrack(
    collections_id INTEGER REFERENCES Collections(id),
    track_id INTEGER REFERENCES Track(id),
    CONSTRAINT pk_collections_ttrack PRIMARY KEY(collections_id, track_id)
);