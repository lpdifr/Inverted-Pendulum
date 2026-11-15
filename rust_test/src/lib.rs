
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
#[pyclass]
struct World{
    gravity : u32, // Gravity 900 pixels per
    k       : u8,  // Env resist
    delta_t : u64, // Delta time
    frame   : u32, // Frame counter
    width   : u32, // Screen width
    height  : u32, // Screen height
}

#[pyclass]
struct Pole{

}
#[pyclass]
struct Cart {
    velocity : u32,
    force : u32,
    cartmass : u32,
    cartx : u32


}
#[pyfunction]
fn phisics() {
    println!("Hello from rust from python !");
}

#[pymodule]
fn phisics_module(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_rust , m)?)?;

    Ok(())
}
