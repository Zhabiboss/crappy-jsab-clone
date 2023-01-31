from classes import *
import pygame
import sys

class LevelMenu(MenuTemplate):
    def __init__(self):
        super().__init__()
        self.buttons.append(StylizedButton(0, 0, "Exit", self.exit))

    def exit(self):
        self.exited = True

class MainMenu(MenuTemplate):
    def __init__(self):
        super().__init__()
        self.buttons.append(StylizedButton(0, 0, "Levels", self.startLevels))

    def startLevels(Self):
        LevelMenu().run()
        
if __name__ == "__main__":
    app = MainMenu()
    app.run()