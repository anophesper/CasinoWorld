from Person import Person
from BankAccount import BankAccount

class Bank:
    def __init__(self):
        self.__account_list = [] # ініціалізуємо порожній список банківських акаунтів

    # метод для створення нового банківського акаунту
    def create_account(self, person: Person):
        new_account = BankAccount(person.name) # створюємо новий акаунт
        person.account = new_account # прив'язуємо акаунт до вже існуючого об'єкту людини
        self.__account_list.append(new_account) # додаємо акаунт до списку акаунтів банку

    # метод для перевірки всіх акаунтів
    def process_accounts(self):
        for account in self.__account_list: # перебираємо кожен акаунт зі списку
            if account.is_blocked: # перевіряємо чи заблокований акаунт, якщо так, то переходимо до наступного акаунту
                continue

            account.credit_observe() # оновлюємо інформацію про кредит
            if account.credit_has_not_been_repaid_for == 6: # блокуємо акаунт якщо кредит не виплачений протягом 6 місяців
                account.is_blocked = True
            else:
                account.interest_accrual() # нараховуємо відсотки якщо кредиту нема