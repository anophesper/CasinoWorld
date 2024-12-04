import random
from Casino import Casino

class Person:
    def __init__(self, name):
        self.name = name
        self._cash = random.randint(100, 1000)
        self._cash_threshold = 100.00
        self.__account = None
        self._risk_level = random.randint(1, 5)
        self._monthly_casino_budget = self.calculate_casino_budget()

    # метод для формування інформації про людину
    def __str__(self):
        return (f"Ім'я: {self.name}\n"
                f"Готівка: {self._cash}\n"
                f"Рівень ризику: {self._risk_level}\n"
                f"Запланована витрата в казино на місяць: {self._monthly_casino_budget}")

    # метод для визначення суми грошей для казино на місяць, базуючись на рівні ризику
    def calculate_casino_budget(self):
        # рандомно визначаємо суму грошей для казино на місяць відповідно до рівня ризику людини (чим він більший, тим більше грошей)
        risk_budget_map = {
            1: (100, 200),
            2: (200, 400),
            3: (400, 600),
            4: (600, 800),
            5: (800, 1000),
        }
        return round(random.randint(*risk_budget_map[self._risk_level]), 2)

    # метод для поповнення рахунку
    def deposit(self, funds: float):
        funds = round(funds, 2)
        # перевірка чи вистачає готівки для поповнення картки
        if self._cash >= funds:
            self.__account.deposit(funds)
            self._cash = round(self._cash - funds, 2)
        else:
            print(f"Не вистачає коштів. Поточна сума грошей на руках: {self._cash} {self.__account.currency}")

    # метод для зняття готівки з рахунку
    def withdraw(self, funds: float):
        funds = round(funds, 2)
        if self.__account.withdraw(funds):
            self._cash = round(self._cash + funds, 2) # якщо гроші успішно зняті з рахунку додаємо їх до готівки

    # метод для взаємодії з банком ПОДУМАТИ
    def interact_with_bank(self):
        # якщо в нас готівки менше ніж нам потрібно на місяць для казино ми знімаємо кошти
        if self._cash < self._monthly_casino_budget:
            self.withdraw(round(self._monthly_casino_budget - self._cash, 2))
        # якщо в нас готівки більше ніж нам потрібно на місяць для казино ми кладемо залишок на рахунок
        elif self._cash > self._monthly_casino_budget:
            self.deposit(round(self._cash - self._monthly_casino_budget, 2))

        credit_limit = self._risk_level  # чим більший рівень ризику людини, тим довше він не переймається за кредит (кредит не позначається терміновим)
        # якщо в нас є терміновий кредит, то маємо його погасити якщо є кошти, і лишити мінімум
        if self.__account.credit_has_not_been_repaid_for > credit_limit:
            self.deposit(round(self._cash - self._cash_threshold, 2))

    # метод для гри в казино ПОДУМАТИ
    def interact_with_casino(self, casino: Casino):
        # чим більший ризик, тим вище ставка
        bet_fraction = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2}
        bet = round(self._cash / bet_fraction[self._risk_level], 2)

        win = 0.0
        print(f"Готівка: {self._cash}")
        while self._cash >= bet:  # Граємо, поки є гроші для ставки
            self._cash = round(self._cash - bet, 2)
            win += round(casino.play(bet), 2)
            print(f"Лишилось грошей для ставок: {self._cash}\n")
        print(f"Виграш в цьому місяці: {round(win, 2)}")
        self._cash = round(self._cash + win, 2) # додаємо виграш до готівки

        # якщо в нас виграш більший за суму грошей які людина може витратити на казино на місяць то її рівень ризику підвищується на один
        # (якщо ще не є максимальним)
        if win > self._monthly_casino_budget and self._risk_level < 5:
            self._risk_level +=1
            print(f"Рівень ризику підвищився на 1. Поточний рівень ризику: {self._risk_level}")
            self._monthly_casino_budget = self.calculate_casino_budget() # оновлюємо суму грошей які людина може витратити на казино
        # якщо виграш нуль, рівень ризику знижується (якщо ще не є максимальним)
        elif win == 0 and self._risk_level > 1:
            self._risk_level -= 1
            print(f"Рівень ризику знизився на 1. Поточний рівень ризику: {self._risk_level}")
            self._monthly_casino_budget = self.calculate_casino_budget()# оновлюємо суму грошей які людина може витратити на казино

    # гетери та сетери для полів
    @property
    def account(self):
        return self.__account
    @account.setter
    def account(self, value):
        self.__account = value

    @property
    def cash(self):
        return self._cash
    @cash.setter
    def cash(self, value):
        self._cash = value