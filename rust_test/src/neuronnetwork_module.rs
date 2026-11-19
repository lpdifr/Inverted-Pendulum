use rand::RngExt;
use rand::rngs::SmallRng;

//for future random weights generator
// rand::thread_rng().gen_range(1..=100);
struct Neuron{
    weights_list : Vec<f64>, // All links data
    z : f64, // sum before activation
    b : f64, // bias
    a : f64, // after activation
}
impl Neuron{
    pub(crate) fn new() -> Self{

        Self
        {
            weights_list : Vec::new(),
            z     : 0.0,
            b     : 0.0,
            a     : 0.0,
        }
    } 
    fn set_neuron(&mut self , weights : Vec<f64>){
        let mut rng: SmallRng = rand::make_rng();
        self.b = (rng.random_range(-1.0..=1.0)) * 2.0 - 1.0;
        self.weights_list.clear();
        for weight in weights{
            self.weights_list.push(weight);
        }
    
    }
    fn calculate_vector(&mut self , incoming_data : Vec<f64>) -> f64{
        
        if incoming_data.len() != self.weights_list.len(){
            panic!("Incoming data number does not match weight's number.")
        }

        self.z = 0.0;
        for i in 0..incoming_data.len(){

            self.z += self.weights_list[i] * incoming_data[i];
        }

        self.z += self.b;
        self.a = self.z.tanh();
        
        return self.a;
    }
}
struct Layer{
    layer   : Vec<Neuron>,
    weights : Vec<f64>
}
impl Layer{
    pub (crate) fn new() -> Self{


        Self
        {
            layer  : Vec::new(),
            weights: Vec::new()
        }

    }
    fn set_layer_weights(&mut self , weights : Vec<f64>){
        for weight in weights{
            self.weights.push(weight);
        }
    }
    fn fill_layer(&mut self , neuron_quantity : i32){
        for i in 0..neuron_quantity{
            let mut neuron = Neuron::new();
            let mut rng: SmallRng = rand::make_rng();
            let weights_copy : Vec<f64> = self.weights.clone();
            let mut weights_last : Vec<f64> = self.weights.clone();
            
            weights_last.clear();
            for weight in weights_copy{
                weights_last.push(weight+(rng.random_range(-1.0..=1.0)) * 2.0 - 1.0);
            }
            neuron.set_neuron(weights_last);
            
            
            self.layer.push(neuron);
        }
    }

    fn calculate_z(&mut self , layer_data : Vec<f64>) -> Vec<f64>{
        let a = 0.0;
        let mut results: Vec<f64> = Vec::new();
        for neuron in self.layer.iter_mut() {
            let neuron_copy = neuron.calculate_vector(layer_data.clone());
            results.push(neuron_copy);
        }
        return results;
    }
}
struct NeuronNetwork{
    // Setting collectable variables
    cartx          : f64,
    cart_velocity  : f64,

    angle          : f64,
    angle_velocity : f64,
    // Setting neuron weights
    layer : Layer,


}
impl NeuronNetwork{
    pub (crate) fn new() -> Self{
        Self
        {
            cartx : 0.0,
            cart_velocity : 0.0,
            angle : 0.0,
            angle_velocity : 0.0,
            layer : Layer::new(),
        }
    }
    fn get_variables(&mut self , cartx : f64 , cart_velocity: f64 , pole_angle : f64 , angle_velocity : f64){
        self.cartx = cartx;
        self.cart_velocity = cart_velocity;
        self.angle = pole_angle;
        self.angle_velocity = angle_velocity;
    }

    
}