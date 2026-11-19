
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
mod score_module;
mod neuronnetwork_module;
use neuronnetwork_module::NeuronNetwork;
use crate::score_module::ScoreSystem;
#[pyclass]
struct Screen{
    width : f64,
    height: f64,
    fps   : f32,
}
impl Screen {
    fn new() -> Self{
        Self { width: 1700.0, height: 900.0, fps: 60.0 }
    }
}
#[pyclass]
struct World{
    // Setting screen
    screen  : Screen,
    tick    : u32, 
    gravity : f64, // Gravity 900 pixels per
    k       : u8,  // Env resist
    delta_t : f64, // Delta time
    frame   : u32, // Frame counter

    b       : f64
}
impl World {
    fn new() -> Self{
        Self { 
                screen: Screen::new(),
                tick: 0,
                gravity: 900.0,
                k: 4, 
                delta_t: 0.0083333,
                frame: 0,
                b: 4.0
            }
    }
}

#[pyclass]
struct Cart {

    // Setting world
    world    : World,

    // Setting size variables
    width    : f64,
    height   : f64,
    // Setting screen variables
    cartx    : f64,
    carty    : f64,

    // Setting pole position on cart
    polex    : f64,
    poley    : f64,

    // Setting phisics variables
    velocity : f64,
    force    : f64,
    cartmass : f64,
    a        : f64

}
#[pyclass]
struct Pole{
    world           : World, // Loading World structure

    // Standart values
    ax              : f64,   // Setting attachment point
    ay              : f64,

    x1              : f64,   // Setting weight point
    y1              : f64,
                             // Setting
    angle           : f64,      // Angle of pole
    weight_mass     : f64,      // Weight mass
    length          : f64,      // Lenght of pole
    angle_velocity  : f64,      // Angle speed
    alpha_angle     : f64,       // Alpha angle

    // Raw values
    raw_pole_angle  : f64,
    // Normalized values
    radians_normal  : f64,
}

#[pyclass]
struct Unit{
    cart : Cart,
    pole : Pole,
    score: ScoreSystem,
    nn : NeuronNetwork,
   
}

impl Pole {
    fn new()-> Self{
        Self 
        {
            world: World::new(),
            ax: 0.0,
            ay: 0.0,
            x1: 0.0,
            y1: 0.0,
            angle: 0.0,
            weight_mass: 0.0,
            length: 0.0,
            angle_velocity: 0.0,
            alpha_angle: 0.0,
            raw_pole_angle: 0.0,
            radians_normal: 0.0
        }
    }
    fn set_default(&mut self , cart : &Cart){
        self.ax = cart.polex;
        self.ay = cart.poley;

        

        self.weight_mass    =      5.0;

        self.length         =  145.0;

        self.angle          =  std::f64::consts::PI;
        self.angle_velocity =    0.0;
        self.alpha_angle    =    0.0;
        self.endofpole();

    }

    // Normalizing values
    fn normalize_values(&mut self){
        self.radians_normal = ((self.angle + std::f64::consts::PI).rem_euclid((2.0 * std::f64::consts::PI))-std::f64::consts::PI)/std::f64::consts::PI;
    }

    // Calculation endpole x , y
    fn endofpole (&mut self){
        self.x1 = self.ax + self.length * self.angle.sin();
        self.y1 = self.ay - self.length * self.angle.cos();
        
    }
    
    // Calculating phisics of pole
    fn calculate_phisics(&mut self , cart : &Cart){
        self.ax = cart.polex;
        self.alpha_angle = (self.world.gravity * self.angle.sin() - cart.a*self.angle.cos())/self.length;
        self.angle_velocity = self.angle_velocity + self.alpha_angle * self.world.delta_t;
        self.angle = self.angle + self.angle_velocity * self.world.delta_t;
        self.endofpole();
    }
}

impl Cart {
    fn new() -> Self{

        Self 
        { 
            world: World::new(),
            width: 200.0,
            height: 100.0,
            cartx: (1700.0/2.0) - 100.0,
            carty: (900.0/2.0)+300.0,
            polex: 1700.0/2.0,
            poley: (900.0/2.0)+300.0,
            velocity: 0.0,
            force: 0.0,
            cartmass: 0.0,
            a: 0.0 
        }
    }
    fn set_default(&mut self){
        self.cartx = (self.world.screen.width /2.0) - (self.width  / 2.0);
        self.carty = (self.world.screen.height /2.0) + 300.0;
        self.polex = (self.world.screen.width / 2.0);
        self.poley = ((self.world.screen.height / 2.0) + 300.0) as f64;
        self.velocity = 0.0;
        self.cartmass = 5.0;
        self.a = 0.0;
        self.force = 0.0;
    }
    fn calculate_phisics(&mut self , pole : &Pole){
        self.a = (self.force - self.world.b*self.velocity + pole.weight_mass * pole.length * pole.angle_velocity.powi(2) * pole.angle.sin() - pole.weight_mass * self.world.gravity * pole.angle.sin() * pole.angle.cos())/(self.cartmass + pole.weight_mass * pole.angle.sin().powi(2));
        self.velocity = self.velocity + self.a * self.world.delta_t;
        self.cartx = self.cartx + self.velocity  * self.world.delta_t;
        self.polex = (self.cartx + self.width/2.0) as f64;
        
    }
}

impl Unit{
    fn new() -> Self {
        Self { cart: Cart::new(),
               pole: Pole::new(), 
               score:ScoreSystem::new(),
               nn:NeuronNetwork::new(),

            }
    }
    fn reset_unit(&mut self){
        self.cart.set_default();
        self.pole.set_default(&self.cart);
    }
    fn calculate_phisics(&mut self){
        
        self.cart.calculate_phisics(&self.pole);
        self.pole.calculate_phisics(&self.cart);
        
    }
    fn step(&mut self){


        self.nn.get_variables(self.cart.cartx, self.cart.velocity, self.pole.angle, self.pole.angle_velocity);
        self.nn.normalize_values();
        self.cart.force = self.nn.calculate_action().clone() * 3000.0;

        self.calculate_phisics();
        self.score.check_situation(&mut self.cart, &mut self.pole);
        self.score.calculate_score();

        
    }
}

#[pyclass]
struct Simulation{
    units : Vec<Unit>,

}
#[pymethods]
impl Simulation{
    #[new]
    pub(crate) fn new() -> Self{
        Self{
            units : Vec::new()
        }
    }
    fn create_simulation(&mut self , units_quantity: i32 ,weights_set : Vec<f64>){
        self.units = Vec::with_capacity(10_000);
        for _ in 0.. units_quantity{
            let mut unit = Unit::new();

            
            unit.nn.init_network(weights_set.clone());
            unit.cart.set_default();
            unit.pole.set_default(&unit.cart);
            self.units.push(unit);
        }
    }
    pub(crate)fn step(&mut self){
        for unit in &mut self.units{
            unit.step();
            
        }
    } 

}














#[pyfunction]
fn main(weights : Vec<f64>) {
    
    let mut simulation = Simulation::new();
    simulation.create_simulation(10000, weights.clone());
    
}

#[pymodule]
fn rust_module(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Simulation>()?;
    m.add_function(wrap_pyfunction!(main , m)?)?;
    

    Ok(())
}
