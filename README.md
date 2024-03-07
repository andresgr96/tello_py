## Install using pip
```
pip install djitellopy
```

For Linux distributions with both python2 and python3 (e.g. Debian, Ubuntu, ...) you need to run
```
pip3 install djitellopy
```

## Install in developer mode
Using the commands below you can install the repository in an _editable_ way. This allows you to modify the library and use the modified version as if you had installed it regularly.

```
git clone https://github.com/damiafuentes/DJITelloPy.git
cd DJITelloPy
pip install -e .
```

## Usage
### API Reference
See [djitellopy.readthedocs.io](https://djitellopy.readthedocs.io/en/latest/) for a full reference of all classes and methods available.

### Simple example
```python
from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(100)
tello.rotate_counter_clockwise(90)
tello.move_forward(100)

tello.land()
```
