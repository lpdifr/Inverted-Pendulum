use crate::{Cart, Pole , World};
struct SSEI{
    //______________________________________________________
    // Setting manual flags , reward values and reward flags
    //______________________________________________________

    // Setting reward by balance and manual flags for score
    MFBB               : bool,  // Manual flag by balance
    by_balance         : bool,  // Flag by balance tells do we need to give reward
    by_balance_reward  : f64, // Setting reward value by balance

    // Setting reward by stopping
    MFBS               : bool, // Manual flag by stopping
    by_stopping        : bool, // Flag by stopping tells do we need to give reward
    by_stopping_reward : f64, // Setting reward value by stopping

    // Setting reward bonus by degrees value
    MFDB               : bool,
    by_degrees_bonus   : f64,
    by_degrees_reward  : f64,

}
impl SSEI{
    fn set_default(&mut self){
        if self.MFBB{
            self.by_balance = false
        }
        if self.MFBS{
            self.by_stopping = false
        }
        if self.MFDB{
            self.by_degrees_bonus = 0.0
        }
    }
}
pub(crate) struct ScoreSystem{
    score : f32,
    SSEI  : SSEI,
}
impl ScoreSystem{
    fn check_situatione(&mut self, cart: &mut Cart, pole: &mut Pole){

        // Setting default score values
        self.SSEI.set_default();

        // Normalizing values
        pole.normalize_values();
        cart.calculate_phisics(pole);
        // Checking if we need to give reward
        if pole.radians_normal > -0.1 && pole.radians_normal < 0.1 {

            let angle = (pole.angle * (180.0 / std::f64::consts::PI) % 360.0) - 180.0;
            self.SSEI.by_balance = true;
            self.SSEI.by_degrees_bonus = self.SSEI.by_balance_reward as f64 + 1.0 - angle.abs() / 100.0;
        }
        if pole.angle_velocity < 0.0 && cart.a > 0.0 ||  pole.angle_velocity > 0.0 && cart.a < 0.0{
            self.SSEI.by_stopping = true
        }
        
    }
    fn calculate_score(&mut self, cart: &Cart, pole: &Pole){
        if pole.radians_normal > -0.1 && pole.radians_normal < 0.1 {
        }

    }
}