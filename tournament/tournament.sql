-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players
	(
		p_id SERIAL PRIMARY KEY,
		name TEXT
	);

CREATE TABLE standings
	(
		id SERIAL PRIMARY KEY,
		p_id INTEGER UNIQUE,
		match INTEGER,
		win INTEGER,
		FOREIGN KEY (p_id) references players(p_id)
	);