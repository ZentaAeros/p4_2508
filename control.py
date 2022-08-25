from msilib.schema import Control
from tinydb import TinyDB, Query
import sys
import random
from model import Controller, Player, Tournament, Match, Database
from view import View

db = TinyDB("players.json")


def serialize_id_player(id_of_player):
    id_player = TinyDB("id_player.json")
    id_player.truncate()
    serialized_id_player = { "id" : id_of_player }
    id_player.insert(serialized_id_player)

def deserialize_id_player():
    id_player = TinyDB("id_player.json")
    id = id_player.all()
    for id_of_player in id:
        return id_of_player["id"]


def serialize_players(list_of_players):
    db = TinyDB("players.json")

    for player in list_of_players:
        serialize_player = {
            "id": player.id,
            "name": player.name,
            "first_name": player.first_name,
            "date_of_birth": player.date_of_birth,
            "sex": player.sex,
            "ranking": player.ranking,
            "number_of_points": player.number_of_points,
            "played_with": player.played_with,
        }

        db.insert(serialize_player)

def deserialize():
    pass

def deserialize_players():
    db = TinyDB("players.json")
    list_of_players_from_db = []
    players = db.all()

    for player in players:
        deserialized_player = Player(
            player["id"],
            player["name"],
            player["first_name"],
            player["date_of_birth"],
            player["sex"],
            player["ranking"],
            player["number_of_points"],
            player["played_with"],
        )

        list_of_players_from_db.append(deserialized_player)

    return list_of_players_from_db

def add_player():
    # Récupération des informations du nouveau joueur depuis la vue
    list_player = []
    player_form = View.create_player_form()
    id_player = deserialize_id_player()
    player = Player(
            str(id_player),
            player_form[0],
            player_form[1],
            player_form[2],
            player_form[3],
            player_form[4],
            0,
            [str(id_player)],
        )
    id_player += 1
    serialize_id_player(id_player)
    list_player.append(player)
    serialize_players(list_player)
    


def add_players_on_tournament():
    player_number = 0
    list_of_players = []
    new_player = []
    list_of_players_from_db = deserialize_players()
    while player_number < 8:
        print(f"Joueur n° {player_number}")
        user_entry = View.add_or_load_player_menu()
        if user_entry == "1":
            # Récupération des informations du nouveau joueur depuis la vue
            id_player = deserialize_id_player()
            player_form = View.create_player_form()
            player = Player(
                    str(id_player),
                    player_form[0],
                    player_form[1],
                    player_form[2],
                    player_form[3],
                    player_form[4],
                    0,
                    [str(id_player)],
                )
            id_player += 1
            serialize_id_player(id_player)
            new_player.append(player)
            list_of_players.append(player)
            player_number += 1
        elif user_entry == "2":
            entry = View.display_player_from_db(list_of_players_from_db)
            if entry == "0":
                continue
            else :
                entry = int(entry) - 1
                list_of_players.append(
                    Player(
                        list_of_players_from_db[entry].id,
                        list_of_players_from_db[entry].name,
                        list_of_players_from_db[entry].first_name,
                        list_of_players_from_db[entry].date_of_birth,
                        list_of_players_from_db[entry].sex,
                        list_of_players_from_db[entry].ranking,
                        list_of_players_from_db[entry].number_of_points,
                        list_of_players_from_db[entry].played_with
                        )
                    )

                list_of_players_from_db.pop(entry)
                
                player_number += 1

    serialize_players(new_player)
        
    return list_of_players

def add_tournament():
    # Récupération des informations de la vue
    tournament_form = View.create_tournament_form()
    tournament = Tournament(
        tournament_form["name"],
        tournament_form["place"],
        tournament_form["description"],
        add_players_on_tournament(),
    )

    return tournament

