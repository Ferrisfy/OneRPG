import random
class DevilFruit:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.abilities = []
        self.stat_bonuses = {"health": 0, "attack": 0, "defense": 0}  # Initialize stat bonuses

    def add_ability(self, ability, stat_increase=None, duration=None):
        self.abilities.append({"ability": ability, "stat_increase": stat_increase, "duration": duration})

    def set_stat_bonuses(self, health_bonus=0, attack_bonus=0, defense_bonus=0):
        self.stat_bonuses["health"] = health_bonus
        self.stat_bonuses["attack"] = attack_bonus
        self.stat_bonuses["defense"] = defense_bonus

# Create Devil Fruits and assign abilities and stat bonuses
devil_fruits = [
    DevilFruit("Gomu Gomu no Mi", "Paramecia"),
    DevilFruit("Hito Hito no Mi", "Zoan"),
    DevilFruit("Mera Mera no Mi", "Logia")
]
for fruit in devil_fruits:
    if fruit.name == "Gomu Gomu no Mi":
        fruit.add_ability("Rubberization")
        fruit.set_stat_bonuses(health_bonus=20, attack_bonus=10)
    elif fruit.name == "Hito Hito no Mi":
        fruit.add_ability("Animal Transformation")
        fruit.set_stat_bonuses(health_bonus=30)
    elif fruit.name == "Mera Mera no Mi":
        fruit.add_ability("Fire Manipulation")
        fruit.set_stat_bonuses(defense_bonus=30)

