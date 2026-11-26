# Source - https://stackoverflow.com/q/74989696
# Posted by Kulo, modified by community. See post 'Timeline' for change history
# Retrieved 2026-11-26, License - CC BY-SA 4.0

import sys, os
import win32api, win32con, win32console
import multiprocessing
class DeveloperConsole:
    def __init__(self):
        self.pause_com = False
        self.continue_com = True
        self.camerastep_com = False
    def ShowConsole(self):
        win32console.FreeConsole()
        win32console.AllocConsole()
        sys.stdout = open("CONOUT$", "w")
        sys.stderr = open("CONOUT$", "w")
        sys.stdin = open("CONIN$", "r")
        print("Test")
        running = True
        while running:
            inp = input(">>> ")
            if inp == "quit":
                running = False
            elif inp == "nextgen":
                print("New generation created.")
            elif inp == "pause":
                if self.pause_com:
                    print("Simulation already paused")
                else:
                    print("Simulation paused")
                    self.pause_com = True
                    self.continue_com = False


            elif inp == "continue":
                if self.continue_com:
                    print("Simulation already continuing")
                else:
                    print("Simulation continued")
                    self.continue_com = True
                    self.pause_com = False

            elif "cameranext" in inp:
                step = inp.split()
                try:
                    print(f"Camera is on step {step[1]}.")
                except IndexError:
                    sectry = input("Set camera step. Or type exit >>> ")
                    if sectry == "exit":
                        pass
                    else:
                        try:
                            sectry = int(sectry)
                        except:
                            print("StepError: cameranext x <-- set num here. try again")
            else:
                print(f"No such command as '{inp}'")
            print("\n")
        os.system("pause")
