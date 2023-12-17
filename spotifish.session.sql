-- DELETE FROM profiles;
-- DELETE FROM albums;
-- DELETE FROM playlists;
-- DELETE FROM tracks;
-- DELETE FROM tracks_by_album;
-- DELETE FROM tracks_by_playlist;
-- DELETE FROM playlists_by_profile;

-- ALTER TABLE playlists
-- ADD COLUMN profile_id uuid REFERENCES profiles (profile_id) ON DELETE CASCADE;

-- ALTER TABLE administration_account
-- ADD COLUMN first_name TEXT;


-- ALTER TABLE administration_account
-- ADD COLUMN last_name TEXT;

SELECT * FROM profiles WHERE profile_type='user';

-- SELECT * FROM playlists WHERE playlist_id='0cccb6d2-411b-4372-b10d-83343a4c9ca9';




-- /* Profiles */
-- CREATE TABLE profiles(
--     profile_id uuid NOT NULL PRIMARY KEY,
--     profile_type TEXT NOT NULL,     
--     profile_privacy TEXT NOT NULL,  
--     profile_name TEXT,              
--     profile_handle TEXT NOT NULL,
--     profile_picture TEXT,
--     profile_links JSON,
--     profile_upload_timestamp TIMESTAMP,
--     profile_upload_source TEXT,
--     profile_followers_counter INT NOT NULL DEFAULT 0,
--     profile_following_counter INT NOT NULL DEFAULT 0,
--     profile_requests_counter INT DEFAULT 0,
--     profile_superuser_list UUID[],
--     profile_verification TEXT
-- );
-- CREATE INDEX ON profiles (profile_type);
-- CREATE INDEX ON profiles (profile_privacy);
-- CREATE INDEX ON profiles (profile_name);
-- CREATE UNIQUE INDEX ON profiles (profile_handle);



-- /* Playlists */
-- CREATE TABLE playlists(
--     playlist_id uuid NOT NULL PRIMARY KEY,
--     playlist_original_id TEXT,
--     playlist_name TEXT NOT NULL,
--     playlist_genre TEXT,
--     playlist_subgenre TEXT,
--     playlist_privacy TEXT NOT NULL,
--     playlist_banner TEXT,
--     playlist_description TEXT,
--     playlist_links JSON,
--     playlist_upload_timestamp TIMESTAMP,
--     playlist_upload_source TEXT,
--     playlist_likes_counter INT NOT NULL DEFAULT 0,
--     playlist_tracks_counter INT NOT NULL DEFAULT 0,
--     playlist_admin_list UUID[],
--     playlist_type TEXT,
-- ); 
-- CREATE INDEX ON playlists (playlist_privacy);
-- CREATE INDEX ON playlists (playlist_name);


-- /* Playlists by profile junction table */
-- CREATE TABLE playlists_by_profile(
--     profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     playlist_id uuid NOT NULL REFERENCES playlists(playlist_id) ON DELETE CASCADE,
--     playlist_position_string TEXT,
--     PRIMARY KEY (profile_id, playlist_id)
-- );
-- CREATE INDEX ON playlists_by_profile (playlist_position_string ASC);


-- /* albums */
-- CREATE TABLE albums(
--     album_id uuid NOT NULL PRIMARY KEY,
--     album_original_id TEXT,
--     album_name TEXT NOT NULL,
--     album_banner TEXT,
--     album_release_date TIMESTAMP,
--     album_links JSON,
--     album_upload_timestamp TIMESTAMP,
--     album_upload_source TEXT,
--     album_likes_counter INT NOT NULL DEFAULT 0,
--     album_tracks_counter INT NOT NULL DEFAULT 0,
--     profile_id uuid REFERENCES profiles (profile_id) ON DELETE CASCADE
-- ); 
-- CREATE INDEX ON albums (album_name);


-- /* Tracks */
-- CREATE TABLE tracks(
--     track_id uuid NOT NULL PRIMARY KEY,
--     track_original_id TEXT,
--     track_name TEXT NOT NULL,
--     profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     track_lyrics TEXT,
--     track_popularity INT,
--     album_id uuid NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
--     track_danceability FLOAT,
--     track_energy FLOAT,
--     track_key INT,
--     track_loudness FLOAT,
--     track_mode INT,
--     track_speechiness FLOAT,
--     track_acousticness FLOAT,
--     track_instrumentalness FLOAT,
--     track_liveness FLOAT,
--     track_valence FLOAT,
--     track_tempo FLOAT,
--     track_duration_ms INT,
--     track_language TEXT,
--     track_soundcloud_link TEXT,
--     track_upload_timestamp TIMESTAMP,
--     track_upload_source TEXT,
--     track_likes_counter INT NOT NULL DEFAULT 0,
--     track_comments_counter INT NOT NULL DEFAULT 0
-- );
-- CREATE INDEX ON tracks (track_name);
-- CREATE INDEX ON tracks (profile_id);
-- CREATE INDEX ON tracks (album_id);


-- /* Tracks by playlist */
-- CREATE TABLE tracks_by_playlist(
--     playlist_id uuid NOT NULL REFERENCES playlists(playlist_id) ON DELETE CASCADE,
--     track_id uuid NOT NULL REFERENCES tracks(track_id) ON DELETE CASCADE,
--     track_position_string TEXT NOT NULL,
--     PRIMARY KEY (playlist_id, track_id)
-- );
-- CREATE INDEX ON tracks_by_playlist (track_position_string ASC);





-- /* Tracks by album */
-- CREATE TABLE tracks_by_album(
--     album_id uuid NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
--     track_id uuid NOT NULL REFERENCES tracks(track_id) ON DELETE CASCADE,
--     track_position_string TEXT NOT NULL,
--     PRIMARY KEY (album_id, track_id)
-- );
-- CREATE INDEX ON tracks_by_album (track_position_string ASC);



-- /* Followers by profile */

-- CREATE TABLE followers_by_profile(
--     profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     follower_profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     follower_type TEXT NOT NULL,
--     follower_timestamp TIMESTAMP DEFAULT statement_timestamp(),
--     PRIMARY KEY (profile_id, follower_profile_id)
-- );
-- CREATE INDEX ON followers_by_profile (follower_type);
-- CREATE INDEX follower_timestamp_idx ON followers_by_profile (follower_timestamp DESC);

-- /* Following by profile */

-- CREATE TABLE following_by_profile(
--     profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     following_profile_id uuid NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
--     following_timestamp TIMESTAMP DEFAULT statement_timestamp(),
--     PRIMARY KEY (profile_id, following_profile_id)
-- );
-- CREATE INDEX following_timestamp_idx ON following_by_profile (following_timestamp DESC);