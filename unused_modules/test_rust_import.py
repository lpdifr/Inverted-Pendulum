import rust_module
from rust_module import Simulation


def main():
    simulation = Simulation()
    simulation.step()
    print("Import OK:", rust_module.__file__)
    print("Simulation() and step() OK")


if __name__ == "__main__":
    main()
