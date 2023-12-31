# -*- coding: utf-8 -*-
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any


class FileSaver(ABC):
    @abstractmethod
    def save(self, data: list[Dict[str, Any]], filename: str) -> None:
        pass


class JsonFileSaver(FileSaver):
    """
    Used for saving data in JSON format
    """

    def save(self, data: list[Dict[str, Any]], filename: str) -> None:
        """
        Saves data to a local JSON file with provided filename

        Args:
            data (Any): Data to be saved as JSON.
            filename (str): Name of the output JSON file.
        """
        # Get the path to the data directory inside the current directory
        data_dir = os.path.join(os.getcwd(), "data")

        # Create the data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Construct the full path to the data file
        file_path = os.path.join(data_dir, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    class CsvFileSaver(FileSaver):
        """
        Used for saving data in CSV format
        """
