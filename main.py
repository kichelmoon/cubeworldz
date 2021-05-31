import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False


class Item:
    def __init__(self, pos_x, pos_y, pos_z=0):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
        self.color = (0, 128, 255)


class AirPackage(Item):
    def __init__(self, pos_x, pos_y, temperature, humidity):
        super().__init__(pos_x, pos_y)
        self.temperature = temperature
        self.humidity = humidity

    def lift(self, meters):
        self.x += meters
        self.temperature -= 100 * 0.0098


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

        self.display_x = 1280 / 4
        self.display_y = 720 / 4
        self.scale = 4

        self.turn = 1

    def draw_scaled_rect(self,color, x, y, width, height):
        pygame.draw.rect(screen, color, pygame.Rect(x * self.scale + self.display_x, (100 - y) * self.scale + self.display_y, width * self.scale, height * self.scale))

    def draw_zones(self):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.display_x, self.display_y, self.height * self.scale, self.width * self.scale))
        for zone in self.zones:
            self.draw_scaled_rect(zone.color, zone.x, zone.y, zone.width, zone.height)

    def draw_items(self):
        if self.mode == "TOP":
            for world_item in self.items:
                self.draw_scaled_rect(world_item.color, world_item.x, world_item.y, 1, 1)

    def new_turn(self):
        print(self.turn)
        for item in self.items:
            item.lift(1)
            print(item.temperature)
        self.turn += 1


class MeteoWorld(WorldView):
    def __init__(self):
        super().__init__()
        #pressure_moment = 1013.25
        #for i in range(self.height):
        #    if i % 8 == 0:
        #        self.zones.append(PressureZone(0, 100 - i, 100, 8, pressure_moment))
        #        pressure_moment -= 8


my_world = MeteoWorld()
my_world.items.append(AirPackage(50, 1, 15, 100))

button = pygame.Rect(100, 100, 50, 50)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            if button.collidepoint(mouse_pos):
                my_world.new_turn()

    my_world.draw_zones()
    my_world.draw_items()
    pygame.draw.rect(screen, (255, 0, 0), button)
    pygame.display.flip()