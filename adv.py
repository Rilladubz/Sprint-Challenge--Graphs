from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

    def peek(self):
        return self.stack[-1]


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

## UPER ###

# create traversal function

# needed items:

# traversal path list
# a hashtable of opposite directions
# a visited graphs

# create a stack & push the players current room on to the Stack
# enter a while loop, while the stack is not empty.
# create a peek function on stack class to allow to view last item
# reference the last item on the stack DO NOT REMOVE THE LAST Item
# use the item in position 0 of the stack as the current room of the player
# use the next item in the stack as the players series of moves
# check to see if the current room exists in the visited graph
# if it doesn't then add it to the visited graph using the id for key and initialize it with an empty set
# the set will represent the paths of the current room which were already taken
# if there is a next item (meaning the player moved) in the stack use the players current room to reference the current room the player is in
# and add that path to the set to represent paths taken from that room.
# if the length of visited graph is the length of room_graph then terminate the while loop and return traversal_path
# create an unexplored paths list that contains all exits not explored by the player...
# choose a random path and let the player do a dft add that path to the visited graph every time the player moves
# add the path and the inverse path to the stack.
# if the player gets stuck then find a way to make the player back up until he's in a room with unvisited paths and continue

## PSUEDO ##


# def traversal():
#     trav_pth = []
#     opp_directions = {key == your current direction needed to be reverse: the reversed value}
#     visited = {}

#     a = stack
#     player push current room to Stack

#     while stack isn't empty:
#         peek value = item in Stack
#         cur_room = a[0]
#         players_move = a[1]

#         if visited[cur room id] not in visited:
#             add it with empty set

#         if player moves:
#             visited_rooms[curr room id] = players_move

#         if the length of visited matches room_graph:
#             break

#         Do a Depth First traversal
#         until player is stuck
#         back up when player is stuck
#         & loop


### TRAVERSAL CODE ###

def traverse():
    # needed to back track path
    opp_directions = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }
    # Item to return
    traversal_path = []

    # Use visited hashtable to cache a room id as a key. Use a set to add directions which were visited.
    # room0.id = (paths visited... already visited paths)
    visited = {}

    my_stack = Stack()
    my_stack.push(value=(player.current_room, None))

    while my_stack.size != 0:
        # peek references the item on the top of the stack
        stack = my_stack.peek()
        # current room will be the first item in stack
        current_room = stack[0]

        # the next item in stack can represent a direction
        # travelled from current room
        travelled_dir = stack[1]

        # if the room isn't in the visited list add it.
        if current_room.id not in visited:
            visited[current_room.id] = set()

        # if player travelled in any direction, log the room
        # which the player travelled from (key) and the direction travelled.
        if travelled_dir:
            visited[current_room.id].add(travelled_dir)

        # if all rooms are visited then you're finished
        if len(visited) == len(room_graph):
            break

        ## DEPTH FIRST SEARCH ##

        # get all unexplored edges -- going to be list comp
        unexplored_path = [edge for edge in current_room.get_exits()
                           if edge not in visited[current_room.id]]

        # if there are remaining paths in players current room enter this scope:
        if unexplored_path:
            # choose a random path
            random_path = random.choice(unexplored_path)
            # add the random path to the current rooms visited paths before traversing down the path
            visited[current_room.id].add(random_path)
            # add the path to the stack so it could be traversed
            # also add the inverse direction to the stack will be used as travelled_dir
            # this will allow the player to back track if stuck
            my_stack.push(value=(current_room.get_room_in_direction(
                random_path), opp_directions[random_path]))
            # append traversal path with all of the travelled directions
            traversal_path.append(random_path)

        # else if the player is stuck because there are no remaining paths enter this scope:
        else:
            # back up and log that move in traversal_path
            traversal_path.append(travelled_dir)
            # pop the last item out of the stack this will remove travelled_dir
            # leaving it empty so on the next move it will be added again
            my_stack.pop()

    return traversal_path


traversal_path = traverse()

# TRAVERSAL TEST - DO NOT MODIFY


visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
