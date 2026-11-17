use serde::Serialize;
use serde::Deserialize;
use crate::{Cart, Pole , World};
use std::fs;
#[derive(Serialize)]
struct SSEI_sys_copy{
    //______________________________________________________
    // Setting manual flags , reward values and reward flags
    //______________________________________________________

    // Setting reward by balance and manual flags for score
    
    MFBB               : bool,  // Manual flag by balance

    MFBS               : bool,  // Manual flag by stopping
    MFDB               : bool,  // Manual flag by degrees bonus
    by_balance_reward  : f64, // Setting reward value by balance
    by_stopping_reward : f64, // Setting reward value by stopping
    by_degrees_reward  : f64, // Setting reward value by degrees bonus


    // Setting reward by balance
    by_balance         : bool,  // Flag by balance tells do we need to give reward
    
    // Setting reward by stopping
    by_stopping        : bool, // Flag by stopping tells do we need to give reward
   
    // Setting reward bonus by degrees value
    by_degrees_bonus   : f64,
    
}
#[derive(Deserialize, Default)]
#[serde(default)]

struct SSEI_sys{
    //______________________________________________________
    // Setting manual flags , reward values and reward flags
    //______________________________________________________

    // Setting reward by balance and manual flags for score
    
    MFBB               : bool,  // Manual flag by balance

    MFBS               : bool,  // Manual flag by stopping
    MFDB               : bool,  // Manual flag by degrees bonus
    by_balance_reward  : f64, // Setting reward value by balance
    by_stopping_reward : f64, // Setting reward value by stopping
    by_degrees_reward  : f64, // Setting reward value by degrees bonus


    // Setting reward by balance
    by_balance         : bool,  // Flag by balance tells do we need to give reward
    
    // Setting reward by stopping
    by_stopping        : bool, // Flag by stopping tells do we need to give reward
   
    // Setting reward bonus by degrees value
    by_degrees_bonus   : f64,
    
}
impl SSEI_sys{

    pub(crate) fn set_default(&mut self){

        self.by_balance       = false;
        self.by_stopping      = false;
        self.by_degrees_bonus = 0.0;
    }


}
pub(crate) struct ScoreSystem{
    score : f64,
    SSEI  : SSEI_sys,
}
impl ScoreSystem{
    pub(crate) fn new() -> Self{
        let json_settigns = include_str!("score_manual.json");
        let settings_loaded = false;
        
        let settings : SSEI_sys = 
            serde_json::from_str(json_settigns)
                .expect("Ошибка загрузки настроек очков сималяции");
        

        Self { 
            score: 0.0, 
            SSEI: settings,
         }
    }
    pub(crate) fn check_situatione(&mut self, cart: &mut Cart, pole: &mut Pole){

        // Setting default score values
        

        // Normalizing values
        pole.normalize_values();

        // Checking if we need to give reward
        if pole.radians_normal > -0.1 && pole.radians_normal < 0.1 {

            let angle = pole.radians_normal * 180.0;
            self.SSEI.by_balance = true;
            self.SSEI.by_degrees_bonus = self.SSEI.by_degrees_reward as f64 + 1.0 - angle.abs() / 100.0;
        }
        if pole.angle_velocity < 0.0 && cart.a > 0.0 ||  pole.angle_velocity > 0.0 && cart.a < 0.0{
            self.SSEI.by_stopping = true
        }
        
    }
    pub(crate) fn calculate_score(&mut self){

        // Balance reward
        if self.SSEI.by_balance             && self.SSEI.MFBB{ self.score += self.SSEI.by_balance_reward; }

        // Stopping reward
        if self.SSEI.by_stopping            && self.SSEI.MFBS{ self.score += self.SSEI.by_stopping_reward;}

        // By degrees bonus
        if self.SSEI.by_degrees_bonus > 0.0 && self.SSEI.MFDB{ self.score += self.SSEI.by_degrees_bonus;  }
        self.SSEI.set_default();
    }
}