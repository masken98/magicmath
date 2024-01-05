import numpy as np

decks = [
    ("RDW", [0.5, 0.7, 0.3, 0.5], 2),
    ("UW", [0.3, 0.5, 0.7, 0.5], 2),
    ("BG", [0.7, 0.3, 0.5, 0.5], 2),
    ("Merfolk", [0.5, 0.5, 0.5, 0.5], 2),
]

def match_sim(deck1, deck2):
    '''Simulates a match between two decks

    param deck1: deck1 winrate against deck2
    param deck2: deck2 winrate against deck1

    returns: 1 if deck1 wins, 0 if deck2 wins
    '''
    if deck1 == None:
        return 0
    elif deck2 == None:
        return 1
    else:
        r = np.random.random()
        if r < deck1:
            return 0
        else:
            return 1

def generate_matchups(decks: list):
    ''' Generates a list of matchups for a round

    param decks: list of decks to generate matchups for. Should be on the form (deck_name, wins, losses)

    returns: list of matchups
    '''
    matchups = []
    grouped_players = {}
    for deck in decks:
        wins = deck[2]
        if wins not in grouped_players:
            grouped_players[wins] = []
        grouped_players[wins].append(deck)
    
    for wins in grouped_players:
        players = grouped_players[wins]
        while len(players) > 1:
            player1 = players.pop()
            player2 = players.pop()
            matchups.append((player1, player2))
        if len(players) == 1:
            matchups.append((players[0], None))
        
    return matchups

def index_of(key, list: list):
    '''Returns the index of a deck in the decks list

    param key: key to search for
    param list: list of decks to search. Assumes the string has index 0

    returns: index of key in list
    '''
    for i in range(len(list)):
        if list[i][0] == key:
            return i
    #TODO: maybe should throw error
    return None

def deck_initializer(lst: list):
    '''Initializes the player records for a tournament

    param decks: list of decks to initialize

    returns: list of tuples (player_id, deck_name, wins, losses)
    '''
    player_records = []
    for i in range(len(lst)):
        if len(lst) == 0:
            break
        deck = lst[i] 
        for _ in range(deck[2]):
            player_id = np.random.randint(1000000)
            player_records.append([player_id, deck[0], 0, 0])

    return player_records

def tournament_sim(decks: list, rounds: int =3):
    '''Simulates a tournament between decks

    param decks: list of decks to simulate
    param rounds: number of rounds to simulate

    returns: list of decks sorted by final placement
    '''
    # Initialize player records
    player_records = deck_initializer(decks)   # list of tuples (deck, wins, losses)  

    # Simulate tournament
    for round in range(rounds):
        matchups = generate_matchups(player_records)

        for matchup in matchups:
            #TODO: Handle byes and pair downs
            deck1 = index_of(matchup[0][0], decks)
            deck2 = index_of(matchup[1][0], decks)
            result = match_sim(deck1, deck2)
            
            winner = index_of(matchup[result][0], player_records)
            loser = index_of(matchup[1 - result][0], player_records)
            if result == 0:
                player_records[winner][2] += 1
                player_records[loser][3] += 1
            else:
                player_records[winner][3] += 1
                player_records[loser][2] += 1
            
    return sorted(player_records, key=lambda x: x[2], reverse=True)


results = tournament_sim(decks)
print(results)



