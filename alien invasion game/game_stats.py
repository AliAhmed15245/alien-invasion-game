import pygame, json

def high_score(file_name):
    with open(file_name, "r") as f_obj:
        return json.load(f_obj)


class States:
    def __init__(self, ai_settings):
        h_score = high_score("score.json")
        self.ai_settings = ai_settings
        self.ships_left = self.ai_settings.ships_left
        self.game_active = False
        self.score = 0
        self.level = 1
        self.high_score = h_score

    def reset_stats(self):
        self.ships_left = self.ai_settings.ships_left
        self.score = 0
        self.level = 1