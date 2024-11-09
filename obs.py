import matplotlib.patches as patches
import numpy as np

from path import generate_point_on_path

# here we will generate dynamic bounds of obstacles based on the start and finish


def generate_obstacles(start, finish):
    obstacles = []

    # Define the dimensions of each obstacle (fixed size for simplicity)
    width, height = 5, 5
    num_of_obstacles = np.random.randint(4, 10)
    # random float between 0 and 1 to determine if the obstacle is on the left or right side of the path
    points = generate_point_on_path(start, finish, num_of_obstacles)
    for point in points[1:-1]:
        x, y = point
        # shift the x and y coordinates randomly but within the bounds
        x = random_float(x)
        y = random_float(y)
        # Create a rectangle at this position
        new_obstacle = patches.Rectangle(
            (x, y),
            width=width,
            height=height,
            facecolor="red",
            edgecolor="black",
            alpha=0.5,
        )
        # add the obstacle to the list
        obstacles.append(new_obstacle)

    # remove the first and last obstacles as they appear from the origin
    return obstacles


def random_float(coord, max_shift=1.5):
    seed = np.random.randint(0, 8)
    # Generate a random float
    rand = np.random.random_sample() * max_shift
    # Randomly choose to add or subtract the float
    sign = np.random.choice([-1, 1])

    # Apply the random float with the chosen sign
    return coord + (sign * (rand * seed))
