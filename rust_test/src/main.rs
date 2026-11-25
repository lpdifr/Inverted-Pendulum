mod neuronnetwork_module;
use neuronnetwork_module::NeuronNetwork;
fn main(){
    let mut nn = NeuronNetwork::new();
    let mut weights    = Vec::new();
    //-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124
    weights.push(-9.117011746541309);
    weights.push(4.569619100723747);
    weights.push(-7.344724531657647);
    weights.push(-5.944618933983124);
    nn.init_network(weights , (1 .,2.0 ,3.0, 4.0,));
    nn.get_variables(700.0, 0.0, std::f64::consts::PI, 0.0);
    nn.normalize_values();
    let result = nn.calculate_action().clone();
    println!("{:?}", result);
}