from World import World

population  = 10
month = 12

world = World(int(population))
for i in range(month):
    world.live()
