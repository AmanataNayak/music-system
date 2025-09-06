CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Auto-update updated_at on changes
CREATE OR REPLACE FUNCTION
update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE artists (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    country VARCHAR(100),
    debut_year INT,
    created_ay TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_artists_updated_at
BEFORE UPDATE ON artists
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE albums (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    release_date DATE,
    genre VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER update_albums_updated_at
BEFORE UPDATE ON albums
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE songs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    album_id UUID REFERENCES albums(id) ON DELETE SET NULL,
    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    duration INT NOT NULL, -- in seconds
    language VARCHAR(50),
    release_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_songs_updated_at
BEFORE UPDATE ON songs
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE playlists (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_playlists_updated_at
BEFORE UPDATE ON playlists
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE playlist_songs (
    playlist_id UUID REFERENCES playlists(id) ON DELETE CASCADE,
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id)
);

CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    favorite_genres TEXT[],
    favorite_artists UUID[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER update_user_preferences_updated_at
BEFORE UPDATE ON user_preferences
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE song_embeddings (
    song_id UUID PRIMARY KEY REFERENCES songs(id) ON DELETE CASCADE,
    embedding VECTOR(128), -- pgvector extension required
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER update_song_embeddings_updated_at
BEFORE UPDATE ON song_embeddings
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE similar_songs (
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    similar_song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    similarity_score FLOAT CHECK (similarity_score BETWEEN 0 AND 1),
    PRIMARY KEY (song_id, similar_song_id)
);

CREATE TABLE user_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    event_type VARCHAR(50) CHECK (event_type IN ('play', 'like', 'skip')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_user_events_updated_at
BEFORE UPDATE ON user_events
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE user_recommendations (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    score FLOAT CHECK (score >= 0),
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id)
);

CREATE TABLE genres (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_genres_updated_at
BEFORE UPDATE ON genres
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION vector;


CREATE INDEX idx_songs_title ON songs USING gin(to_tsvector('english', title));
CREATE INDEX idx_albums_title ON albums USING gin(to_tsvector('english', title));
CREATE INDEX idx_artists_name ON artists USING gin(to_tsvector('english', name));



CREATE TABLE audio_variants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    storage_key TEXT NOT NULL,              -- e.g. s3://bucket/tracks/{song_id}/128.mp3
    cdn_path TEXT,                          -- e.g. /tracks/{song_id}/128.mp3
    codec VARCHAR(20) NOT NULL,             -- mp3 | aac
    bitrate_kbps INT NOT NULL,              -- 64 | 128 | 256 ...
    sample_rate INT,                        -- e.g. 44100
    channels INT,                           -- 2
    duration_seconds INT,                   -- (redundant but convenient)
    file_size_bytes BIGINT,
    sha256 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_audio_variants_updated_at
BEFORE UPDATE ON audio_variants
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();