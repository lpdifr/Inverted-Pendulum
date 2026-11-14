class Simulation_Score_Increase_Event:
        def __init__(self):

            self.by_balance  = 0# flag
            self.MFBB = 1 # Manual flag bonus if 0: reward will be ignored
            # Balance reward value
            self.bbr = 1

            # Reward
            self.by_stopping = 1# flag

            self.MFBS = 1 # Manual flag bonus if 0: reward will be ignored
            # Stopping rewart value
            self.bsr = 3

            # Increase score by degrees bonus
            self.degrees_bonus = 0
            self.MFDB = 1 # Manual flag bonus if 0: reward will be ignored
            # If AI just hanging around and does nothing we reduce his score
            self.AFK_bonus = 10
            self.MFAB = 0
            # Score sum
            self.score_sum = 0
