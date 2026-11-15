
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn hello_from_rust() {
    println!("Hello from rust from python !");
}

#[pymodule]
fn hello_module(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(hello_from_rust));

    Ok(())
}
