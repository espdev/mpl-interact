# mpl-interact

A library encompassing smart interactions missing in matplotlib

## Usage

The following code enables interactors for GCF:

* zoom by mouse wheel scrolling
* drag by mouse left button
* reset by mouse any button double click

```python
import numpy as np
from matplotlib import pyplot as plt
from mpl_interact import interact

x = np.linspace(0, 2*np.pi, 100)
ys = np.sin(x)
yc = np.cos(x)

plt.plot(x, ys, 'o-', x, yc, 'o-')

interact()

plt.show()
```
