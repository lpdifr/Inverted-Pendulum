import pickle

from datetime import datetime , date

class SaveLoadGen:
    def __init__(self):
        self.last_version_ext = ".lg"
        self.gen_ext = ".gen"
        self.save_folder = "saves"
        self.log_name = "log.txt"
        
    # Load gen function
    def LoadLastGen(self ,manual : str = "None"):
        now = datetime.now()
        log = open(self.save_folder+"/"+self.log_name , "a")
        for i in range(3):

            log.write("\n")
        # Open gen version list
        if manual == "None":
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded generation name in NoneManualMode" + "\n")
            last_gen_file = open(self.save_folder+"/"+"lastgen.lg" , "rb")
            last_gen_name = pickle.load(last_gen_file)
        else:
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded generation name in ManualMode" + "\n")
            last_gen_name = "gen_"+str(manual)

        # Loading last gen file name
        #

        # Loading last gen file
        if manual == "None":
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded last generation file in NoneManualMode" + "\n")
        else:
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded last generation file in ManualMode" + "\n")
        last_gen = open(self.save_folder+"/"+last_gen_name+".gen" , "rb")#type:ignore
        if manual == "None":
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded last generation file was successful in NoneManualMode" + "\n")
        else:
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loaded last generation file was successful in ManualMode" + "\n")
        # Loadout data from gen file
        try:
            data = pickle.load(last_gen)
        except pickle.UnpicklingError:
            if manual == "None":
                log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loading last generation file was not successful in NoneManualMode" + "\n")
            else:
                log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loading last generation file was not successful in ManualMode" + "\n")
            return 0

        if manual == "None":
            last_gen_file.close()
        last_gen.close()
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Loading last generation file was FULL successful" + "\n")
        log.close()
        
        # Return data
        return data

    # Save gen function
    def SaveGen(self , weights):
        now = datetime.now()
        log = open(self.save_folder+"/"+self.log_name , "a")

        # Loading last gen data
        
        last_gen_data = self.LoadLastGen()
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing gen index..." + "\n")
        # Setting next gen index
        gen = last_gen_data["gen"] + 1
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing gen index was successful" + "\n")
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing new gen data..." + "\n")
        # Saving gen data with new gen index
        new_gen_data = {
            "gen" : gen,
            "weights": weights
            }
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing new gen data was successful" + "\n")
        # Creating new gen file
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Creating new gen data file..." + "\n")
        new_gen_file = open(self.save_folder+"/"+f"gen_{gen}"+self.gen_ext , "wb")
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Creating new gen data file was successful" + "\n")
        # Saving data to file
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing to save new gen data file..." + "\n")
        pickle.dump(new_gen_data , new_gen_file)
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Finished to save new gen data" + "\n")
        new_gen_file.close()
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; New gen data file was successful closed" + "\n")
        # Updating lastgen file
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing to change lastgen.lg..." + "\n")
        try:
            lastgen_list = open(self.save_folder+"/"+ "lastgen.lg" , "wb")
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Changing was successful." + "\n")
        except:
            log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Changing was not successful."+ "\n")
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Prepearing to change lastgen.lg second time..." + "\n")
        pickle.dump(f"gen_{gen}" , lastgen_list)
        log.write(f"On {date.today()} ; In {now.strftime("%H:%M:%S")}; Changing was successful."+ "\n")
        
        lastgen_list.close()
    # Saving raw data to init save system
    def SaveManual(self , weights , bias , gen):
        last_gen_file = open(self.save_folder+"/"+"lastgen.lg" , "wb")
        raw_name = "gen_" + str(gen)
        pickle.dump(raw_name , last_gen_file)
        raw_gen = open(self.save_folder+"/"+raw_name+self.gen_ext , "wb")
        raw_data = {
            "gen" : gen,
            "weights" : weights,
            "bias" : bias
            }
        pickle.dump(raw_data , raw_gen)
        last_gen_file.close()
        raw_gen.close()
slg = SaveLoadGen()
def FIX_LAST_GEN_FILE(last_working_gen):
    a = slg.LoadLastGen(last_working_gen)
    slg.SaveManual(a["weights"] , last_working_gen + 1)
