import random
import colorama

class BankAccount:
    def __init__(self, name):
        self.name = name
        self.__card_number = self.generate_card_number()
        self.__balance = 0.0
        self.__currency = "UAH"
        self.__credit_limit = 10000.0
        self.__credit_funds = 10000.0
        self.__interest_rate = 0.02
        self.__credit_has_not_been_repaid_for = 0
        self.__is_blocked = False

    # метод для формування інформації про банківський рахунок
    def __str__(self):
        return (f"Власник рахунку: {self.name}\n"
                f"Номер картки: {self.__card_number}\n"
                f"Баланс: {self.__balance} {self.__currency}\n"
                f"Кредитні кошти: {self.__credit_funds} {self.__currency}\n"
                f"Кредитний ліміт: {self.__credit_limit} {self.__currency}\n"
                f"Процентна ставка: {self.__interest_rate * 100}%\n"
                f"Заблоковано: {'Так' if self.__is_blocked else 'Ні'}")

    # метод для генерації номера картки
    @staticmethod
    def generate_card_number():
        return " ".join("".join(str(random.randint(0, 9)) for _ in range(4)) for _ in range(4)) # рандомно формуємо чотири частини
        # номера картки з чотирьох чисел

    # метод для поповнення балансу або кредитного рахунку
    def deposit(self, funds: float):
        # if self.__is_blocked: # нічого не робимо якщо акаунт заблокований
        #     print("Аккаунт заблоковано")
        #     return

        funds = round(funds, 2)
        if funds <= 0.00: # додаткова перевірка, сума для поповнення картки має бути більшою за нуль
            print("Для поповнення рахунку сума має бути більшою за нуль")
            return

        credit_shortfall = round(self.__credit_limit - self.__credit_funds, 2) # перевіряємо чи є в клієнта кредит
        if credit_shortfall > 0: # якщо кредит є спочатку повертаємо його
            to_credit = round(min(funds, credit_shortfall), 2) # якщо сума заборгованості більша за суму поповнення, то всі гроші буде
            # використано на повернення кредиту. якщо сума заборгованості менша за суму поповнення, то на повернення кредиту буде використано
            # тільки те що заборговано, решта піде на рахунок клієнта
            self.__credit_funds = round(self.__credit_funds + to_credit, 2)
            funds = round(funds - to_credit, 2) # решта після повернення кредиту
            print(f"Поповнення кредитного рахунку на {to_credit} {self.__currency}. Кредитні кошти: {self.__credit_funds}")

        if funds > 0: # якщо решта після повернення кредиту є, поповнюємо баланс
            self.__balance = round(self.__balance + funds, 2)
            print(f"Поповнення балансу на {funds} {self.__currency}. Баланс: {self.__balance}")

    # метод для зняття грошів з рахунку ПОДУМАТИ
    def withdraw(self, funds: float):
        # if self.__is_blocked: # нічого не робимо якщо акаунт заблокований
        #     print("Аккаунт заблоковано")
        #     return

        funds = round(funds, 2)
        if funds <= 0:# додаткова перевірка, сума для зняття з картки має бути більшою за нуль
            print("Для зняття грошей з рахунку сума має бути більшою за нуль")
            return

        # якщо на балансі вистачає коштів, використовуємо тільки їх
        if self.__balance >= funds:
            self.__balance = round(self.__balance - funds, 2)
            print(f"Зняття готівки з балансу на суму {funds}. Баланс: {self.__balance} {self.__currency} ")
            return True
        # якщо на балансі недостатньо коштів, і кредитних коштів також, операція відхилена
        elif self.__balance + self.__credit_funds < funds:
            print(f"На рахунку недостатньо коштів для зняття готівки. Баланс: {self.__balance} {self.__currency} "
                f"Кредитні кошти: {self.__credit_funds} {self.__currency}")
            return False
        # якщо на балансі немає коштів, але є кредитні кошти, знімаємо з них
        elif self.__credit_funds > funds and self.__balance == 0:
            self.__credit_funds = round(self.__credit_funds - funds, 2)
            print(f"Зняття готівки з кредитного рахунку на суму {funds}. "
                  f"Кредитні кошти: {self.__credit_funds} {self.__currency} ")
            return True
        # якщо на балансі не вистачає коштів, але є кредитні, знімаємо з балансу все що є і решту беремо з кредитних коштів
        else:
            print(f"Зняття готівки з балансу на суму {self.__balance}. Баланс: 0 {self.__currency} ")
            self.__balance = 0
            self.__credit_funds = round(self.__credit_funds - (funds - self.__balance), 2)
            print(f"Зняття готівки з кредитного рахунку на суму {funds - self.__balance}. "
                  f"Кредитні кошти: {self.__credit_funds} {self.__currency} ")
            return True

    # метод для зміни кредитного ліміту
    def change_limit(self, funds: float):
        # if self.__is_blocked: # нічого не робимо якщо акаунт заблокований
        #     print("Аккаунт заблоковано")
        #     return

        funds = round(funds, 2)
        if funds <= 100: # ми не можемо встановити кредитний ліміт менше ніж 100
            print(f"Мінімальний кредитний ліміт - 100 {self.__currency}")
            return
        # якщо в нас є заборгованість ми не можемо змінити кредитний ліміт
        if self.__credit_funds < self.__credit_limit:
            print(f"Ви не можете змінити поточний ліміт в зв'язку з кредитною заборгованістю."
                  f"Кредитна заборгованість: {self.__credit_limit - self.__credit_funds} {self.__currency} ")
        # якщо в нас нема заборгованості змінюємо ліміт
        else:
            self.__credit_limit = funds
            self.__credit_funds = funds
            print(f"Кредитний ліміт змінено. Кредитні кошти: {self.__credit_funds} {self.__currency} ")

    # метод для нарахування відсотків
    def interest_accrual(self):
        # якщо в нас немає кредиту, нараховуємо відсотки відносно поточного балансу
        if self.__credit_funds == self.__credit_limit:
            interest = round(self.__balance * self.__interest_rate, 2) # вираховуємо суму нарахування
            self.__balance = round(self.__balance + interest, 2)
            print(f"Відсотки нараховано: {interest} {self.__currency}. Новий баланс: {self.__balance}")
        else:
            print(f"Відсотки не нараховуються.")

    # метод для спостереження за кредитом
    def credit_observe(self):
        if self.__credit_funds == self.__credit_limit:
            self.__credit_has_not_been_repaid_for = 0
            print("Кредитної заборгованості немає.")
        # якщо в нас є кредитна заборгованість додаємо один місяць до терміну не сплати кредитних коштів
        else:
            self.__credit_has_not_been_repaid_for += 1
            print(f"Кредит не виплачений протягом {self.__credit_has_not_been_repaid_for} місяців.")

    # гетери та сетери для полів
    @property
    def credit_has_not_been_repaid_for(self):
        return self.__credit_has_not_been_repaid_for
    @credit_has_not_been_repaid_for.setter
    def credit_has_not_been_repaid_for(self, value):
        self.__credit_has_not_been_repaid_for = value
    @property
    def is_blocked(self):
        return self.__is_blocked
    @is_blocked.setter
    def is_blocked(self, value):
        self.__is_blocked = value