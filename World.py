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
            print(f"Нова людина в місті. \n{person.__str__()}\n")
            self.bank.create_account(person)
            self.people.append(person)

    def live(self):
        for person in self.people: # перебираємо по черзі кожну людину зі списку
            if person.account.is_blocked: # якщо акаунт заблоковано нічого не робимо
                continue

            print("----------------------------------------------------------------------------------------")
            print(f"{person.name}")
            person.interact_with_bank() # людина взаємодіє з банком на початку
            #print(f"\n{person.account.__str__()}\n")
            person.interact_with_casino(self.casino) # людина грає в казино
            print(f"{person.name} Готівка: {person.cash}")
            person.interact_with_bank() # людина знову взаємодіє з банком
            # print(f"\n{person.account.__str__()}\n")
            print("----------------------------------------------------------------------------------------")

        print("----------------------------------------------------------------------------------------")
        self.bank.process_accounts() # банк перевіряє кожен акаунт наприкінці місяця
        print("----------------------------------------------------------------------------------------")

        # ДОДАТИ ЯКУСЬ ВЗАЄМОДІЮ ІЗ ЗМІНЕННЯМ КРЕДИТНОГО ЛІМІТУ