import random
from Casino import Casino
from Report import Report

class Person:
    # ПОДУМАТИ НАД МОДИФІКАТОРАМИ ДОСТУПУ
    def __init__(self, name):
        self.name = name
        self.__cash = random.randint(1000, 10000)
        self._cash_threshold = 500.00
        self.__account = None
        self._risk_level = random.randint(1, 5)
        self._monthly_casino_budget = self.calculate_casino_budget()
        self.monthly_report = [] # змінна для запису дій персонажа за кожен місяць

    # метод для визначення суми грошей для казино на місяць, базуючись на рівні ризику
    def calculate_casino_budget(self):
        # рандомно визначаємо суму грошей для казино на місяць відповідно до рівня ризику людини (чим він більший, тим більше грошей)
        risk_budget_map = {
            1: (1000, 2000),
            2: (2000, 4000),
            3: (4000, 6000),
            4: (6000, 8000),
            5: (8000, 10000),
        }
        return round(random.randint(*risk_budget_map[self._risk_level]), 2)

    # Метод для додавання нового звіту до списку
    def add_monthly_report(self, month):
        self.monthly_report.append(Report(month))

    # метод для формування інформації про людину
    def __str__(self):
        return (f"Ім'я: {self.name}\n"
                f"Готівка: {self.__cash}\n"
                f"Рівень ризику: {self._risk_level}\n"
                f"Запланована витрата в казино на місяць: {self._monthly_casino_budget}")

    # ПОДУМАТИ метод для формування звіту за місяць
    def get_monthly_summary(self):
        report = self.monthly_report[-1] # беремо останній звіт в списку
        account_info = ""
        if self.__account: # перевірка наявності акаунту
            account_info = (f"Грошей на рахунку: {self.__account.balance}\n"
                            f"Кредит: {self.__account.credit_remaining}\n"
                            f"Статус Акаунту: {'Заблоковано' if self.__account.is_blocked else 'Активно'}\n")

        # формування звіту
        summary = (f"Ім'я: {self.name}\n"
                   f"{str(report)}\n"
                   f"Грошей на руках: {self.__cash}\n"
                   f"{account_info}")

        return summary

    # метод для поповнення рахунку
    def deposit(self, funds: float):
        funds = round(funds, 2) # округлюємо суму
        # перевірка чи вистачає готівки для поповнення картки
        if self.__cash >= funds:
            # якщо поповнення рахунку успішне, віднімаємо суму з готівки
            if self.__account.deposit(funds):
                self.__cash = round(self.__cash - funds, 2)
                return True
        return False

    # метод для зняття готівки з рахунку
    def withdraw(self, funds: float):
        funds = round(funds, 2) # округлюємо суму
        # якщо гроші успішно зняті з рахунку додаємо їх до готівки
        if self.__account.withdraw(funds):
            self.__cash = round(self.__cash + funds, 2)
            return True
        return False

    # метод для взаємодії з банком
    # ПОДУМАТИ ЯКАСЬ ФІГНЯ ІЗ ЗАПИСОМ СКІЛЬКИ ПОКЛАЛИ СКІЛЬКИ ЗНЯЛИ ЗА МІСЯЦЬ
    def interact_with_bank(self):
        # якщо в нас готівки менше ніж нам потрібно на місяць для казино ми знімаємо кошти
        if self.__cash < self._monthly_casino_budget:
            funds = round(self._monthly_casino_budget - self.__cash, 2)
            if self.withdraw(funds):
                self.monthly_report[-1].add_info_report("withdraw", funds)# ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ

        # якщо в нас готівки більше ніж нам потрібно на місяць для казино ми кладемо залишок на рахунок
        elif self.__cash > self._monthly_casino_budget:
            funds = round(self.__cash - self._monthly_casino_budget, 2)
            if self.deposit(funds):
                self.monthly_report[-1].add_info_report("deposit", funds)# ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ

        credit_limit = self._risk_level  # чим більший рівень ризику людини, тим довше він не переймається за кредит (кредит не позначається терміновим)
        # якщо в нас є терміновий кредит, то маємо його погасити якщо є кошти, і лишити мінімум
        if self.__account.credit_has_not_been_repaid_for >= credit_limit:
            # якщо в нас готівки вистачить для погашення кредиту і не важливо скільки в нас лишається коштів ми погашаємо його
            # (ТІЛЬКИ В ВИПАДКУ ЯКЩО КРЕДИТНА ЗАБОРГОВАНІСТЬ ВЖЕ 5 МІСЯЦІВ)
            if self.__account.credit_remaining <= self.__cash and self.__account.credit_has_not_been_repaid_for == 5:
                funds = round(self.__cash - self.__account.credit_remaining, 2)
            else:
                funds = round(self.__cash - self._cash_threshold, 2)

            if self.deposit(funds):
                self.monthly_report[-1].add_info_report("deposit", funds)# ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ

    # метод для гри в казино ПОДУМАТИ
    def interact_with_casino(self, casino: Casino):
        # загальна ставка на цей місяць
        # якщо в нас готівки менше ніж заплановано в казино на місяць, то загальна ставка = наявна готівка, в інших випадках
        # загальна ставка рівна тому, що заплановано на місяць
        if self.__cash <= self._monthly_casino_budget:
            max_bet = self.__cash
        else:
            max_bet = self._monthly_casino_budget

        # ПОДУМАТИ НАД ЦИМ може на кількість ставок буде впливати рівень ризику людини
        bet_fraction = random.randint(3, 30) # кількість ставок на місяць рандомно від трьох до тридцяти ПОДУМАТИ
        bet = round(max_bet / bet_fraction, 2)

        total_bet = 0.0 # скільки грошей вже було поставлено
        win = 0.0 # виграш
        while max_bet >= bet:  # Граємо, поки є гроші для ставки
            max_bet = round(max_bet - bet, 2) # віднімаємо поточну ставку від загальної ставки на місяць
            total_bet += bet # додаємо поточну ставку до грошей які вже поставили
            win += round(casino.play(bet), 2) # граємо в казино і додаємо результат гри до виграшу
        self.__cash = round((self.__cash - total_bet) + win, 2) # додаємо загальний виграш до готівки

        self.monthly_report[-1].add_info_report("win", win)  # ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ

        loss = round(abs(total_bet - win), 2)  # Програш: загальна сума ставок мінус виграш
        self.monthly_report[-1].add_info_report("loss", loss)  # ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ

        # якщо в нас виграш більший за суму грошей які людина може витратити на казино на місяць то її рівень ризику підвищується на один
        # (якщо ще не є максимальним)
        if win > self._monthly_casino_budget and self._risk_level < 5:
            self._risk_level +=1
            self.monthly_report[-1].add_info_report("risk_level", 1)  # ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ
            self._monthly_casino_budget = self.calculate_casino_budget() # оновлюємо суму грошей які людина може витратити на казино
        # якщо виграш нуль, рівень ризику знижується (якщо ще не є максимальним)
        elif win == 0 and self._risk_level > 1:
            self._risk_level -= 1
            self.monthly_report[-1].add_info_report("risk_level", -1)  # ЗАПИСУЄМО ЦЮ ДІЮ В РЕПОРТ ЗА МІСЯЦЬ
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
        return self.__cash
    @cash.setter
    def cash(self, value):
        self.__cash = value