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
    if tp == npc.YellowFish:
        return 'Yellow fish'
    if tp == npc.YellowStrapeFish:
        return 'Yellow-strape fish'
    if tp == npc.BlueFish:
        return 'Blue fish'
    if tp == npc.GreyFish:
        return 'Grey fish'
    if tp == npc.BullShark:
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
    Task(1, 100, [], []),
    Task(1, 100, [10], [npc.NpcSprite]),
    Task(3, 0, [6, 3], [npc.YellowStrapeFish, npc.BlueFish]),
    Task(2, 300, [4], [npc.GreyFish]),
    Task(5, 0, [1], [npc.BullShark])
]