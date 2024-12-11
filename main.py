from World import World

population  = 10
month = 6

world = World(int(population))
for i in range(1, month + 1):
    world.live(i)