class Player:
    def __init__(self, name, level, exp, health, attack, defense, stat_points, gold):
        self.name = name
        self.level = level
        self.exp = exp
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.stat_points = stat_points
        self.gold = gold
        self.devil_fruits = []
        self.abilities = []

    def show_abilities(self):
        print("\nAbilities:")
        for i, fruit in enumerate(self.abilities, start=1):
            ability_name = fruit.abilities[0]['ability']
            print(f"{i}. {ability_name} - {fruit.name} ({fruit.type})")

    def choose_ability(self):
        while True:
            self.show_abilities()
            ability_choice = input(f"Choose an ability (1-{len(self.abilities)}, 0 to cancel): ")
            if ability_choice.isdigit():
                ability_index = int(ability_choice) - 1
                if 0 <= ability_index < len(self.abilities):
                    ability = self.abilities[ability_index]  # Get the DevilFruit object
                    ability_name = ability.abilities[0]['ability']  # Access the ability name
                    return ability_name
            elif ability_choice == "0":
                return None
            print("Invalid choice. Try again.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def level_up(self):
        print(f"\nCongratulations! {self.name} leveled up!")
        self.level += 1
        self.exp = 0
        self.stat_points += 1
        self.max_health += round(self.level * 1.255)
        self.health = self.max_health
        print(f"Level: {self.level}, Stat Points: {self.stat_points}")
        self.show_stat_menu()

    def show_stat_menu(self):
        print("\nStat Menu:")
        print("1. Increase Health")
        print("2. Increase Attack")
        print("3. Increase Defense")

    def show_devil_fruits(self):
        if not self.devil_fruits:
            print("\nPlayer can still swim")
        else:
            print("\nDevil Fruits:")
            for i, fruit in enumerate(self.devil_fruits, start=1):
                ability_name = fruit.abilities[0]['ability']
                print(f"{i}. Devil Fruit - {fruit.name} ({fruit.type})")
                print(f"   Type: {fruit.type}")
                print(f"   Ability: {ability_name}")

    def choose_stat_increase(self):
        while self.stat_points > 0:
            self.show_stat_menu()
            choice = input("Choose where to invest your stat points (1-3): ")
            if choice == "1":
                self.health += round(3 * (.5 * self.level) + 5) * 2
                self.max_health += round(3 * (.5 * self.level) + 5) * 2
                self.stat_points -= 1
            elif choice == "2":
                self.attack += round((2 * (self.level + 1) * (self.level / 2)),1)
                self.stat_points -= 1
            elif choice == "3":
                self.defense += round((1.25 * (.40 * self.level) + 2) * (.1 * self.level),1)
                self.stat_points -= 1
            else:
                print("Invalid choice. Try again.")

def create_player():
    name = input("Enter your pirate name: ")
    return Player(name, level=1, exp=0, health=100, attack=20, defense=10, stat_points=0, gold=0)

def create_enemy(player_level):
    enemies = [
        {"name": "Marine Soldier", "level": 1, "base_health": 30, "base_attack": 10, "exp_reward": 10, "gold_reward": 1},
        {"name": "Pirate", "level": 10, "base_health": 60, "base_attack": 20, "exp_reward": 30, "gold_reward": 5},
        {"name": "Sea King", "level": 25, "base_health": 150, "base_attack": 40, "exp_reward": 80, "gold_reward": 10},
        {"name": "Yonko Commander", "level": 40, "base_health": 300, "base_attack": 60, "exp_reward": 150, "gold_reward": 15},
        {"name": "Yonko", "level": 50, "base_health": 500, "base_attack": 100, "exp_reward": 250, "gold_reward": 25},
        {"name": "Admiral", "level": 75, "base_health": 750, "base_attack": 150, "exp_reward": 400, "gold_reward": 70, "drop_devil_fruit": True},
        {"name": "Fleet Admiral", "level": 90, "base_health": 900, "base_attack": 180, "exp_reward": 500, "gold_reward": 100, "drop_devil_fruit": True},
        {"name": "Gorosei", "level": 125, "base_health": 1200, "base_attack": 250, "exp_reward": 800, "gold_reward": 200, "drop_devil_fruit": True}
    ]

    # Limit appearance of stronger enemies based on level cap
    available_enemies = [enemy for enemy in enemies if enemy["level"] <= player_level + 5]
    enemy = random.choice(available_enemies)

    # Randomize enemy level within a range
    enemy_level = random.randint(player_level,player_level + 3)

    health = enemy["base_health"] + ((enemy_level - enemy["level"]) * 10)
    attack = enemy["base_attack"] + ((enemy_level - enemy["level"]) * 2)

    return Enemy(enemy["name"], enemy_level, health, attack, enemy["exp_reward"], enemy["gold_reward"], enemy.get("drop_devil_fruit", False))

def create_boss(player_level):
    bosses = [
        {"name": "Kaido", "level": 100, "base_health": 5000, "base_attack": 200, "exp_reward": 1000, "gold_reward": 1000, "drop_devil_fruit": True, "unique_drop": "drop"}, #make drops / changes stats
        {"name": "???", "level": 75, "base_health": 7500, "base_attack": 300, "exp_reward": 2000, "gold_reward": 2000, "drop_devil_fruit": True, "unique_drop": "drop"},
        {"name": "???", "level": 125, "base_health": 12000, "base_attack": 500, "exp_reward": 5000, "gold_reward": 5000, "drop_devil_fruit": True, "unique_drop": "drops"}
    ]

    # Limit appearance of bosses based on player level
    available_bosses = [boss for boss in bosses if boss["level"] <= player_level + 20]
    boss = random.choice(available_bosses)

    # Randomize boss level within a range
    boss_level = random.randint(player_level, player_level + 5)

    health = boss["base_health"] + (boss_level - boss["level"]) * 100
    attack = boss["base_attack"] + (boss_level - boss["level"]) * 20

    return Boss(boss["name"], boss_level, health, attack, boss["exp_reward"], boss["gold_reward"], boss.get("drop_devil_fruit", False), boss.get("unique_drop", None))

def visit_shop(player):
    print("\nWelcome to the Black Market!")
    print("1. Visit Village") #armor
    print("2. Buy a rare Devil Fruit (cost: 1000 gold)")
    print("3. Small Health Pot (cost: 5 gold)")
    print("4. Medium Health Pot (cost: 15 gold)")
    print("5. Big Health Pot (cost: 30 gold)")
    print("6. Max Health Pot (cost: 150 gold)")

    AlphaChoice = input("Choose an option (1-6, 0 to exit): ")

    if AlphaChoice == "1":
        print("\nWelcome to the Village!")
        print("1. Weapons")
        print("2. Armor")

        VillageChoice = input("Choose an option (1-2, 0 to exit): ")

        if VillageChoice == "1":
            print("\nWelcome to the Weapon Depot!")
            print("1. Grade Swords (50g +5atk)")
            print("2. Skillful Grade Swords (100g +12atk)")
            print("3. Great Grade Swords (200g +30atk)")
            print("4. Supreme Grade Swords (500g +75atk)")
        SwordChoice = input("Choose an option (1-4, 0 to exit): ")
        if SwordChoice == "1":
            if player.gold >= 50:
                player.gold -= 50
                player.attack += 5
                print("You bought a Grade Sword!")
            else:
                print("Not enough gold.")

        if SwordChoice == "2":
            if player.gold >= 100:
                player.gold -= 100
                player.attack += 12
                print("You bought a Skillful Grade Sword!")
            else:
                print("Not enough gold.")

        if SwordChoice == "3":
            if player.gold >= 200:
                player.gold -= 200
                player.attack += 30
                print("You bought a Great Grade Sword!")
            else:
                print("Not enough gold.")

        if SwordChoice == "4":
            if player.gold >= 500:
                player.gold -= 500
                player.attack += 75
                print("You bought a Supreme Grade Sword!")
            else:
                print("Not enough gold.")

        elif SwordChoice == "0":
            print("Leaving Weapon Depot.")

        elif VillageChoice == "2":
            print("\nWelcome to the Armor Depot!")

        elif VillageChoice == "0":
            print("Leaving Village.")

    elif AlphaChoice == "2":
        if player.gold >= 1000:
            player.gold -= 1000
            fruit = random.choice(devil_fruits)
            obtain_devil_fruit(player, fruit)
        else:
            print("Not enough gold.")

    elif AlphaChoice == "3":
        if player.gold >= 5:
            player.gold -= 5
            player.health += 5
            print("You bought a Small Health Pot (+5 hp)")
        else:
            print("Not enough gold.")

    elif AlphaChoice == "4":
        if player.gold >= 15:
            player.gold -= 15
            player.health += 20
            print("You bought a Small Health Pot (+20 hp)")
        else:
            print("Not enough gold.")

    elif AlphaChoice == "5":
        if player.gold >= 30:
            player.gold -= 30
            player.health += 30
            print("You bought a Big Health Pot (+50 hp)")
        else:
            print("Not enough gold.")

    elif AlphaChoice == "6":
        if player.gold >= 150:
            player.gold -= 150
            player.health += player.max.health
            print("You bought a Max Health Pot (+MAX hp)")
        else:
            print("Not enough gold.")

    elif AlphaChoice == "0":
        print("Exiting the Black Market.")
    else:
        print("Invalid choice. Try again.")

def obtain_devil_fruit(self, fruit):
    if len(self.devil_fruits) >= 1:
        print("You already have a Devil Fruit. You cannot obtain another one.")
        return
    self.devil_fruits.append(fruit)
    for ability in fruit.abilities:
        ability_instance = DevilFruit(fruit.name, fruit.type)
        ability_instance.abilities.append(ability)
        self.abilities.append(ability_instance)
    print(f"\nYou obtained the {fruit.name} Devil Fruit! You can now use its abilities in battles.")

def battle(player, enemy):
    print(f"A wild {enemy.name} (Level {enemy.level}) appears!")

    logia_invincible = False  # Flag to track if player has Logia devil fruit and is invincible

    while player.is_alive() and enemy.is_alive():
        print("\n" + "=" * 30)
        print(f"{player.name}'s Health: {player.health}/{player.max_health}")
        print(f"{enemy.name}'s Health: {enemy.health}")
        print("=" * 30)

        # Check Logia invincibility condition
        if any(fruit.type == "Logia" for fruit in player.abilities):
            logia_invincible == True

        # Decrement duration of active abilities
        for ability in player.abilities:
            if ability.abilities[0].get('duration', 0) is not None and ability.abilities[0].get('duration', 0) > 0:
                ability_name = ability.abilities[0]['ability']

                if ability_name == "Rubberization":
                    logia_invincible = True
                elif ability_name == "Fire Manipulation":
                    enemy.take_damage(ability.abilities[0].get('extra_damage', 0))
                    print(f"Your attack inflicts {ability.abilities[0].get('extra_damage', 0)} additional fire damage!")
                elif ability_name == "Animal Transformation":
                    if 'stat_increase' in ability.abilities[0]:
                        player.attack += ability.abilities[0]['stat_increase'].get('attack', 0)
                ability.abilities[0]['duration'] -= 1
                if ability.abilities[0]['duration'] == 0:
                    print(f"The effect of {ability_name} has worn off.")
                    # Remove ability effects when duration reaches 0
                    if ability_name == "Rubberization":
                        logia_invincible = False
                    elif ability_name == "Animal Transformation":
                        if 'stat_increase' in ability.abilities[0]:
                            player.attack -= ability.abilities[0]['stat_increase'].get('attack', 0)  # Remove attack bonus
                    player.abilities.remove(ability)

        action = input("\nEnter your move (1: Attack, 2: Use Ability, 3: Run): ")

        if action == "1":
            if logia_invincible == True and enemy.level < 50:
                print("You are invincible to enemies under level 50!")
                enemy.health - player.attack
                print(f"You dealt {player.attack} damage to {enemy.name}!")

            if enemy.level >= 50 and logia_invincible == True:
                damage_received = round(enemy.attack - player.defense)
                player.take_damage(damage_received)
                enemy.take_damage(player.attack)
                print(f"You dealt {player.attack} damage to {enemy.name}!")
                print(f"{enemy.name} counterattacks! You took {damage_received} damage.")
            elif logia_invincible == False:
                damage_received = round(enemy.attack - player.defense)
                player.take_damage(damage_received)
                enemy.take_damage(player.attack)
                print(f"You dealt {player.attack} damage to {enemy.name}!")
                print(f"{enemy.name} counterattacks! You took {damage_received} damage.")
            else:
                print(f"an error occurred")

        elif action == "2":
            if player.abilities:
                player.show_abilities()
                ability_choice = input(f"Choose an ability (1 - {player.abilities[0].name} ({player.abilities[0].type}), 0 to cancel): ")
                if ability_choice.isdigit() and 0 < int(ability_choice) <= len(player.abilities):
                    ability = player.abilities[int(ability_choice) - 1]  # Get the selected ability object
                    ability_name = ability.abilities[0]['ability']  # Access the ability name from the DevilFruit object
                    if ability_name == "Rubberization":
                        print("You activated Rubberization!")
                        print("You gain temporary invincibility.")
                        ability.abilities[0]['duration'] = 3
                    elif ability_name == "Animal Transformation":
                        print("You activated Animal Transformation!")
                        print("Your attack increases for a few turns.")
                        ability.abilities[0]['duration'] = 3
                        attack_increase = 20 + ((player.level - 1) * 2)
                        ability.abilities[0]['stat_increase'] = {'attack': attack_increase}
                    elif ability_name == "Fire Manipulation":
                        print("You activated Fire Manipulation!")
                        print("Your attacks will inflict additional fire damage.")
                        ability.abilities[0]['duration'] = 3
                        ability.abilities[0]['extra_damage'] = 20
                    else:
                        print("This ability does not have a specific effect yet.")

                elif ability_choice == "0":
                    print("Cancelled ability.")
                else:
                    print("Invalid choice. Try again.")
            else:
                print("You don't have any abilities to use.")

        elif action == "3":
            print("You managed to escape from the battle.")
            return False
        else:
            print("Invalid move. Try again.")

    if player.is_alive():
        gold_earned = enemy.gold_reward
        player.exp += round(enemy.exp_reward + (.05 * enemy.level))
        player.gold += gold_earned
        print(f"\nYou defeated {enemy.name} (Level {enemy.level})! Your health: {player.health}, EXP: {player.exp}/{(player.level * 1.25) * (player.level + 79)}")
        print(f"You earned {gold_earned} gold.")

        if player.exp >= round((player.level * 1.25) * (player.level + 79),2):
            player.level_up()
            player.choose_stat_increase()

        if enemy.drop_devil_fruit and random.random() < 0.2:  # 20% chance of dropping a devil fruit
            obtain_devil_fruit(player)
        return True
    else:
        print("\nGame Over. You have been defeated.")
        return False

class Enemy:
    def __init__(self, name, level, health, attack, exp_reward, gold_reward, drop_devil_fruit=False):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.drop_devil_fruit = drop_devil_fruit

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

class Boss(Enemy):
    def __init__(self, name, level, health, attack, exp_reward, gold_reward, drop_devil_fruit=False, unique_drop=None):
        super().__init__(name, level, health, attack, exp_reward, gold_reward, drop_devil_fruit)
        self.unique_drop = unique_drop

    def defeat_message(self):
        return f"\nYou defeated {self.name} (Level {self.level})! Your health: {self.health}, EXP: {self.exp_reward}, Gold: {self.gold_reward}. You obtained {self.unique_drop}!"

class Game:
    def __init__(self):
        self.player = create_player()

    def view_stats(self):
        print(f"\nStats:")
        print(f"Level: {self.player.level}")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Attack: {self.player.attack}")
        print(f"Defense: {self.player.defense}")
        print(f"Gold: {self.player.gold}")
        print(f"EXP: {self.player.exp}/{(self.player.level * 1.25) * (self.player.level + 79)}")

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Battle")
            print("2. Visit the Black Market")
            print("3. View Stats")
            print("4. View Devil Fruit")
            print("5. Boss")
            print("6. Exit")
            choice = input("Choose an option (1-6): ")

            if choice == "1":
                enemy = create_enemy(self.player.level)
                battle_result = battle(self.player, enemy)
                if battle_result:
                    self.view_stats()
            elif choice == "2":
                visit_shop(self.player)
            elif choice == "3":
                self.view_stats()
            elif choice == "4":
                self.player.show_devil_fruits()
            elif choice == "5":
                if self.player.level >= 70:
                    enemy = create_boss(self.player.level)
                    battle_result = battle(self.player, enemy)
                    if battle_result:
                        self.view_stats()
                else:
                    print("You need to be level 70 or higher to challenge a boss.")
            elif choice == "6":
                print("Exiting the game. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    game = Game()
    game.main_menu()
