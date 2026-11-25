# Inverted Pendulum

Симулятор тележки с перевёрнутым маятником. Популяция контроллеров оценивается по результатам симуляции. Веса победителя служат основой следующего поколения.

## Точки входа

- `main.py` — Python-приложение. Создаёт окно GLFW/OpenGL, определяет `Environment`, загружает веса и запускает цикл кадров. По умолчанию моделирует 10 000 агентов, рисует до 100 и вызывает смену поколения каждые 60 секунд.
- `rust_test/Cargo.toml` — Rust-пакет. `rust_test/src/lib.rs` экспортирует расширение `rust_module` через PyO3. `rust_test/src/main.rs` — отдельный пример вычисления действия контроллера.
- Текущий цикл `main.py` вызывает Python-реализацию через `Units.SimulationStep()`. Импорт `rust_module` при этом обязателен для запуска. Одноимённый импорт `Simulation` в `main.py` перекрывает Python-импорт, но `Unit` берёт Python-класс из `simulation_module.py` напрямую.

## Где менять поведение

| Задача | Файл и символы |
| --- | --- |
| Размер популяции, таймер поколений, параметры мира | `main.py`: `units_quantity`, `max_frame`, `Environment`. |
| Мутации и отбор | `units_module.py`: `Units.CreateUnits()`, `ReturnBestUnit()`, `NewGen()`. |
| Входы контроллера и управляющая сила | `simulation_module.py`: `Simulation.step()` нормализует положение и скорость тележки, угол и угловую скорость маятника, затем умножает выход контроллера на 1500. Вычисление сети — `neuralnetwork_module.py`, класс `NerualNetwork` (имя как в исходнике). |
| Физика Python | `cart_module.py` и `pole_module.py`: методы `PhisicsCalculate()`. |
| Баллы и сброс в Python | `simulation_module.py`: `Simulation.Score.ScoreSystem()`, `Simulation.reset()`. Параметры наград — `SSEI_module.py`. |
| Отрисовка | `render_module.py`, вызовы и лимит `max_render` — в `Units.SimulationStep()`. |
| Физика и популяция Rust | `rust_test/src/lib.rs`: типы `Cart`, `Pole`, `Unit`, `Simulation`. Сеть — `neuronnetwork_module.rs`, оценка — `score_module.rs` и встроенный через `include_str!` файл `score_manual.json`. |
| Хранение весов | `gen_saver.py`: `SaveLoadGen` читает и пишет `saves/gen_*.gen` с полями `gen` и `weights`, указатель `saves/lastgen.lg` и журнал `saves/log.txt`. |

## Контракты и особенности текущего кода

- Путь выполнения Python: `main.py → Units.SimulationStep() → Simulation.step() → контроллер → Cart/Pole → ScoreSystem()`. На смене поколения `NewGen()` выбирает максимальный балл и создаёт мутированные копии весов.
- Python загружает плоский список весов из сохранения. Rust-метод `create_simulation()` принимает вложенные списки весов и отдельный список смещений. Rust-метод `step(buffer)` ожидает изменяемый двумерный NumPy-массив `float64` с одной строкой на агента и тремя столбцами для позиции тележки и координат конца маятника.
- В Python `Units.best_score` инициализируется нулём и не обновляется в `NewGen()`. При работе с таймерами учитывай, что `main.py` обновляет локальный `frame_counter`, а система баллов читает `world.frame_counter`.
- `enviroment_module.py` и `rust_test/src/phisics_module.rs` сейчас пусты. Реальные определения находятся в точках входа, указанных выше.

## Запуск и проверка

- Python-приложение запускается из корня командой `python main.py`, поскольку пути к `saves/` относительные. По исходникам требуются Pygame, glfw, PyOpenGL, NumPy и импортируемый `rust_module`. Для синтаксиса вложенных f-строк в `gen_saver.py` нужен Python 3.12+.
- Обычный запуск пишет в журнал и может создать новое сохранение. Для проверки, где нужно сохранить исходный набор поколений, используй рабочую копию `saves/`. Файлы поколений сериализованы через `pickle`. Загружай их только из доверенного источника.
- Для проверки типов и компиляции Rust есть `cargo check --manifest-path rust_test/Cargo.toml`. Для проверки импорта нужен собранный и доступный Python модуль `rust_module`.
- `test_rust_import.py` вызывает `Simulation.step()` без обязательного буфера и расходится с текущей сигнатурой Rust. `tests/test_10000_carts.py` — отдельная демонстрация нагрузки на Pygame. Корневой `test.py` — короткий эксперимент с поиском индекса.
