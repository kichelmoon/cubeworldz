import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False


class Item:
    def __init__(self, pos_x, pos_y, pos_z=0):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
        self.color = (0, 128, 255)


class Zone:
    def __init__(self, pos_x, pos_y, width, height):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height


class PressureZone(Zone):
    def __init__(self, pos_x, pos_y, width, height, pressure):
        super().__init__(pos_x, pos_y, width, height)
        self.pressure = pressure
        self.color = (255, 255, pressure % 255)


class WorldView:
    def __init__(self, dimensions=2):
        self.width = 100
        self.height = 100
        if dimensions == 3:
            self.depth = 100
        self.items = []
        self.zones = []
        self.mode = "TOP"

    def draw_zones(self):
        for zone in self.zones:
            pygame.draw.rect(screen, zone.color, pygame.Rect(zone.x, zone.y, zone.width, zone.height))

    def draw_items(self):
        if self.mode == "TOP":
            for world_item in self.items:
                pygame.draw.rect(screen, world_item.color, pygame.Rect(world_item.x, world_item.y, 1, 1))


class MeteoWorld(WorldView):
    def __init__(self):
        super().__init__()
        pressure_moment = 1013.25
        for i in range(self.height):
            if i % 8 == 0:
                self.zones.append(PressureZone(0, i, 100, 8, pressure_moment))
                pressure_moment -= 8


my_world = MeteoWorld()
my_world.items.append(Item(22, 22))
my_world.items.append(Item(3, 33))
my_world.items.append(Item(55, 55))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    my_world.draw_zones()
    my_world.draw_items()
    pygame.display.flip()