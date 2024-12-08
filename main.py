
import tkinter as tk
from tkinter import messagebox
import random

class PokemonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Combat Pokémon - Types, Potions et Changement")

        # Équipes des joueurs avec types et attaques uniques
        self.player_team = [
            {"name": "Pikachu", "hp": 100, "max_hp": 100, "type": "Électrique", "attacks": {"Éclair": (15, 25), "Tonnerre": (20, 35)}},
            {"name": "Bulbasaur", "hp": 120, "max_hp": 120, "type": "Plante", "attacks": {"Fouet Lianes": (10, 20), "Lance-Soleil": (25, 40)}},
            {"name": "Squirtle", "hp": 110, "max_hp": 110, "type": "Eau", "attacks": {"Pistolet à Eau": (15, 25), "Hydrocanon": (20, 40)}},
            {"name": "Charmander", "hp": 90, "max_hp": 90, "type": "Feu", "attacks": {"Flammèche": (15, 20), "Lance-Flammes": (25, 35)}},
            {"name": "Jigglypuff", "hp": 130, "max_hp": 130, "type": "Fée", "attacks": {"Berceuse": (0, 0), "Éclat Magique": (20, 30)}},
            {"name": "Eevee", "hp": 100, "max_hp": 100, "type": "Normal", "attacks": {"Charge": (10, 15), "Coup de Tête": (15, 25)}}
        ]
        self.enemy_team = [
            {"name": "Rattata", "hp": 100, "max_hp": 100, "type": "Normal", "attacks": {"Charge": (10, 15), "Morsure": (15, 20)}},
            {"name": "Pidgey", "hp": 90, "max_hp": 90, "type": "Vol", "attacks": {"Cru-Aile": (10, 20), "Tornade": (15, 25)}},
            {"name": "Meowth", "hp": 110, "max_hp": 110, "type": "Normal", "attacks": {"Griffe": (15, 25), "Coup Bas": (10, 20)}},
            {"name": "Zubat", "hp": 100, "max_hp": 100, "type": "Poison", "attacks": {"Vampirisme": (10, 15), "Onde Folie": (5, 10)}},
            {"name": "Sandshrew", "hp": 120, "max_hp": 120, "type": "Sol", "attacks": {"Jet de Sable": (10, 20), "Séisme": (25, 40)}},
            {"name": "Koffing", "hp": 130, "max_hp": 130, "type": "Poison", "attacks": {"Gaz Toxique": (5, 15), "Bombe Acide": (15, 30)}}
        ]

        # Pokémon actifs
        self.current_player_pokemon = self.player_team[0]
        self.current_enemy_pokemon = self.enemy_team[0]

        # Système de potions
        self.potions = 3
        self.potion_heal_amount = 30

        # Interface utilisateur
        self.attack_buttons = []  # Stocke les boutons d'attaque
        self.create_widgets()

    def create_widgets(self):
        # Affichage du Pokémon du joueur
        self.player_label = tk.Label(self.root, text=f"{self.current_player_pokemon['name']} (HP: {self.current_player_pokemon['hp']})", font=("Arial", 16))
        self.player_label.pack(pady=10)

        self.player_hp_bar = tk.Canvas(self.root, width=200, height=20, bg="grey")
        self.player_hp_bar.pack(pady=5)

        # Affichage du Pokémon ennemi
        self.enemy_label = tk.Label(self.root, text=f"{self.current_enemy_pokemon['name']} (HP: {self.current_enemy_pokemon['hp']})", font=("Arial", 16))
        self.enemy_label.pack(pady=10)

        self.enemy_hp_bar = tk.Canvas(self.root, width=200, height=20, bg="grey")
        self.enemy_hp_bar.pack(pady=5)

        # Boutons pour chaque attaque
        self.update_attack_buttons()

        # Bouton pour changer de Pokémon
        self.switch_button = tk.Button(self.root, text="Changer de Pokémon", command=self.switch_pokemon, font=("Arial", 14))
        self.switch_button.pack(pady=10)

        # Bouton pour utiliser une potion
        self.potion_button = tk.Button(self.root, text=f"Potion ({self.potions})", command=self.use_potion, font=("Arial", 14))
        self.potion_button.pack(pady=10)

        # Bouton pour quitter
        self.quit_button = tk.Button(self.root, text="Quitter", command=self.root.quit, font=("Arial", 14))
        self.quit_button.pack(pady=10)

        # Initialiser les barres de vie
        self.update_hp_bars()

    def update_attack_buttons(self):
        # Supprimer les anciens boutons d'attaque
        for btn in self.attack_buttons:
            btn.destroy()
        self.attack_buttons = []

        # Créer de nouveaux boutons pour les attaques disponibles
        for attack_name in self.current_player_pokemon["attacks"]:
            btn = tk.Button(self.root, text=attack_name, command=lambda name=attack_name: self.player_attack(name), font=("Arial", 14))
            btn.pack(pady=5)
            self.attack_buttons.append(btn)

    def switch_pokemon(self):
        def switch_to(pokemon):
            if pokemon["hp"] > 0:
                self.current_player_pokemon = pokemon
                self.update_labels()
                self.update_hp_bars()
                self.update_attack_buttons()  # Rafraîchir les attaques
                switch_window.destroy()
            else:
                messagebox.showinfo("Impossible", f"{pokemon['name']} est déjà KO !")

        # Fenêtre pour choisir le Pokémon
        switch_window = tk.Toplevel(self.root)
        switch_window.title("Changer de Pokémon")

        for pokemon in self.player_team:
            btn = tk.Button(switch_window, text=f"{pokemon['name']} (HP: {pokemon['hp']}/{pokemon['max_hp']})",
                            command=lambda p=pokemon: switch_to(p))
            btn.pack(pady=5)

    def player_attack(self, attack_name):
        if attack_name in self.current_player_pokemon["attacks"]:
            attack = self.current_player_pokemon["attacks"][attack_name]
        else:
            messagebox.showerror("Erreur", f"L'attaque {attack_name} n'existe pas pour {self.current_player_pokemon['name']} !")
            return

        damage = random.randint(*attack)
        self.current_enemy_pokemon["hp"] -= damage
        self.current_enemy_pokemon["hp"] = max(0, self.current_enemy_pokemon["hp"])

        self.update_labels()
        self.update_hp_bars()

        if self.current_enemy_pokemon["hp"] <= 0:
            messagebox.showinfo("KO", f"{self.current_enemy_pokemon['name']} est KO !")
            self.next_enemy_pokemon()
            if not self.enemy_team:
                messagebox.showinfo("Victoire", "Vous avez vaincu tous les Pokémon adverses !")
                self.reset_game()
                return

        self.enemy_attack()

    def use_potion(self):
        if self.potions > 0:
            heal_amount = min(self.potion_heal_amount, self.current_player_pokemon["max_hp"] - self.current_player_pokemon["hp"])
            self.current_player_pokemon["hp"] += heal_amount
            self.potions -= 1
            self.potion_button.config(text=f"Potion ({self.potions})")
            messagebox.showinfo("Potion utilisée", f"{self.current_player_pokemon['name']} a récupéré {heal_amount} HP !")
            self.update_labels()
            self.update_hp_bars()
        else:
            messagebox.showinfo("Plus de potions", "Vous n'avez plus de potions !")

    def update_labels(self):
        self.player_label.config(text=f"{self.current_player_pokemon['name']} (HP: {self.current_player_pokemon['hp']})")
        self.enemy_label.config(text=f"{self.current_enemy_pokemon['name']} (HP: {self.current_enemy_pokemon['hp']})")

    def update_hp_bars(self):
        self.player_hp_bar.delete("all")
        player_hp_percentage = self.current_player_pokemon["hp"] / self.current_player_pokemon["max_hp"]
        self.player_hp_bar.create_rectangle(0, 0, 200 * player_hp_percentage, 20, fill="green")

        self.enemy_hp_bar.delete("all")
        enemy_hp_percentage = self.current_enemy_pokemon["hp"] / self.current_enemy_pokemon["max_hp"]
        self.enemy_hp_bar.create_rectangle(0, 0, 200 * enemy_hp_percentage, 20, fill="red")

    def enemy_attack(self):
        attack_name = random.choice(list(self.current_enemy_pokemon["attacks"].keys()))
        attack = self.current_enemy_pokemon["attacks"][attack_name]
        damage = random.randint(*attack)

        self.current_player_pokemon["hp"] -= damage
        self.current_player_pokemon["hp"] = max(0, self.current_player_pokemon["hp"])

        self.update_labels()
        self.update_hp_bars()

        if self.current_player_pokemon["hp"] <= 0:
            messagebox.showinfo("KO", f"{self.current_player_pokemon['name']} est KO !")
            self.next_player_pokemon()
            if not self.player_team:
                messagebox.showinfo("Défaite", "Tous vos Pokémon sont KO. Vous avez perdu !")
                self.reset_game()

    def next_enemy_pokemon(self):
        self.enemy_team.pop(0)
        if self.enemy_team:
            self.current_enemy_pokemon = self.enemy_team[0]
            self.update_labels()
            self.update_hp_bars()

    def next_player_pokemon(self):
        self.player_team = [pokemon for pokemon in self.player_team if pokemon["hp"] > 0]
        if self.player_team:
            self.current_player_pokemon = self.player_team[0]
            self.update_labels()
            self.update_hp_bars()

    def reset_game(self):
        self.__init__(self.root)

# Lancement du jeu
root = tk.Tk()
game = PokemonGame(root)
root.mainloop()
