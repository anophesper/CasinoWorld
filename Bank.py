from Person import Person
from BankAccount import BankAccount
import colorama

class Bank:
    def __init__(self):
        self.__account_list = [] # ініціалізуємо порожній список банківських акаунтів

    # метод для створення нового банківського акаунту
    def create_account(self, person: Person):
        new_account = BankAccount(person.name) # створюємо новий акаунт
        person.account = new_account # прив'язуємо акаунт до вже існуючого об'єкту людини
        self.__account_list.append(new_account) # додаємо акаунт до списку акаунтів банку

    # метод для перевірки всіх акаунтів РЕДАГУВАТИ
    def process_accounts(self):
        for account in self.__account_list: # перебираємо кожен акаунт зі списку
            print(f"{account.name}")
            if account.is_blocked: # перевіряємо чи заблокований акаунт, якщо так, то переходимо до наступного акаунту
                print(f"Аккаунт заблоковано")
                continue

            account.credit_observe() # оновлюємо інформацію про кредит
            if account.credit_has_not_been_repaid_for == 6: # блокуємо акаунт якщо кредит не виплачений протягом 6 місяців
                account.is_blocked = True
                print(f"Аккаунт заблоковано")
            else:
                account.interest_accrual() # нараховуємо відсотки