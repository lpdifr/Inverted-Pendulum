
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
#[pyclass]
struct Screen{
    width : i32,
    height: i32,
    fps   : f16,
}
#[pyclass]
struct World{
    // Setting screen
    screen  : Screen,

    gravity : u32, // Gravity 900 pixels per
    k       : u8,  // Env resist
    delta_t : u64, // Delta time
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
    polex    : f32,
    poley    : f32,

    // Setting phisics variables
    velocity : f32,
    force    : f32,
    cartmass : f32,
    a        : f32

}
#[pyclass]
struct Pole{
    world           : World, // Loading World structure
    cart            : Cart,  // Loading Cart structure

    ax              : f32,   // Setting attachment point
    ay              : f32,

    x1              : f32,   // Setting weight point
    y1              : f32,
                             // Setting
    angle           : f32,      // Angle of pole
    weight_mass     : u32,      // Weight mass
    length          : f32,      // Lenght of pole
    angle_velocity  : f32,      // Angle speed
    alpha_angle     : f32       // Alpha angle
}
impl Pole {
    fn set(&mut self){
        self.ax = self.cart.polex;
        self.ay = self.cart.poley;

        self.endofpole();

        self.weight_mass    =      5;

        self.length         =  145.0;

        self.angle          =  std::f32::consts::PI;
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
        self.cartx = self.world.screen.width   as f32/2.0 - self.width/2;
        self.carty = (self.world.screen.height as f32/2.0) + 300;
        self.polex = self.world.screen.width   as f32 /2.0;
        self.poley = (self.world.screen.height as f32/2.0) + 300;
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
