
import sys, os
import win32api, win32con, win32console
import multiprocessing
class DeveloperConsole:
    def __init__(self):
        self.startsimulation = multiprocessing.Value("b" , False)
        self.quit_com = multiprocessing.Value("b" , False)
        self.pause_com = multiprocessing.Value("b" , False)
        self.continue_com = multiprocessing.Value("b" , True)
        self.camerastep_com = multiprocessing.Value("b" , False)
        self.population = 10000
        self.render_range = multiprocessing.Array("i", [0, 100])
        self.brandnewsim = multiprocessing.Value("b" , False)
        self.render = multiprocessing.Value("b" , True)
        self.HelpTextPATH = "hf/help_console.txt"

    def ShowConsole(self):
        win32console.FreeConsole()
        win32console.AllocConsole()
        sys.stdout = open("CONOUT$", "w")
        sys.stderr = open("CONOUT$", "w")
        sys.stdin = open("CONIN$", "r")
        print("Inverted Pendelum console. Ver 1.0\nTo start simulation enter 'start_simulation'.\nBefore start you can change simulation parametrs.")
        running = True
        while running:
            inp = input(">>> ")
            if inp == "start_simulation":
                self.startsimulation.value = True
                print("Simulation starting in 3...\nSimulation starting in 2...\nSimulation starting in 1...")
            elif inp == "quit":
                self.quit_com.value = True
                running = False
            elif inp == "help":
                textfile = open(self.HelpTextPATH , "r")
                text = textfile.read()
                print(text)
                textfile.close()
            elif inp == "nextgen":
                print("New generation created.")
            
            elif inp == "pause":
                if self.pause_com.value:
                    print("Simulation already paused")
                else:
                    print("Simulation paused")
                    self.pause_com.value = True
                    self.continue_com.value = False

            elif inp == "continue":
                if self.continue_com.value:
                    print("Simulation already continuing")
                else:
                    print("Simulation continued")
                    self.continue_com.value = True
                    self.pause_com.value = False

            elif "cameranext" in inp.split():
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
            
            elif "set" in inp.split():
                if "--render" in inp.split():
                    if not self.startsimulation.value:
                        sp = inp.split()
                        if sp[len(sp)-1] == "true":
                            self.render.value = True
                            print("Render ON")
                        elif sp[len(sp)-1] == "false":
                            self.render.value = False
                            print("Render OFF")
                        else:
                            print(f"Unknown flag as {sp[len(sp)-1]}")
                    else:
                        print("You need to write '--render' before you start simulation")
                if "--renderrange" in inp.split():
                    sp = inp.split()
                    self.render_range[0] = int(sp[len(sp)-2])
                    self.render_range[1] = int(sp[len(sp)-1])
                    print(f"Render range setted on {self.render_range}")
                if "--population" in inp.split():
                    sp = inp.split()
                    self.population = int(sp[len(sp)-1])
                    print(f"Population setted on {self.population}")
                if "--rules" in inp.split():
                    pass
            elif inp == "brandnewsim":
                self.brandnewsim.value = True
                print("Creating new simulation")
            else:
                print(f"No such command as '{inp}'")

            print("\n")

if __name__ == "__main__":
    devcon = DeveloperConsole()
    p = multiprocessing.Process(target=devcon.ShowConsole)
    p.start()
    p.join()
    print(p.exitcode)