# mpl-interact

[![PyPI version](https://img.shields.io/pypi/v/mpl-interact.svg)](https://pypi.python.org/pypi/mpl-interact)
[![Build status](https://travis-ci.org/espdev/mpl-interact.svg?branch=master)](https://travis-ci.org/espdev/mpl-interact)
[![Docs status](https://readthedocs.org/projects/mpl-interact/badge/)](https://mpl-interact.readthedocs.io/en/latest/)
[![License](https://img.shields.io/pypi/l/mpl-interact.svg)](LICENSE)

A library encompassing smart interactions missing in matplotlib

**UNDER DEVELOPMENT**

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
