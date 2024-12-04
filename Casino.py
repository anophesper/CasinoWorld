import random

class Casino:
    @staticmethod
    def play(bet: float):
        # округлюємо ставку до двох знаків після коми
        bet = round(bet, 2)
        print(f"Ставка: {bet}")
        # кидаємо кубики
        cube1 = random.randint(1, 6)
        cube2 = random.randint(1, 6)

        if cube1 == cube2: # якщо в нас дубль ставка подвоєна або помножена на шість якщо випало 5 і 5
            if cube1 + cube2 == 10:
                bet = round(bet * 6, 2)
                text = "Великий виграш! Ваша ставка помножена на шість!"
            else:
                bet = round(bet * 2, 2)
                text = "Ваша ставка подвоєна!"
            text += f" Виграш: {bet}"
        elif cube1 + cube2 in (10, 11): # якщо в нас сума кубиків 10 чи 11 ставка подвоюється
            bet = round(bet * 3, 2)
            text = f"Ваша ставка подвоєна! Виграш: {bet}"
        elif cube1 + cube2 in (6, 7): # якщо в нас сума кубиків 6 чи 7 ставка зберігається
            text = f"Ви зберегли свою ставку"
            pass
        else: # в інших випадках гравець програв ставку
            bet = 0
            text = f"Ви програли"

        print(f"Кубик 1: {cube1}, Кубик 2: {cube2}, {text}") # виводимо повідомлення в консоль які кубики випали та результат гри
        return bet