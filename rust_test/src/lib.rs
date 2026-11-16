
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
#[pyclass]
struct Screen{
    width : i32,
    height: i32,
    fps   : f32,
}
#[pyclass]
struct World{
    // Setting screen
    screen  : Screen,

    gravity : f64, // Gravity 900 pixels per
    k       : u8,  // Env resist
    delta_t : f64, // Delta time
    frame   : u32, // Frame counter
    width   : u32, // Screen width
    height  : u32, // Screen height
}

#[pyclass]
struct Cart {

    // Setting world
    world    : World,

    // Setting size variables
    width    : i32,
    height   : i32,
    // Setting screen variables
    cartx    : i32,
    carty    : i32,

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
    cart            : Cart,  // Loading Cart structure

    ax              : f64,   // Setting attachment point
    ay              : f64,

    x1              : f64,   // Setting weight point
    y1              : f64,
                             // Setting
    angle           : f64,      // Angle of pole
    weight_mass     : f64,      // Weight mass
    length          : f64,      // Lenght of pole
    angle_velocity  : f64,      // Angle speed
    alpha_angle     : f64       // Alpha angle
}
impl Pole {
    fn set(&mut self){
        self.ax = self.cart.polex;
        self.ay = self.cart.poley;

        self.endofpole();

        self.weight_mass    =      5.0;

        self.length         =  145.0;

        self.angle          =  std::f64::consts::PI;
        self.angle_velocity =    0.0;
        self.alpha_angle    =    0.0;


    }
    fn endofpole (&mut self){
        self.x1 = self.ax + self.length * self.angle.sin();
        self.y1 = self.ay - self.length * self.angle.cos();
        
    }
    
    fn calculate_phisics(&mut self){
        self.alpha_angle = (self.world.gravity * self.angle.sin() - self.cart.a*self.angle.cos())/self.length;
        self.angle_velocity = self.angle_velocity + self.alpha_angle * self.world.delta_t;
        self.angle = self.angle + self.angle_velocity * self.world.delta_t;
    }
}

impl Cart {
    fn set(&mut self){
        self.cartx = (self.world.screen.width /2) - (self.width/2);
        self.carty = (self.world.screen.height /2) + 300;
        self.polex = (self.world.screen.width / 2) as f64;
        self.poley = ((self.world.screen.height / 2) + 300) as f64;
        self.velocity = 0.0;
        self.cartmass = 5.0;
        self.a = 0.0;
        self.force = 0.0;
    }
    fn calculate_phisics(&mut self){

    }
}

























#[pyfunction]
fn phisics() {
    println!("Hello from rust from python !");
}

#[pymodule]
fn phisics_module(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(phisics , m)?)?;

    Ok(())
}
