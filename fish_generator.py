import random, time
from npc import *


# Fish generator class, spawn fishes in the tank
class FishGenerator:
    def __init__(self, fish_tank_capacity, frequency, list):
        self.id_generator = 0  # Should not be reduced
        self.capacity = fish_tank_capacity
        self.frequency = frequency
        self.work = True
        self.fishes = list  # list of fishes in the tank
        self.level = 1

    def change_level(self):
        self.level += 1

    def clear_tank(self):
        self.id_generator = 0
        for fish in self.fishes:
            if fish.id == -1:
                player = fish
                break
        self.fishes.clear()
        self.fishes.append(player)

    def stop(self):
        self.work = False

    def start(self):
        self.work = True
        while self.work:
            if self.capacity <= len(self.fishes):
                time.sleep(5)
                # self.fishes[0].alive = False
                # self.fishes.pop(0)
                continue

            rand = random.randint(1, 58)  # top limit depends on number of species

            # Large
            if 0 < rand <= 2:
                new_fish = Yellow(self.get_location(), self.id_generator)
            elif 2 < rand <= 4:
                new_fish = Killer(self.get_location(), self.id_generator)

            # Medium
            elif 4 < rand <= 7:
                new_fish = Stripes(self.get_location(), self.id_generator)
            elif 7 < rand <= 10:
                new_fish = Dark(self.get_location(), self.id_generator)
            elif 10 < rand <= 13:
                new_fish = Tuna(self.get_location(), self.id_generator)
            elif 13 < rand <= 17:
                new_fish = Red(self.get_location(), self.id_generator)

            # Small
            elif 17 < rand <= 21:
                new_fish = Tropical(self.get_location(), self.id_generator)
            elif 21 < rand <= 25:
                new_fish = Zebra(self.get_location(), self.id_generator)
            elif 25 < rand <= 29:
                new_fish = Guppy(self.get_location(), self.id_generator)
            elif 29 < rand <= 33:
                new_fish = Tiger(self.get_location(), self.id_generator)

            # Very small
            elif 33 < rand <= 38:
                new_fish = Pixel(self.get_location(), self.id_generator)
            elif 38 < rand <= 43:
                new_fish = Neon(self.get_location(), self.id_generator)
            elif 43 < rand <= 48:
                new_fish = Color(self.get_location(), self.id_generator)
            elif 48 < rand <= 53:
                new_fish = Disc(self.get_location(), self.id_generator)
            elif 53 < rand <= 58:
                new_fish = Orange(self.get_location(), self.id_generator)

            if self.level not in new_fish.levels:
                continue

            self.fishes.append(new_fish)
            self.id_generator += 1

            time.sleep(self.frequency)

    def get_location(self):
        max_iteration = 20
        for i in range(max_iteration):
            a, b = [random.randint(100, round(gd.SCREEN_WIDTH - 100)), random.randint(100, round(gd.SCREEN_HEIGHT - 100))]
            found = True
            for other in self.fishes:
                # x2 = other.rect.centerx
                # y2 = other.rect.centery
                # if math.sqrt(pow((x2 - a), 2) + pow((y2 - b), 2)) < gd.MIN_DISTANCE / 2:
                if other.rect.collidepoint(a, b):
                    found = False
                    break
            if found:
                return [a, b]

    def spawn_danger_fish(self):
        if not self.work:
            return

        new_fish = DangerFish([0, 0], self.id_generator)
        new_fish.alive = False
        self.fishes.append(new_fish)
        self.id_generator += 1
        blink = BlinkingImage(gd.screen, gd.danger_sign_path, new_fish.get_location(), 0.7, new_fish)
        blink_thread = threading.Thread(target=blink.start)
        blink_thread.daemon = True
        blink_thread.start()
        timer_thread = threading.Timer(gd.DANGER_SIGH_INTERVAL, blink.stop)
        timer_thread.daemon = True
        timer_thread.start()


class BlinkingImage:
    def __init__(self, screen, image_path, position, freq, fish):
        self.screen = screen
        self.fish = fish
        self.image = pygame.image.load(image_path)
        self.position = self.set_position(position)
        self.frequency = freq
        self.active = True
        self.switch = False

    def set_position(self, position):
        y = position[1] - self.image.get_rect().size[1] * 2

        if self.fish.direction == Direction.West:
            x = position[0] - self.image.get_rect().size[0]
        else:
            x = position[0]

        return x, y

    def stop(self):
        self.fish.alive = True
        self.active = False

    def start(self):
        self.switcher()
        while self.active:
            if self.switch:
                self.screen.blit(self.image, self.position)

    def switcher(self):
        if not self.active:
            return

        # waits self.frequency amount of seconds before it calls itself
        threading.Timer(self.frequency, self.switcher).start()
        self.switch = not self.switch