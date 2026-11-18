use rand::Rng;
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
    fn set_neuron_weight(&mut self , weights : Vec<f64>){
        self.weights_list.clear();
        for weight in weights{
            self.weights_list.push(weight);
        }
    
    }
    fn calculate_vector(&mut self , incoming_data : Vec<f64>){
        
        if incoming_data.len() != self.weights_list.len(){
            panic!("Incoming data number does not match weight's number.")
        }

        self.z = 0.0;
        for i in 0..incoming_data.len(){

            self.z += self.weights_list[i] * incoming_data[i];
        }

        self.z += self.b;
        self.a = self.z.tanh();
    }
}
struct Layer{
    layer : Vec<Neuron>
}
impl Layer{
    pub (crate) fn new() -> Self{


        Self
        {
            layer : Vec::new(),

        }

    }

    fn fill_layer(&mut self){

    }
    fn calculate_z(&mut self){
        let a = 0.0;
        for (index ,neuron) in self.layer.enumerate(){
            if index == 0{
                a += neuron.z;
            }
            if index > 0{
                a += neuron.z - self.layer[index] + self.layer[index].b;
            }
            
        }
    }
}
struct NeuronNetwork{
    // Setting collectable variables
    cartx          : f64,
    cart_velocity  : f64,

    angle          : f64,
    angle_velocity : f64,
    // Setting neuron weights

    w1             : f64,
    w2             : f64,
    w3             : f64,
    w4             : f64,
    weight_n       : f64,
    weights_list   : Vec<f64>,

    // Setting Neuron
    S_list         : Vec<f64>,
    z              : f64,
    b              : f64 
}
impl NeuronNetwork{
    pub (crate) fn new() -> Self{
        Self
        {
            cartx : 0.0,
            cart_velocity : 0.0,
            angle : 0.0,
            angle_velocity : 0.0,

            w1 : 0.0,
            w2 : 0.0,
            w3 : 0.0,
            w4 : 0.0,
            weights_list  : 0.0,
            S_list : 0.0,
            z  : 0.0,
            b : 0.0,
        }
    }
    fn get_variables(&mut self , cartx : f64 , cart_velocity: f64 , pole_angle : f64 , angle_velocity : f64){
        self.cartx = cartx;
        self.cart_velocity = cart_velocity;
        self.angle = pole_angle;
        self.angle_velocity = angle_velocity;
    }
    fn set_weights(&mut self , weights : Vec<f64>){
        for weight in weights{
            self.weights_list.push
        }
        
    }
}