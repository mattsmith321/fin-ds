<a name="readme-top"></a>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Financial data sources (fin-ds)

## Overview


## Getting started

### Requirements

The detailed requirements are spelled out in the requirements.txt file but at a high level, the following packages are required:
* pandas - Because pandas makes data analysis so much easier.
* python-decouple - Used to pull API keys from environment variables.
* Data source clients - Install the following packages for each data source you plan to use:
** [alpha-vantage](https://pypi.org/project/alpha-vantage/)
** [eodhd](https://pypi.org/project/eodhd/)
** [nasdaq-data-link](https://pypi.org/project/Nasdaq-Data-Link/)
** [tiingo](https://pypi.org/project/tiingo/)
** [yfinance](https://pypi.org/project/yfinance/)
** [openpyxl](https://pypi.org/project/openpyxl/) - Technically not a data source but needed if reading from Excel.

### Installation

As with many other Python applications, tt is recommended to install this package in a virtual environment.

```bash
$ pip install git+https://github.com/mattsmith321/fin-ds.git
```

#### Examples

In order for the references in the examples folder to work, the package must be installed within the application directory.
```bash
$ pip install -e .
```

### Configuration
At this point in time, there are no exposed configuration options.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Troubleshooting

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Release history
* 0.3.0 - Added Nasdaq data sources using [nasdaq-data-link](https://pypi.org/project/Nasdaq-Data-Link/) package.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
