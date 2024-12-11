from Bank import Bank
from Casino import Casino
from Person import Person

class World:
    def __init__(self, population: int):
        self.people = []
        self.bank = Bank()
        self.casino = Casino()

        # створення людей та акаунтів для них
        for i in range(1, population + 1):
            person = Person(f"Person{i}")
            print(f"Нова людина в місті. \n{str(person)}\n")
            self.bank.create_account(person)
            self.people.append(person)

    def live(self, month):
        print("----------------------------------------------------------------------------------------")
        for person in self.people: # перебираємо по черзі кожну людину зі списку
            if person.account.is_blocked: # якщо акаунт заблоковано переходимо до наступного
                continue
            person.add_monthly_report(month) # додаємо звіт за новий місяць
            person.interact_with_bank() # людина взаємодіє з банком на початку
            person.interact_with_casino(self.casino) # людина грає в казино
            person.interact_with_bank() # людина знову взаємодіє з банком
        self.bank.process_accounts() # банк перевіряє кожен акаунт наприкінці місяця
        for person in self.people:
            print(person.get_monthly_summary())
        print("----------------------------------------------------------------------------------------")
        # ДОДАТИ ЯКУСЬ ВЗАЄМОДІЮ ІЗ ЗМІНЕННЯМ КРЕДИТНОГО ЛІМІТУ