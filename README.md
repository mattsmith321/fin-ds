<a name="readme-top"></a>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Financial data sources (fin-ds)

Financial Data Sources (fin-ds) is a Python package for retrieving financial OHLCV data from a data source using a common interface and returning a standardized pandas DataFrame. Using the library is as simple as:

```python
ds = DataSourceFactory("Tinngo")
df = df.get_ticker_data("AAPL")
```

Here are the column mappings from each data source into fin-ds:
| fin-ds    | Alpha Vantage      | EODHD     | Nasdaq    | Tiingo      | Yahoo Finance |
| :---      | :---               | :---      | :---      | :---        | :---          |
| date      | date               | date      | date      | date        | Date          |
| open      | 1. open            | open      | open      | open        | Open          |
| high      | 2. high            | high      | high      | high        | High          |
| low       | 3. low             | low       | low       | low         | Low           |
| close     | 4. close           | close     | close     | close       | Close         |
| volume    | 6. volume          | volume    | volume    | volume      | Volume        |
| adj_open  | -                  | -         | adj_open  | adjOpen     | -             |
| adj_high  | -                  | -         | adj_high  | adjHigh     | -             |
| adj_low   | -                  | -         | adj_low   | adjLow      | -             |
| adj_close | 5. adjusted close  | adj_close | adj_close | adjClose    | Adj Close     |
| dividend  | 7. dividend amount | -         | dividend  | divCash     | -             |
| split     | -                  | -         | split     | splitFactor | -             |
| -         | -                  | symbol    | ticker    | -           | -             |
| -         | -                  | interval  | -         | -           | -             |



## Overview


## Getting started

### Requirements

The detailed requirements are spelled out in the requirements.txt file but at a high level, the following packages are required:
* pandas - Because pandas makes data analysis so much easier.
* python-decouple - Used to pull API keys from environment variables.
* Data source clients - Install the following packages for each data source you plan to use:
  * [alpha-vantage](https://pypi.org/project/alpha-vantage/)
  * [eodhd](https://pypi.org/project/eodhd/)
  * [nasdaq-data-link](https://pypi.org/project/Nasdaq-Data-Link/)
  * [tiingo](https://pypi.org/project/tiingo/)
  * [yfinance](https://pypi.org/project/yfinance/)
  * [openpyxl](https://pypi.org/project/openpyxl/) - Technically not a data source but needed if reading from Excel.

### Installation

As with many other Python applications, it is recommended to install this package in a virtual environment.

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
* 0.3.1 - Fixed how tickers with special characters are handled (at least for BRK-A).
* 1.0.0 - Made changes to class and module names to support dynamic loading.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
