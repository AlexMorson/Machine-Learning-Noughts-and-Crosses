# Machine-Learning-Noughts-and-Crosses
## boards.pickle
This is a file that contains all (even-moved) board states.  
Here is an example of how to load this into a program.
```python
from enum import Enum
import pickle

class Tile(Enum):
    Empty = 0
    Noughts = 1
    Crosses = 2

with open("boards.pickle", "rb") as file:
    boards = pickle.load(file)
```
Note that the `Tile` enum must be defined before loading the data!
