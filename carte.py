import random
import json

#On defini un classe card pour créer notre paquet
class Card :
    def __init__(self, color, value) :
        self.value = value
        self.color = color
    #Fonction pour afficher proprement les cartes
    def show_card(self) :
        return self.value + self.color + " "

#Création d'une classe joueur
class Player :
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won = False
    #fonction pour imprimer la main du joueur
    def print_hand(self) :
        hand_string = ""
        for i in range(len(self.hand)) :
            hand_string += self.hand[i].show_card()
        print("Votre main " + hand_string)
    #fonction pour check si le joueur a gagné
    def verify_win(self):
            self.won = True
            for card in self.hand :
                #On compare tous les symboles de cartes au symbole de la 1ere carte, si y'a un different, on continue la partie
                if card.color != self.hand[0].color :
                    self.won = False
            if self.won:
                return True
#fonction pour les choix
def choice_input(message, condition, error):
    goodnumber = False
    while not goodnumber:
        try:
            number = int(input(message))
            if number in condition:
                goodnumber = True
            else:
                print(error)
        except ValueError:
            print("Pas un nombre")
    return number


#On crée des listes pour définir le noms des cartes
colors = ['♣', '♦', '♥', '♠']
values = ['As','2','3','4','5','6','7','8','9','10','Valet','Reine','Roi']

#Création du deck de référence
base_deck = [Card(color, value) for value in values for color in colors]

def init():
    #Création des joueurs,de la pioche et la défausse
    player_number = choice_input("Entrez le nombre de joueurs (max 4) : ", range(1, 5), "action invalide, veillez choisir un nombre entre 1 et 4")
    global player_list, playing_deck, pile
    player_list = []
    for i in range(player_number) :
        name = input(f"Entrez le nom du {i+1}e joueur : ")
        player_list.append(Player(name))
        i += 1
    playing_deck = []
    pile = []

    #On met les cartes dans les mains et la pioche
    playing_deck = random.choices(base_deck, k=52)
    for player in player_list :
        for i in range(10) :
            player.hand.append(playing_deck.pop(i))

def save():
    #Une tentative de sauvegarde a été faite mais par manque de temps et un bug que je n'arrive pas à corriger je n'y arrive pas (si vous tu sais comment mettre des objets python dans un json je suis pas contre >w<)
    json_object =[]
    for player in player_list:
        json_object.append({"name" : player.name, "hand" : player.hand})
    with open("save.json", "w") as my_file:
        json.dump(json_object, my_file, indent=4)
        

init()
#game loop
while True :
    for player in player_list :
        #On annonce le joueur courant
        print(f"Au tour de {player.name}")
        #On affiche la 1ere carte de la pile si elle n'est pas vide
        if pile != []:
            print("La 1ere carte de la defausse est " + pile[-1].show_card())
        else :
            print("La defausse est vide")
        #On mélange la pile a la pioche si elle est vide
        if playing_deck == []:
            playing_deck = random.choices(pile, k=len(pile))
            pile = []
        player.print_hand()
        #Choix de l'action (l'endroit ou on pioche)
        action_choice = choice_input("1 pour piocher dans la pioche, 2 pour piocher dans la defausse : ", [1, 2], "Action invalide, veillez choisir 1 ou 2")
        if action_choice == 1:
            #on enlève une carte de la pioche pour la mettre dans la main du joueur
            player.hand.append(playing_deck.pop(0))
        #Sécurité pour empecher le joueur de piocher dans une défausse vide
        elif pile ==[] :
            print("La pile est vide, vous piochez dans la pioche")
            #on enlève une carte de la pioche pour la mettre dans la main du joueur
            player.hand.append(playing_deck.pop(0))
        elif action_choice == 2 and pile != [] :
            #on enlève une carte de la défausse pour la mettre dans la main du joueur
            player.hand.append(playing_deck.pop(-1))
        player.print_hand()
        #Choix de la carte a enlvever
        card_remove = choice_input("Choissez la carte a enlever : ", range(0, 11), "Action invalide, veillez choisir un nombre entre 0 et 10")
        pile.append(player.hand.pop(card_remove))
        #On vérifie si le joueur courant a gagné
        if player.verify_win():
            print(f"{player.name} à gagné !")
            break
    if player.verify_win():
        #on vérifie si le joueur a gagner pour lui demander si il veux rejouer
        choice_replay = choice_input("1 pour rejouer, 2 pour quitter", [1,2], "Action invalide, veillez choisir 1 ou 2")
        if choice_replay == 1:
            init()
            continue
        else :
            break
    else: 
        #on demande aux joueurs si ils veulent continuer la partie ou quitter et sauvegarder (save qui fonctionne pas)
        choice_continue = choice_input("1 pour continuer, 2 pour sauvegarder et quitter", [1,2], "Action invalide, veillez choisir 1 ou 2")
        if choice_continue == 1 :
            continue
        else :
#           save()
            break
