from tinydb import TinyDB, Query
from audioop import reverse
import random


class Player:
    def __init__(
        self,
        id,
        name,
        first_name,
        date_of_birth,
        sex,
        ranking,
        number_of_points,
        played_with,
    ):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.number_of_points = number_of_points
        self.played_with = played_with

    def __repr__(self):
        return (
            self.id,
            self.name,
            self.first_name,
            self.date_of_birth,
            self.sex,
            self.ranking,
            self.number_of_points,
            self.played_with,
        )

    def name_of_player(self):
        return f"{self.first_name} {self.name}"

    def sort_players_by_ranking(players_sorting):
        return sorted(players_sorting, key=lambda player: player.ranking)

    def sort_players_by_number_of_points(players_sorting):
        return sorted(
            players_sorting,
            key=lambda player: (player.number_of_points, player.ranking),
            reverse=True,
        )

    def __str__(self):
        return f"{self.first_name} {self.name}"


class Tournament:
    def __init__(self, name, place, description, players):
        self.name = name
        self.place = place
        self.description = description
        self.players = players
        self.round_number = 0

    def __str__(self):
        return f"Nom du tournoi : {self.name}, Lieu : {self.place}"


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def __str__(self):
        return f"{self.player1.__repr__()} vs {self.player2.__repr__()}"


class Round(Match):
    def __init__(self, list_of_matchs):
        self.list_of_matchs = list_of_matchs


class Database:
    def remove_player_from_db(to_remove):
        db = TinyDB("players.json")
        db.all()
        player_to_delete = Query()
        db.remove(player_to_delete.id == to_remove)


class Controller:
    list_of_matchs = []
    pair_of_players = []
    list_of_players = []
    list_of_players_from_db = []
