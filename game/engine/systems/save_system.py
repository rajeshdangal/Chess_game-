import json

class SaveSystem:
    def save(self, scene):
        data = {
            "board": scene.board.to_dict(),
            "player": scene.current_player
        }

        with open("save.json", "w") as f:
            json.dump(data, f)

    def load(self):
        try:
            with open("save.json") as f:
                return json.load(f)
        except:
            return None