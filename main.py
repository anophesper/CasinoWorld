from World import World

population  = int(input("Введіть кількість жителів цього світу:\n"))
month = int(input("Введіть кількість місяців:\n"))

world = World(population)
for i in range(1, month + 1):
    world.live(i)
