#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        """Connect to the PostgreSQL database.  Returns a database connection."""
        db =  psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    delete_sql = "delete from matches"
    db, c = connect()
    c.execute(delete_sql)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    delete_sql = "delete from players"
    db, c = connect()

    c.execute(delete_sql)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    count_query = """
        select count(*) from players
        """
    db, c = connect()

    count = c.execute(count_query)
    # Uses fetchone due to one row resulting from count aggregation
    count = c.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    insert_sql = """insert into players (name) values (%s)"""
    db, c = connect()

    c.execute(insert_sql, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standing_query = """select * from standings_view"""
    # standing_query = """
    #     select players.p_id, players.name, standings.win, standings.match
    #     from players left join standings
    #     on players.p_id = standings.p_id
    #     order by win
    #     """
    # insert_sql = """
    #     insert into standings
    #     (p_id, win, match) values (%s, 0, 0)
    #     """
    db, c = connect()
    playerStandings = c.execute(standing_query)
    playerStandings = c.fetchall()
    db.close()
    print 'playerSTandings'
    print playerStandings
    # for playerStanding in playerStandings:
    #     if playerStanding[2] is None:
    #         update = c.execute(insert_sql, (playerStanding[0],))
    #         db.commit()
    # playerStandings = c.execute(standing_query)
    # playerStandings = c.fetchall()
    # db.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    update_winner_sql = """
        update standings
        set win = win + 1, match = match + 1
        where p_id = (%s)
        """
    update_loser_sql = """
        update standings
        set match = match + 1
        where p_id = (%s)"""
    db, c = connect()

    c.execute(update_winner_sql, (winner,))
    c.execute(update_loser_sql, (loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, c = connect()
    sql_count = """
        select count(name) from players"""
    count = c.execute(sql_count)
    count = c.fetchone()[0]
    if count % 2 == 0:
        results = playerStandings()
        pairings = []
        for i in range(0, len(results), 2):
            tup = (results[i][0], results[i][1], results[i+1][0], results[i+1][1])
            pairings.append(tup)
        return pairings
    else:
        return "Uneven number"
