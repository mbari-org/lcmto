# LCMTO LCM log conversion utility

This is a simple package for use on Python (>3.6) that facilitates conversion of LCM files into Pandas dataframes and CSV files.

## Installation

See package dependencies in `requirements.txt`

Using `pip`:

    python -m pip install -r requirements.txt
    python -m hatchling build
    python -m pip install dist/lcmto-0.2.0-py2.py3-none-any.whl

## Getting Started

Once installed, this utility assumes you have employed [`lcm-gen`](https://linux.die.net/man/1/lcm-gen) to generate types and have those available to your python environment, either installed in your site-packages, or referenced through export of `PYTHONPATH` or within code using `sys.path.append`.

### Reading in a Dataframe

See the help for `lcmto.dataframe()`

### Creating a CSV-file

See the help for `lcmto.csv()`
