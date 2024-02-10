<a name="readme-top"></a>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Financial data sources (fin-ds)

`fin-ds` (financial data sources) is a Python package for retrieving financial OHLCV data from a data source using a common interface and returning a standardized pandas DataFrame. Using the library is as simple as:

```python
ds = DataSourceFactory("Tiingo")
df = df.get_ticker_data("AAPL")
```

To see the list of available data sources call `DataSourceFactory.data_sources`:
```python
['AlphaVantage', 'EODHD', 'NasdaqDataLink', 'Tiingo', 'YFinance']
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

`fin-ds` is a Python package designed to simplify the process of fetching financial OHLCV (Open, High, Low, Close, Volume) data from various sources through a unified interface. It abstracts away the differences between data source APIs, returning data in a standardized pandas DataFrame format. This makes it an ideal tool for financial analysis, algorithmic trading strategy development, and data science projects focusing on financial markets.


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

### Built-in data sources
The package comes with a variety of built-in data sources that can be easily accessed and used to fetch data. To use a built-in data source, simply instantiate the DataSourceFactory with the name of the data source you wish to use.

Example:
```python
from fin_ds import DataSourceFactory

# Create an instance of the AlphaVantage data source
alpha_vantage_ds = DataSourceFactory("AlphaVantage")

# Now you can use the data source instance to fetch data
data = alpha_vantage_ds.get_ticker_data("AAPL")
```

The available built-in data sources include:

* AlphaVantage
* EODHD
* NasdaqDataLink
* Tiingo
* YFinance

You can list all available data sources using:
```python
print(DataSourceFactory.data_sources)
```

### Custom Data Sources

To extend the functionality with your own data sources, you can create custom data source classes and register them with the `DataSourceFactory`. Custom data source classes should subclass `BaseDataSource` and implement the required methods.

#### Creating a Custom Data Source

1. **Subclass `BaseDataSource`**: Your custom data source class should inherit from `BaseDataSource`.

2. **Implement Required Methods**: At a minimum, your class should implement the `get_ticker_data` method.

#### Example:

```python
from fin_ds.data_sources.base_data_source import BaseDataSource
import pandas as pd

class MyCustomDataSource(BaseDataSource):
    def get_ticker_data(self, ticker, interval="daily"):
        # Custom logic to fetch data
        # For demonstration, return an empty DataFrame
        return pd.DataFrame()

# Register the custom data source with the factory
from fin_ds import DataSourceFactory
DataSourceFactory.register_data_source(MyCustomDataSource)
```

#### Using Your Custom Data Source

Once registered, you can instantiate your custom data source using the `DataSourceFactory` just like built-in sources:

```python
# Create an instance of your custom data source
my_custom_ds = DataSourceFactory("MyCustomDataSource")

# Use it to fetch data
data = my_custom_ds.get_ticker_data("AAPL")
```

### Tips for Custom Data Sources

- **Naming**: The name used to instantiate the data source via `DataSourceFactory` is derived from the class name, omitting "DataSource" suffix if present. Ensure your class names are descriptive and unique.
- **API Keys**: If your data source requires an API key, make sure to include logic in your class to handle this securely. You might use environment variables or configuration files to manage API keys outside your codebase.
- **Error Handling**: Implement robust error handling within your custom data source methods to deal with API limitations, network issues, or data inconsistencies.

By following these guidelines, you can seamlessly integrate custom data sources into your application, enhancing its data retrieval capabilities.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Troubleshooting

Encountering issues is a normal part of working with any software package. This section provides guidance on resolving common problems you may face while using this package.

### Data Source Not Found

If you encounter an error indicating that a data source could not be found, consider the following steps:

- **Check the Data Source Name**: Ensure that the name you're using to instantiate the data source matches one of the available data sources. Remember, the name is case-sensitive.
  
- **List Available Data Sources**: Use `DataSourceFactory.data_sources` to list all registered data sources to verify if your desired data source is available.
  
- **Custom Data Source Registration**: If you're trying to use a custom data source, ensure it has been registered correctly with `DataSourceFactory.register_data_source()` before attempting to use it.

### ImportError or ModuleNotFoundError

These errors can occur when the package tries to dynamically load a data source module but fails. Possible reasons include:

- **Incorrect Directory Structure**: Verify that your custom data source files are placed in the correct directory if they follow the built-in data source convention.
  
- **Incorrect Module Name**: Ensure that the module file name matches the expected naming convention (`lowercase` version of the data source class name).
  
- **Environment Issues**: If you're using a virtual environment, ensure it's activated, and the package is installed within it.

### API Key Errors

If your data source requires an API key and you encounter authentication or access errors:

- **Verify API Key**: Check that the API key is correct and has the necessary permissions.
  
- **Configuration Check**: Ensure that the API key is properly configured, either through environment variables or configuration files as expected by your data source class.

### Data Fetching Errors

Problems fetching data can arise due to various reasons:

- **Network Issues**: Verify your internet connection.
  
- **API Limitations**: Some APIs have call rate limits. Ensure you're not exceeding these limits.
  
- **Incorrect Parameters**: Verify that the parameters passed to the data fetching methods (e.g., ticker symbols) are correct and supported by the data source.

### Debugging Tips

- **Logging**: Increase the logging level to `DEBUG` to get more detailed output that might help identify the issue.
  
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```
  
- **Interactive Python Shell**: Experiment with your data sources in an interactive Python shell (e.g., `ipython` or `python` REPL) for quicker feedback and easier troubleshooting.

### Seeking Further Assistance

If you've gone through these steps and still face issues, consider seeking further assistance by:
- **Checking the Documentation**: Review the package documentation for any additional troubleshooting tips or known issues.
- **GitHub Issues**: If you suspect a bug or have a feature request, use the GitHub Issues page for the project to search for existing issues or create a new one.
  



<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Release history

For a more detailed changelog, including the list of all changes for each version, please refer to the [Releases](https://github.com/mattsmith321/fin-ds/releases) page on GitHub.

* 0.3.0 - Added Nasdaq data sources using [nasdaq-data-link](https://pypi.org/project/Nasdaq-Data-Link/) package.
* 0.3.1 - Fixed how tickers with special characters are handled (at least for BRK-A).
* 1.0.0 - Made changes to class and module names to support dynamic loading.
* 1.1.0 - Added dynamic registration of custom data source classes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### 5. Include Contribution Guidelines

```markdown
## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

Please ensure your code adheres to the [Black](https://github.com/psf/black) code style, and include unit tests for new features or fixes. For more details, check out our CONTRIBUTING.md file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


