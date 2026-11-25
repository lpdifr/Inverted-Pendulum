use rand::RngExt;
use rand::rngs::SmallRng;
mod neuronnetwork_module;
use neuronnetwork_module::NeuronNetwork;

fn main(){
    let mut rng: SmallRng = rand::make_rng();
    let mut unit = Unit::new();
    let mut nn = NeuronNetwork::new();
    let mut weights_list    = Vec::new();
    //-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124
    for i in 0.. 16{
        let mut weights    = Vec::new();
        weights.push(-9.117011746541309+rng.random_range(-1.0..=1.0));
        weights.push(4.569619100723747+rng.random_range(-1.0..=1.0));
        weights.push(-7.344724531657647+rng.random_range(-1.0..=1.0));
        weights.push(-5.944618933983124+rng.random_range(-1.0..=1.0));
        weights_list.push(weights);
    }
    let mut bias = Vec::new();
    for i in 0.. 4{
        bias.push(rng.random_range(-1.0..=1.0));
        
    }
    nn.init_network(weights_list , bias);
    nn.get_variables(700.0, 0.0, std::f64::consts::PI, 0.0);
    nn.normalize_values();
    let result = nn.calculate_action().clone();
    println!("{:?}", result);
}