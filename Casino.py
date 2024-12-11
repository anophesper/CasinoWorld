import random
from typing import List

class Casino:
    def __init__(self):
        # словник для комбінацій кубиків та коефіцієнтів виграшу
        self.odds = {
            6: {(5, 5)},  # Коефіцієнт 6 для дубля 5+5
            3: {(4, 6), (5, 6)},  # Коефіцієнт 3 для кубиків з сумою 10,11
            2: {(1, 1), (2, 2), (3, 3), (4, 4), (6, 6)}  # Коефіцієнт 2 для дубля
        }

    # метод для отримування коефіцієнта виграшу
    def get_odds(self, dice_roll: List[int]) -> int:
        dice_roll_sorted = tuple(sorted(dice_roll))  # сортуємо кубики, щоб уникнути порядку й перетворюємо на кортеж для порівняння
        for coefficient, combinations in self.odds.items(): # перебираємо кожну комбінацію в odds
            if dice_roll_sorted in combinations: # якщо отримана комбінація є в словнику отримуємо коефіцієнт виграшу
                return coefficient
        return 0  # якщо жодна комбінація не зіграла

    # метод для гри в казино
    def play(self, bet: float):
        bet = round(bet, 2) # округлюємо ставку до двох знаків після коми
        if bet <= 0:# додаткова перевірка, ставка має бути більшою за нуль
            return False

        dice_roll = [random.randint(1, 6), random.randint(1, 6)] # кидаємо кубики
        odds_value = self.get_odds(dice_roll)# перевіряємо комбінації

        return round(bet * odds_value, 2) # повертаємо ставку помножену на коефіцієнт