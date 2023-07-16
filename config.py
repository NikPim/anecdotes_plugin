import configparser

def read_config() -> configparser.ConfigParser:
    """
    Reads data from configuration.ini (API token, etc.)
    """
    config = configparser.ConfigParser()
    config.read("configuration.ini")

    return config
