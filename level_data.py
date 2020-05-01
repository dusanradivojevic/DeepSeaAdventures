import npc
import random


def get_random_task(level):
    index = random.randint(0, len(tasks) - 1)
    while tasks[index].level != level:
        index = random.randint(0, len(tasks) - 1)
    return tasks[index]


# Names that will be used in display instead class names
def get_name_of_type(tp):
    if tp == npc.NpcSprite:
        return 'Any'
    elif tp == npc.Yellow:
        return 'Yellow fish'
    elif tp == npc.Killer:
        return 'Killer shark'
    elif tp == npc.Stripes:
        return 'Stripes fish'
    elif tp == npc.Dark:
        return 'Grey fish'
    elif tp == npc.Tuna:
        return 'Tuna fish'
    elif tp == npc.Red:
        return 'Red shark'
    elif tp == npc.Tropical:
        return 'Tropical fish'
    elif tp == npc.Zebra:
        return 'Zebra fish'
    elif tp == npc.Guppy:
        return 'Guppy'
    elif tp == npc.Tiger:
        return 'Tiger fish'
    elif tp == npc.Pixel:
        return 'Pixel'
    elif tp == npc.Neon:
        return 'Neon fish'
    elif tp == npc.Color:
        return 'Colorful fish'
    elif tp == npc.Disc:
        return 'Disc fish'
    elif tp == npc.Orange:
        return 'Small orange'
    elif tp == npc.DangerFish:
        return 'Danger fish'

    return 'Unknown'  # if type is wrong


# Each level will have a task that need to be fulfilled before going to the next one
class Task:
    def __init__(self, level, score, fish_num, fish_type):
        self.level = level
        self.score_needed = score  # 0 if not needed
        self.fish_numbers = fish_num  # array of numbers
        self.fish_types = fish_type  # array of objects (NpcSprite == any type of fish)


# Predefined tasks
tasks = [
    Task(1, 200, [], []),
    Task(1, 100, [8], [npc.NpcSprite]),
    Task(1, 100, [2, 3], [npc.Color, npc.Neon]),
    Task(1, 100, [1, 4], [npc.Pixel, npc.Disc]),
    Task(1, 75, [2, 2, 2], [npc.Orange, npc.Disc, npc.Color]),
    Task(3, 500, [], []),
    Task(3, 250, [6, 3], [npc.Tuna, npc.Red]),
    Task(3, 250, [2, 7], [npc.Stripes, npc.Dark]),
    Task(3, 200, [4, 4, 4], [npc.Guppy, npc.Tuna, npc.Dark]),
    Task(2, 300, [], []),
    Task(2, 150, [11], [npc.NpcSprite]),
    Task(2, 150, [4, 3], [npc.Zebra, npc.Tropical]),
    Task(2, 150, [2, 5], [npc.Guppy, npc.Tiger]),
    Task(2, 100, [3, 3, 3], [npc.Zebra, npc.Guppy, npc.Tropical]),
    Task(4, 1000, [], []),
    Task(4, 800, [5, 6], [npc.Yellow, npc.Tuna]),
    Task(4, 800, [7, 4], [npc.Killer, npc.Tropical])
]