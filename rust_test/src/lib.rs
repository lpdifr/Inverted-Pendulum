
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn hello_from_rust() {
    println!("Hello from rust from python !");
}

#[pymodule]
fn phisics_module(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_rust , m)?)?;

    Ok(())
}
