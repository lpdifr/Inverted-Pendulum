use std::{f64, result, vec};

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
    fn set_neuron(&mut self , weights : Vec<f64> ,bias: f64){

        self.b = bias;
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
    weights : Vec<f64>,
    pub(crate)bias   : Vec<f64>
}
impl Layer{
    pub (crate) fn new() -> Self{


        Self
        {
            layer  : Vec::new(),
            weights: Vec::new(),
            bias   : Vec::new(),
        }

    }
    fn set_layer_weights(&mut self , weights : Vec<f64> ){
        self.weights.clear();
        for weight in weights{
            self.weights.push(weight);
        }
    }
    fn fill_layer(&mut self , neuron_quantity : i32){
        for i  in 0..neuron_quantity{
            let mut neuron = Neuron::new();

            let weights_last : Vec<f64> = self.weights.clone();
            

            neuron.set_neuron(weights_last ,self.bias[i as usize]);
            
            
            self.layer.push(neuron);
        }
    }

    fn calculate_z(&mut self , layer_data : Vec<f64>) -> Vec<f64>{
        
        let mut results: Vec<f64> = Vec::new();
        for neuron in self.layer.iter_mut() {
            let neuron_copy = neuron.calculate_vector(layer_data.clone());
            results.push(neuron_copy);
        }
        return results;
    }
}
pub(crate) struct NeuronNetwork{
    // Setting collectable variables
    cartx          : f64,
    cart_velocity  : f64,

    angle          : f64,
    angle_velocity : f64,
    // Setting neuron weights
    layer : Layer,

    pend_data : Vec<f64>,

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
            pend_data : Vec::new()
        }
    }
    pub (crate)fn init_network(&mut self , weights : Vec<f64>){
        self.layer.set_layer_weights(weights);
        self.layer.fill_layer(4);
    }

    pub (crate)fn get_variables(&mut self , cartx : f64 , cart_velocity: f64 , pole_angle : f64 , angle_velocity : f64){
        self.cartx = cartx;
        self.cart_velocity = cart_velocity;
        self.angle = pole_angle;
        self.angle_velocity = angle_velocity;
    }
    pub(crate) fn normalize_values(&mut self){
        self.cartx = (self.cartx - 750.0)/750.0;
        self.angle = ((self.angle + std::f64::consts::PI).rem_euclid((2.0 * std::f64::consts::PI))-std::f64::consts::PI)/std::f64::consts::PI;
        self.cart_velocity = self.cart_velocity/300.0;
        self.angle_velocity = self.angle_velocity/10.0;
    }
    pub (crate)fn set_data_vector(&mut self){
        self.pend_data.clear();
        self.pend_data.push(self.cartx);
        self.pend_data.push(self.cart_velocity);
        self.pend_data.push(self.angle);
        self.pend_data.push(self.angle_velocity);

    }
    pub (crate)fn calculate_action(&mut self) ->f64{
        self.set_data_vector();
        let vector = self.layer.calculate_z(self.pend_data.clone());
        let result = vector.iter().sum::<f64>()/(vector.iter().len() as f64);
        return result;

    }
    
}
