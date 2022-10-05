Thermodynamic properties calculations for gas compositions (GERG 2008)
======================================================================

GasPropertyCalculator is a package for thermodynamic calculations of properties 
of gas compositions according to the GERG 2008 equation of state.

GasPropertyCalculator has the following capabilities:

- Calculation of thermodynamic properties of gas compositions.
- Visualisation of pressure and temperature dependent properties.
- Enthalpy–entropy chart.
- Choice of different unit systems (metric, imperial).
- Choice of different norm state defintions.

Everybody is welcome to use GasPropertyCalculator.

Audience
--------

The audience for GasPropertyCalculator includes engineers, mathematicians, physicists, 
biologists, and anyone else who intends to calculate gas properties.

License
-------

Copyright (C) 2016 Michael Fischer.

GasPropertyCalculator is open source software; you can redistribute it and/or modify 
it under the terms of the :doc:`GPL-3.0 </license>`.

History
-------

GasPropertyCalculator was born in 2016. The software was designed and written by 
Michael Fischer.

Installation
------------

GasPropertyCalculator requires Python 3.7 or higher and builds upon PyQt5 and pyqtgraph. 
It can be installed from Anaconda prompt
using ``pip``.

.. code:: bash

    pip install gaspropertycalculator

GasPropertyCalculator additionally requires the external library 
`LibGergCalc <link URL>`_ 
in order to perform actual calculations.

Nevertheless, the software can installed and run without the library as well. In that case,
only dummy calculations can be performed.

Quick start
-----------

After installation GasPropertyCalculator can be started from Anaconda prompt by

.. code:: bash

    gaspropertycalculator

or from Python prompt by

.. code:: python

    >>> import gaspropertycalculator
    >>> gaspropertycalculator.gaspropertycalculator.run()

Tutorial
--------

An exemplary application of the software is presented in the :doc:`tutorial <tutorial>`.



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
