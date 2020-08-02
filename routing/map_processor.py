# Project: Autonomous Service Robot - Charles
# Author: Hadiyah Ghoghari
# Acknowledgement: Help from Joseph, and Prashant Singh's article on
#                  GeeksforGeeks https://www.geeksforgeeks.org/shortest-distance-two-cells-matrix-grid/)
# All rights reserved.


# This file contains the code to read a layout of the environment in which the autonomous service robot will operate.
# Its get_shortest_path method calculates the shortest path between two locations on the map,
# with the help of the abstraction explained below.

# The layout of the environment is fed to the robot in the form of a binary matrix. Consider this example:
# data = [
#     [1, 0, 1, 0, 1],
#     [1, 1, 1, 0, 0],
#     [0, 1, 1, 0, 0],
#     [0, 1, 1, 1, 1],
#     [0, 1, 1, 0, 1]
# ]
# Every cell in the matrix represents a finite distance in the real world, such as feet or meters.
# '1' indicates that a specific 1ft x 1ft square is accessible by the robot.
# '0' indicates that a specific 1ft x 1ft square is not accessible by the robot.
# The collection of such cells represents the areas that the robot can move in, within its local environment.
# The example above resembles the top view of the following floor plan:
#   -----------------
#   |   |||   |||   |
#   |         |||||||
#   ||||      |||||||
#   ||||            |
#   ||||      |||   |
#   -----------------
# Empty spaces are areas that people can move in;
# Whereas marked areas represent walls or objects on the floor that prevent passage.

# UPDATE THE LAYOUT HERE
data = [
    # 0  1  2  3  4
    [1, 0, 1, 0, 1],  # 0
    [1, 1, 1, 0, 0],  # 1
    [0, 1, 1, 0, 0],  # 2
    [0, 1, 1, 1, 1],  # 3
    [0, 1, 1, 0, 1]   # 4
]


class Node:
    def __init__(self, row, column, distance_from_start=None, previous=None):
        self.row = row
        self.column = column
        if previous is None:
            self.previous = None
        else:
            self.previous = previous
        if distance_from_start is None:
            self.distance_from_start = 0
        else:
            self.distance_from_start = distance_from_start

    def __repr__(self):
        return f"({self.row}, {self.column})\n"

    def __eq__(self, other):
        try:
            return (self.row == other.row) and (self.column == other.column)
        except:
            return False


# SPECIFY THE COORDINATES OF LOCATIONS THAT YOU WANT TO BE ABLE TO MAKE DELIVERIES TO
where_is_everything = {
    "224": Node(2, 2),
    "225": Node(4, 2),
    "223": Node(1, 0)
}


def get_node_value(matrix, node_row, node_column):
    return matrix[node_row][node_column]


def get_shortest_path(matrix, start, end):
    # Prints the shortest path to travel between two cells of a matrix,
    # and calculates the distance for that path.
    # Parameters:
    #   matrix - a two-dimensional array containing 1 or 0.
    #   start - a start node with row and column values that are valid for the matrix
    #   end - the destination node with row and column values that are valid for the matrix
    # This method is based on the Breadth-first Search Algorithm. 

    MAX_COL = len(matrix[0])
    MIN_COL = 0
    MAX_ROW = len(matrix)
    MIN_ROW = 0
    INACCESSIBLE = 0
    # ACCESSIBLE = 1

    explored_nodes = [[False for x in range(MAX_COL)] for y in range(MAX_ROW)]
    r = 0
    c = 0
    while r < MAX_ROW:
        c = 0
        while c < MAX_COL:
            if(get_node_value(matrix, r, c)) == INACCESSIBLE:
                explored_nodes[r][c] = True
                # Note: invalid/inaccessible nodes also count as "explored" nodes,
                #       since they don't need to be added to the exploration path.
            c = c + 1
        r = r + 1

    # Now perform a breadth-first search on the nodes that need to be explored.
    # Update the distances of the nodes (from the 'start') during the exploration.
    current_path = [start]  # list to track the nodes seen along a path.
    explored_nodes[start.row][start.column] = True  # set the 'start' node to an explored state.
    while current_path:
        current_node = current_path[0]
        current_path.remove(current_node)

        if current_node == end:
            # reached the destinatio, now print the path.
            distance = current_node.distance_from_start

            # Using the 'previous' to print the path, so first need to reverse the order.
            # Get all the nodes that are in that path.
            node_order = []
            node_order.append(current_node)
            while current_node.previous is not None:  # None indicates that the 'start' node has been reached.
                node_order.append(current_node.previous)
                current_node = current_node.previous
            node_order.reverse()  # reverse the nodes to get the correct order beginning with the start node

            # now print the path in the correct order.
            list_length = len(node_order)
            i = 0
            while i < list_length:
                print(node_order[i])
                i = i + 1
            return distance

        # check if the neighbor above likes to be visited.
        if ((current_node.row-1) >= MIN_ROW) and (explored_nodes[current_node.row-1][current_node.column] is False):
            current_path.append(Node(current_node.row-1, current_node.column, current_node.distance_from_start+1, current_node))
            explored_nodes[current_node.row - 1][current_node.column] = True

        # check if the neighbor below likes to be visited.
        if ((current_node.row+1) < MAX_ROW) and (explored_nodes[current_node.row+1][current_node.column] is False):
            current_path.append(Node(current_node.row + 1, current_node.column, current_node.distance_from_start + 1, current_node))
            explored_nodes[current_node.row + 1][current_node.column] = True

        # check if the neighbor to the left likes to be visited.
        if ((current_node.column-1) >= MIN_COL) and (explored_nodes[current_node.row][current_node.column-1] is False):
            current_path.append(Node(current_node.row, current_node.column - 1, current_node.distance_from_start + 1, current_node))
            explored_nodes[current_node.row][current_node.column - 1] = True

        # check if the neighbor to the right likes to be visited.
        if ((current_node.column+1) < MAX_COL) and (explored_nodes[current_node.row][current_node.column+1] is False):
            current_path.append(Node(current_node.row, current_node.column + 1, current_node.distance_from_start + 1, current_node))
            explored_nodes[current_node.row][current_node.column + 1] = True

    return -1


def get_directions(start_row, start_column, dest_room):
    if dest_room not in where_is_everything:
        print('Invalid destination was chosen. Please try again.\n')
    else:
        get_shortest_path(data, Node(start_row, start_column), where_is_everything[dest_room])


if __name__ == '__main__':
    # get_directions(2, 1, "223")
    print("Debug mode: Getting directions from (0, 0) to Room 225.")
    final_path = get_shortest_path(data, Node(0, 0, 0), where_is_everything["225"])
    print(f"Shortest distance from start to end: {final_path}")
