-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- PLAYER TABLE
-- p_id column represents unique player ID
-- name column contains player names
CREATE TABLE players
	(
		p_id SERIAL PRIMARY KEY,
		name VARCHAR(20) NOT NULL
	);

CREATE TABLE matches
	(
		match_id SERIAL PRIMARY KEY,
		winner INTEGER REFERENCES players(p_id) ON DELETE CASCADE,
		loser INTEGER REFERENCES players(p_id) ON DELETE CASCADE,
		CHECK (winner <> loser)
	);

-- STANDINGS TABLE
-- Standings table  references  player id from players table
-- Match column counts number of matches the player has gone through
-- Win column has win count
-- Losses can be determined by subtracting wins from matches (losses = wins-matches)

-- CREATE TABLE standings
-- 	(
-- 		id SERIAL PRIMARY KEY,
-- 		p_id INTEGER UNIQUE,
-- 		match INTEGER,
-- 		win INTEGER,
-- 		FOREIGN KEY (p_id) references players(p_id)
-- 	);

	CREATE VIEW standings_view AS
	SELECT players.p_id, players.name,
						COUNT(matches.winner) AS wins,
		COALESCE(SUM(matches.winner + matches.loser),0) AS matches
		FROM players LEFT JOIN matches ON players.p_id = matches.winner
		GROUP BY players.p_id
		ORDER BY wins;
