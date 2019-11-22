from CLASS import *

if __name__ == '__main__':
    SQLData = [
        {'ID': 1, 'name': '1', 'LT': 1, 'pre': []},
        {'ID': 2, 'name': '2', 'LT': 2, 'pre': [1]},
        {'ID': 3, 'name': '3', 'LT': 3, 'pre': [5]},
        {'ID': 4, 'name': '4', 'LT': 4, 'pre': [8]},
        {'ID': 5, 'name': '5', 'LT': 5, 'pre': [2]},
        {'ID': 6, 'name': '6', 'LT': 6, 'pre': [1]},
        {'ID': 7, 'name': '7', 'LT': 7, 'pre': [3, 4]},
        {'ID': 8, 'name': '8', 'LT': 8, 'pre': [6, 2, 5]},
        {'ID': 9, 'name': '9', 'LT': 9, 'pre': [7]},
        {'ID': 10, 'name': '10', 'LT': 10, 'pre': [7]},
    ]
    g = Graph()
    g.readDataFromSQL(SQLData)
    g.info()
    print(g.topologicalSorting())
