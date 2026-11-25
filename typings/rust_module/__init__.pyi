import numpy as np
import numpy.typing as npt

class Simulation:
    def __init__(self) -> None: ...
    def create_simulation(
        self,
        units_quantity: int,
        weights_set: list[list[float]],
        bias: list[float],
    ) -> None:
        """Создать популяцию с мутированными весами и смещениями."""
        ...
    def step(self, buffer: npt.NDArray[np.float64]) -> None:
        """Выполнить шаг и записать координаты в буфер формы (units_quantity, 3)."""
        ...
    def find_best_unit(self) -> tuple[list[list[float]], list[float]]:
        """Вернуть веса и смещения лучшего юнита."""
        ...
    def reset_simulation(self) -> tuple[list[list[float]], list[float]]:
        """Вернуть параметры победителя и сбросить физику и очки."""
        ...

def main(weights: list[list[float]], bias: list[float]) -> None: ...
