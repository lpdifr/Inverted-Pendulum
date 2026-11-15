import pickle

class SaveLoadGen:
    def __init__(self):
        self.last_version_ext = ".lg"
        self.gen_ext = ".gen"
        self.save_folder = "saves"

    # Load gen function
    def LoadLastGen(self ,manual : str = "None"):
        # Open gen version list
        if manual == "None":
            last_gen_file = open(self.save_folder+"/"+"lastgen.lg" , "rb")
        else:
            last_gen_file = manual+".gen"

        # Loading last gen file name
        last_gen_name = pickle.load(last_gen_file)

        # Loading last gen file
        last_gen = open(self.save_folder+"/"+last_gen_name+".gen" , "rb")#type:ignore

        # Loadout data from gen file
        data = pickle.load(last_gen)
        last_gen_file.close()
        last_gen.close()
        # Return data
        return data

    # Save gen function
    def SaveGen(self , weights):
        # Loading last gen data
        last_gen_data = self.LoadLastGen()

        # Setting next gen index
        gen = last_gen_data["gen"] + 1

        # Saving gen data with new gen index
        new_gen_data = {
            "gen" : gen,
            "weights": weights
            }
        
        # Creating new gen file
        new_gen_file = open(self.save_folder+"/"+f"gen_{gen}"+self.gen_ext , "wb")
        
        # Saving data to file
        
        pickle.dump(new_gen_data , new_gen_file)
        new_gen_file.close()
        # Updating lastgen file
        lastgen_list = open(self.save_folder+"/"+ "lastgen.lg" , "wb")
        
        pickle.dump(f"gen_{gen}" , lastgen_list)
        
        lastgen_list.close()
    # Saving raw data to init save system
    def SaveRaw(self , weights):
        last_gen_file = open(self.save_folder+"/"+"lastgen.lg" , "wb")
        raw_name = "gen_0"
        pickle.dump(raw_name , last_gen_file)
        raw_gen = open(self.save_folder+"/"+raw_name+self.gen_ext , "wb")
        raw_data = {
            "gen" : 0,
            "weights" : weights
            }
        pickle.dump(raw_data , raw_gen)
        last_gen_file.close()
        raw_gen.close()
