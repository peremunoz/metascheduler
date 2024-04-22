"""
Reads a csv file and returns a list of strings with the content of the file.

"""
from typing import List


def read_csv(file_path: str) -> List[str]:
    """
    Read the csv file and return its values
    """
    with open(file_path, 'r') as file:
        return file.read().split(',')
