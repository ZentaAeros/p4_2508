from unicodedata import name


class View:
    def main_menu():
        print()
        print("1. Créer un tournoi")
        print("2. Ajouter un joueur")
        print("3. Voir tous les joueurs")
        print("4. Quitter l'application")
        response = input()

        return response

    def create_player_form():
        name = input("Nom : ")
        first_name = input("Prénom : ")
        date_of_birth = input("Date de naissance : ")
        sex = input("Genre ? : ")
        ranking = input("Classement du joueur : ")
        print()

        return name, first_name, date_of_birth, sex, ranking

    def create_tournament_form():
        name = input("Entrez le nom du tournoi : ")
        place = input("Indiquez le lieu du tournoi : ")
        description = input("Ajoutez une description : ")

        return {"name": name, "place": place, "description": description}

    def display_get_results_from_user(player1, player2):
        print()
        print(f"Qui est le vainqueur de la partie : ")
        print(f"1. {player1}")
        print(f"2. {player2}")
        print("3. Les joueurs sont à égalités")
        return input()

    def add_or_load_player_menu():
        print("1. Ajouter un nouveau joueur")
        print("2. Charger un joueur")
        return input()

    def display_tournament(tournament):
        print(f"Début du tounoi {tournament.name} à 04:00")
        print(f"Lieu du tournoi : {tournament.place}")
        print(f"Description du tournoi : {tournament.description}")
        print()

    def display_pairs(pair_of_players):
        x = 0
        for pair in pair_of_players:
            print(
                f"{pair.player1} vs {pair.player2}"
            )
            input()
            x += 1

    def display_resultat(resultats):
        for resultat in resultats:
            print(f"{resultat.name_of_player()} a {resultat.number_of_points} points !")
        print()

    def display_player_from_db(players):
        number_player = 1
        print("0 : Revenir en arrière")
        for player in players:
            print(f"{number_player} : {player}")
            number_player += 1
        return input()
    
    def display_infos_player(player):
        print()
        print(f"Nom : {player.name}")
        print(f"Prénom : {player.first_name}")
        print(f"Date de naissance : {player.date_of_birth}")
        print(f"Genre : {player.sex}")
        print(f"Classement : {player.ranking}")
        print()
        print("1. Retour à la liste des joueurs")
        print("2. Menu principal")
        
        return input()



"""x = 0
print("Quel joueur souhaitez-vous ajouter ?")
print("0 : Retour en arrière")
while x < len(list_of_players_from_db):
    print(f"{x+1} : {list_of_players_from_db[x]}")
    x += 1
entry = input()"""