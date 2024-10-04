import logging

from fin_ds.data_source_factory import DataSourceFactory

# Configure the basic logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def default():
    """Basic example using YFinance"""
    print("Default data source (YFinance):")
    df = DataSourceFactory().get_eod_data("AAPL")
    print(df)


def main():
    print("Choose an example to run:")
    print("1: Default example")

    choice = input("Enter the example number: ")

    if choice == "1":
        default()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
