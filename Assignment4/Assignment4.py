import sys
import os
import json
import glob
from Game import Game

path_to_content = 'content'


def main():
    content_path = os.path.join(os.path.dirname(__file__), path_to_content)
    scenes = []

    for json_file in glob.glob(content_path + '/*.json'):
        with open(json_file) as file:
            data = json.load(file)
            for scene in data:
                scenes.append(scene)

    game_instance = Game(scenes)
    game_instance.start()

    while game_instance.is_running:
        # Process game events
        game_instance.execute()

    sys.exit()


if __name__ == "__main__":
    main()
