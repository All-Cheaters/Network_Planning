"""
from CLASS import *

if __name__ == '__main__':
    SQLData = [
        {'ID': 1, 'name': 'A', 'LT': 5, 'pre': []},
        {'ID': 2, 'name': 'B', 'LT': 2, 'pre': [1]},
        {'ID': 3, 'name': 'C', 'LT': 8, 'pre': [1]},
        {'ID': 4, 'name': 'D', 'LT': 10, 'pre': [2, 3]},
        {'ID': 5, 'name': 'E', 'LT': 5, 'pre': [3]},
        {'ID': 6, 'name': 'F', 'LT': 10, 'pre': [4]},
        {'ID': 7, 'name': 'G', 'LT': 11, 'pre': [4, 5]},
        {'ID': 8, 'name': 'H', 'LT': 10, 'pre': [6, 7]},
    ]
    p = Project()
    p.readDataFromSQL(SQLData)
    p.graph.info()
"""
