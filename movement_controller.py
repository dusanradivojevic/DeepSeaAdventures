import game_data as gd
import threading


def find_index_of_fish(list, fish):
    for i in range(len(list)):
        if fish.id == list[i].id:
            return i

    return -1


# Prevents fishes to go out of the screen and keeps smaller away from larger fish
class MovementController:
    def __init__(self, list):
        self.fishes = list  # list of fishes in the tank

    def control(self):
        for fish in self.fishes:
            if fish.id == -1 \
                or not fish.alive\
                    or fish.size == gd.DANGER_FISH_SIZE:
                continue

            # if fish.rect.centerx - fish.current_image.get_rect().size[0] / 2 < 0:
            #     fish.goOpposite()
            # elif fish.rect.centerx + fish.current_image.get_rect().size[0] / 2 > gd.SCREEN_WIDTH:  # we dont want them to go off the screen
            #     fish.goOpposite()
            # elif fish.rect.centery - fish.current_image.get_rect().size[1] / 2 < 0:
            #     fish.goOpposite()
            # elif fish.rect.centery + fish.current_image.get_rect().size[1] / 2 > gd.SCREEN_HEIGHT:
            #     fish.goOpposite()

            if fish.rect.centerx + fish.current_image.get_rect().size[0] < 0:
                # self.fishes.pop(find_index_of_fish(self.fishes, fish))
                fish.alive = False
            elif fish.rect.centerx - fish.current_image.get_rect().size[0] > gd.SCREEN_WIDTH:
                # self.fishes.pop(find_index_of_fish(self.fishes, fish))
                fish.alive = False
            elif fish.rect.centery + fish.current_image.get_rect().size[1] < 0:
                # self.fishes.pop(find_index_of_fish(self.fishes, fish))
                fish.alive = False
            elif fish.rect.centery - fish.current_image.get_rect().size[1] > gd.SCREEN_HEIGHT:
                # self.fishes.pop(find_index_of_fish(self.fishes, fish))
                fish.alive = False

            if self.endangered(fish) and fish.id != -1 and not fish.endangered:
                fish.change_endangered_status()
                threading.Timer(1, fish.change_endangered_status).start()
                fish.changeDirection()
                fish.move()

    def endangered(self, fish):
        x = fish.rect.centerx
        y = fish.rect.centery
        for other in self.fishes:
            if fish.id == other.id:
                continue

            if fish.size > other.size:
                continue

            x2 = other.rect.centerx
            y2 = other.rect.centery

            min_horizontal_distance = fish.current_image.get_rect().size[0] / 2 + \
                                      other.current_image.get_rect().size[0] / 2 + gd.MIN_DISTANCE
            min_vertical_distance = fish.current_image.get_rect().size[1] / 2 + \
                                      other.current_image.get_rect().size[1] / 2 + gd.MIN_DISTANCE

            if abs(x2 - x) < min_horizontal_distance and abs(y2 - y) < min_vertical_distance:
                if abs(x2 - x) < min_horizontal_distance / 2 and abs(y2 - y) < min_vertical_distance / 2:
                    # if the fish is eaten by the player it will be removed from the
                    # tank in player's class
                    if other.id != -1 and fish.size < ((100 - gd.FISH_SIZE_DIFFERENCE) / 100) * other.size:
                        fish.alive = False
                return True
        return False