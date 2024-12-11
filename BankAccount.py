import random

class BankAccount:
    # ПОДУМАТИ НАД МОДИФІКАТОРАМИ ДОСТУПУ
    def __init__(self, name):
        self.name = name
        self.__card_number = self.generate_card_number()
        self.__balance = 0.0
        self.__currency = "UAH"
        self.__credit_limit = 50000.0
        self.__credit_funds = 50000.0
        self.__interest_rate = 0.02
        self.__credit_has_not_been_repaid_for = 0
        self.is_blocked = False

    # метод для формування інформації про банківський рахунок
    def __str__(self):
        return (f"Власник рахунку: {self.name}\n"
                f"Номер картки: {self.__card_number}\n"
                f"Баланс: {self.__balance} {self.__currency}\n"
                f"Кредитні кошти: {self.__credit_funds} {self.__currency}\n"
                f"Кредитний ліміт: {self.__credit_limit} {self.__currency}\n"
                f"Процентна ставка: {self.__interest_rate * 100}%\n"
                f"Заблоковано: {'Так' if self.is_blocked else 'Ні'}")

    # метод для генерації номера картки
    @staticmethod
    def generate_card_number():
        return " ".join("".join(str(random.randint(0, 9)) for _ in range(4)) for _ in range(4)) # рандомно формуємо чотири частини номера картки з чотирьох чисел

    # метод для поповнення балансу або кредитного рахунку
    def deposit(self, funds: float):
        funds = round(funds, 2)
        if funds <= 0.00: # додаткова перевірка, сума для поповнення картки має бути більшою за нуль
            return False

        credit_shortfall = round(self.__credit_limit - self.__credit_funds, 2) # перевіряємо чи є в клієнта кредит
        if credit_shortfall > 0: # якщо кредит є спочатку повертаємо його
            to_credit = round(min(funds, credit_shortfall), 2) # якщо сума заборгованості більша за суму поповнення, то всі гроші буде
            # використано на повернення кредиту. якщо сума заборгованості менша за суму поповнення, то на повернення кредиту буде використано
            # тільки те що заборговано, решта піде на рахунок клієнта
            self.__credit_funds = round(self.__credit_funds + to_credit, 2)
            funds = round(funds - to_credit, 2) # решта після повернення кредиту

        if funds > 0: # якщо решта після повернення кредиту є, поповнюємо баланс
            self.__balance = round(self.__balance + funds, 2)
            return True

    # метод для зняття грошів з рахунку ПОДУМАТИ
    def withdraw(self, funds: float):
        funds = round(funds, 2)
        if funds <= 0:# додаткова перевірка, сума для зняття з картки має бути більшою за нуль
            return False

        # якщо на балансі вистачає коштів, використовуємо тільки їх
        if self.__balance >= funds:
            self.__balance = round(self.__balance - funds, 2)
            return True
        # якщо на балансі недостатньо коштів, і кредитних коштів також, операція відхилена
        elif self.__balance + self.__credit_funds < funds:
            return False
        # якщо на балансі немає коштів, але є кредитні кошти, знімаємо з них
        elif self.__balance == 0 and self.__credit_funds > funds:
            self.__credit_funds = round(self.__credit_funds - funds, 2)
            return True
        # якщо на балансі не вистачає коштів, але є кредитні, знімаємо з балансу все що є і решту беремо з кредитних коштів
        else:
            funds = round(funds - self.__balance, 2)
            self.__balance = 0
            self.__credit_funds = round(self.__credit_funds - funds, 2)
            return True

    # метод для зміни кредитного ліміту
    def change_limit(self, funds: float):
        funds = round(funds, 2)
        if funds <= 100: # ми не можемо встановити кредитний ліміт менше ніж 100
            return False
        # якщо в нас є заборгованість ми не можемо змінити кредитний ліміт
        if self.__credit_funds != self.__credit_limit:
            return False
        # якщо в нас нема заборгованості змінюємо ліміт
        else:
            self.__credit_limit = funds
            self.__credit_funds = funds
            return True

    # метод для нарахування відсотків
    def interest_accrual(self):
        # якщо в нас немає кредиту, нараховуємо відсотки відносно поточного балансу
        if self.__credit_funds == self.__credit_limit:
            interest = round(self.__balance * self.__interest_rate, 2) # вираховуємо суму нарахування
            self.__balance = round(self.__balance + interest, 2)
        else:
            pass

    # метод для спостереження за кредитом
    def credit_observe(self):
        # якщо в нас кредитний ліміт та кредитні кошти не відрізняються то кредиту нема
        if self.__credit_funds == self.__credit_limit:
            self.__credit_has_not_been_repaid_for = 0
        # якщо в нас є кредитна заборгованість додаємо один місяць до терміну не сплати кредитних коштів
        else:
            self.__credit_has_not_been_repaid_for += 1

    # Геттери та сетери для полів
    @property
    def credit_has_not_been_repaid_for(self):
        return self.__credit_has_not_been_repaid_for
    @credit_has_not_been_repaid_for.setter
    def credit_has_not_been_repaid_for(self, value):
        self.__credit_has_not_been_repaid_for = value
    @property
    def balance(self):
        return self.__balance
    @property
    def credit_remaining(self):
        return round(self.__credit_limit - self.__credit_funds, 2)