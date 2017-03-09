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

-- MATCHES TABLE
-- match_id column represents unique ID record for match
-- winner column refers to player who won match
-- loser column refers to player who lost match
CREATE TABLE matches
	(
		match_id SERIAL PRIMARY KEY,
		winner INTEGER REFERENCES players(p_id) ON DELETE CASCADE,
		loser INTEGER REFERENCES players(p_id) ON DELETE CASCADE,
		CHECK (winner <> loser)
	);


--Standings VIEW
--Utilizes information in existing tables
--Provides the current standings for all players in the tournament
--Returns player_id, player name, number of matches won, total matches played
CREATE VIEW standings_view AS
	SELECT players.p_id AS pid,
		players.name AS name,
		COUNT(matches.winner) AS wins,
		COALESCE((SELECT COUNT(*)
			FROM matches
			WHERE matches.winner = players.p_id
			OR matches.loser = players.p_id), 0) AS match
	FROM players LEFT JOIN matches ON matches.winner = players.p_id
		GROUP BY players.p_id
		ORDER BY wins;
