import random
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "stories")

DAY_FILES = {
    1: "rose_day.txt",
    2: "propose_day.txt",
    3: "chocolate_day.txt",
    4: "teddy_day.txt",
    5: "promise_day.txt",
    6: "hug_day.txt",
    7: "kiss_day.txt"
}

def load_story(day_number, sender_name, partner_name):
    file_name = DAY_FILES.get(day_number)
    if not file_name:
        return ""

    file_path = os.path.join(BASE_PATH, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    stories = [s.strip() for s in content.split("---") if s.strip()]
    story = random.choice(stories)

    story = story.replace("{{sender}}", sender_name)
    story = story.replace("{{partner}}", partner_name)

    return story
