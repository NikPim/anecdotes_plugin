# -*- coding: utf-8 -*-
import json


def save_data_to_json(data, filename):
    """
    Saves data to a local JSON file with provided filename

    Args:
        data (Any): Data to be saved as JSON.
        filename (str): Name of the output JSON file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