def create_pair_of_players(list_of_players):
    players_not_assigned = 0
    pair_of_players = []
    if Tournament.round_number == 1:
        # Trie les joueurs selon leur classement
        list_of_players = Player.sort_players_by_ranking(list_of_players)
        # Division du groupe : Moitié supérieure
        moitie_superieure = list_of_players[0:4]
        # Division du groupe : Moitié inférieure
        moitie_inferieure = list_of_players[4:8]

        # Jumelage des joueurs
        for moitie_sup, moitie_inf in zip(moitie_superieure, moitie_inferieure):
            pair = Match(moitie_sup, moitie_inf)
            pair_of_players.append(pair)

            # Ajout de l'ID dans la liste des parties jouées des joueurs
            moitie_inf.played_with.append(moitie_sup.id)
            moitie_sup.played_with.append(moitie_inf.id)

    else:
        # Trie les joueurs selon leur classement
        list_of_players = Player.sort_players_by_number_of_points(list_of_players)
        next_player = 1
        players_assigned = []
        # Tant que tous les joueurs ne sont pas assignés
        while players_not_assigned < len(list_of_players):
            # Si le joueur n'est pas dans la liste des joueurs assignés
            if (
                search_in_list(list_of_players[players_not_assigned].id, players_assigned)
                == False
            ):
                while next_player < 8:
                    if search_in_list(list_of_players[next_player].id, players_assigned):
                        next_player += 1
                    elif search_in_list(
                        list_of_players[players_not_assigned].id,
                        list_of_players[next_player].played_with,
                    ):
                        next_player += 1
                    else:
                        # Les joueurs assignés
                        players_assigned.append(list_of_players[next_player].id)
                        players_assigned.append(list_of_players[players_not_assigned].id)
                        pair = Match(
                            list_of_players[next_player], list_of_players[players_not_assigned]
                        )
                        # Ajout de l'ID dans la liste des parties jouées
                        list_of_players[next_player].played_with.append(
                            list_of_players[players_not_assigned].id
                        )
                        list_of_players[players_not_assigned].played_with.append(
                            list_of_players[next_player].id
                        )
                        # Ajout de la pair de joueur dans le tableau
                        pair_of_players.append(pair)
                        next_player = 0
                        break
            players_not_assigned += 1

    return pair_of_players

def assign_color_players(pair_of_players):
    assigned_colors = []
    """while pair_number < len(players):"""
    for pairs in pair_of_players:
        if random.randint(0, 5) == 2:
            pair = [
                [pairs.player1, "Blanc"],
                [pairs.player2, "Noir"],
            ]
            assigned_colors.append(pair)
        else:
            pair = [
                [pairs.player1, "Noir"],
                [pairs.player2, "Blanc"],
            ]
            assigned_colors.append(pair)

    return assigned_colors

def results(pair_of_players):
    players = []

    for pair in pair_of_players:
        user_entry = View.display_get_results_from_user(pair.player1, pair.player2)
        if user_entry == "1":
            pair.player1.number_of_points += 1
            players.append(pair.player1)
            players.append(pair.player2)

        elif user_entry == "2":
            pair.player2.number_of_points += 1
            players.append(pair.player1)
            players.append(pair.player2)

        elif user_entry == "3":
            pair.player1.number_of_points += 0.5
            pair.player2.number_of_points += 0.5
            players.append(pair.player1)
            players.append(pair.player2)

    return players

def search_in_list(tosearch, liste):
    return tosearch in liste

def start_tournament(tournament):
    controller = Controller()
    controller.list_of_players.append(tournament.players)
    Tournament.round_number = 1
    View.display_tournament(tournament)
    while Tournament.round_number < 5:
        print(f"Tour {Tournament.round_number} : ")
        controller.pair_of_players= create_pair_of_players(controller.list_of_players[0])
        assign_color_players(controller.pair_of_players)
        View.display_pairs(controller.pair_of_players)
        resultats = results(controller.pair_of_players)
        Tournament.round_number += 1
        resultats = Player.sort_players_by_number_of_points(resultats)
    View.display_resultat(resultats)


players = [
    Player("001", "Hanson", "Jason", "15061997", "M", "3", 0, ["001"]),
    Player("002", "Brown", "Joseph", "05021998", "M", "4", 0, ["002"]),
    Player("003", "Webb", "Gabriel", "14081992", "M", "8", 0, ["003"]),
    Player("004", "Sexton", "Charles", "10051965", "M", "7", 0, ["004"]),
    Player("005", "Harris", "David", "30061971", "M", "5", 0, ["005"]),
    Player("006", "Wade", "Amanda", "22101995", "F", "6", 0, ["006"]),
    Player("007", "Wagner", "Bryan", "05121995", "M", "1", 0, ["007"]),
    Player("008", "Harrison", "Matthew", "05121978", "M", "2", 0, ["008"]),
]

test = Tournament("Calaisfornia", "Calais", "Le meilleur tournoi de Calais !", players)

def list_of_players_from_db():
    players = deserialize_players()
    user_entry = View.display_player_from_db(players)
    if str(user_entry) == "0":
        start_application()
    else:
        user_entry = int(user_entry) - 1
        get_info_player(players[user_entry])

def get_info_player(player):
    user_entry = View.display_infos_player(player)
    print("test")
    if user_entry == "1":
        list_of_players_from_db()
    elif user_entry == "2":
        start_application()




def start_application():
    entry = 0
    while entry != "4":
        entry = View.main_menu()
        if entry == "1":
            tournament = add_tournament()
            start_tournament(tournament)

        elif entry == "2":
            add_player()
            entry = View.main_menu()

        elif entry == "3":
            list_of_players_from_db()
    sys.exit()

start_application()