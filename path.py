import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path


# We will first generated a path in the graph space using the start and goal position
#
# Since we are in a graph space, the easiest path will be a straight line from the start to the goal
#
# This is a simple path generator but is not dynamic
# below you will find a more dynamic path generator
def path_generator(start, finish):
    codes = [Path.MOVETO, Path.LINETO]
    verts = [start, finish]

    path = Path(verts, codes)

    return path


def dynamic_path_generator(start, finish, ax, obstacles, bounds):
    steps = 100
    lookahead = 5
    x_values = np.linspace(start[0], finish[0], steps)
    y_values = np.linspace(start[1], finish[1], steps)

    # Extract upper and lower bounds
    upper, lower = extract_limits(bounds)
    points_on_upper_bound = generate_point_on_path(upper[0], upper[1], steps)
    points_on_lower_bound = generate_point_on_path(lower[0], lower[1], steps)

    for i, (x, y) in enumerate(zip(x_values, y_values)):
        collision = False

        # implement a lookahead to detect collisions
        #
        # TODO: look into how to make the lookahead dynamic
        for j in range(i, min(i + lookahead, steps)):
            collision, index = detect_obstacle_collision(
                x_values[j], y_values[j], obstacles
            )
            if collision:
                break
        # If a collision is detected, adjust position to avoid the obstacle
        if collision:
            # Get the corresponding points on upper and lower bounds
            upper_x, upper_y = points_on_upper_bound[i]
            lower_x, lower_y = points_on_lower_bound[i]
            x, y = deter_obstacle_collision(
                x, y, upper_x, upper_y, lower_x, lower_y, obstacles, index
            )
        ax.plot(x, y, "bo", markersize=2)
        plt.pause(0.01)


def draw_bounds(ax, coords: slice):
    # draw the bounds
    upper, lower = extract_limits(coords)

    upper_limit_path = path_generator(upper[0], upper[1])
    lower_limit_path = path_generator(lower[0], lower[1])

    upper_patch = patches.PathPatch(
        upper_limit_path, facecolor="none", edgecolor="black", lw=1, linestyle="--"
    )
    lower_patch = patches.PathPatch(
        lower_limit_path, facecolor="none", edgecolor="black", lw=1, linestyle="--"
    )
    ax.add_patch(upper_patch)
    ax.add_patch(lower_patch)


# how it works is that we know that the ideal path of the bot is a straight line
# between the start and finish points, hence we will generate upper and lower limits
# for the obstacles based on the start and finish points
#
# this will simulate a real world scenario where obstacles are usually unpredictable
def generate_bounds(start, finish, delta):
    # depending on the delta we will take the start coordinates and add the delta to them
    # to get the upper and lower bounds of the obstacles
    start_upper_bounds = (start[0] + delta, start[1] + delta)
    start_lower_bounds = (start[0] - delta, start[1] - delta)

    finish_upper_bounds = (finish[0] + delta, finish[1] + delta)
    finish_lower_bounds = (finish[0] - delta, finish[1] - delta)

    # Calculate overall upper and lower bounds for obstacle generation
    upper_bounds = [start_upper_bounds, finish_upper_bounds]
    lower_bounds = [start_lower_bounds, finish_lower_bounds]

    return [upper_bounds, lower_bounds]


def extract_limits(coords: slice):
    upper_limit = coords[0]
    lower_limit = coords[1]

    upper_start = (lower_limit[0][0], upper_limit[0][1])
    upper_finish = (lower_limit[1][0], upper_limit[1][1])

    lower_start = (upper_limit[0][0], lower_limit[0][1])
    lower_finish = (upper_limit[1][0], lower_limit[1][1])

    return (upper_start, upper_finish), (lower_start, lower_finish)


def generate_point_on_path(start, finish, steps):
    x_values = np.linspace(start[0], finish[0], steps)
    y_values = np.linspace(start[1], finish[1], steps)

    # reduce precision to 2 decimal places
    x_values = np.around(x_values, decimals=2)
    y_values = np.around(y_values, decimals=2)
    return [(x, y) for x, y in zip(x_values, y_values)]


def detect_obstacle_collision(x, y, obstacles):
    for i, obs in enumerate(obstacles):
        # add a slight offset to avoid absolute collisions. This can be described as a safety distance
        delta = 1.5
        # Get the bottom-left corner, width, and height of the obstacle
        obs_x, obs_y = obs.get_xy()
        obs_width = obs.get_width()
        obs_height = obs.get_height()

        # Check if the point (x, y) lies within the bounds of the rectangle
        #
        # This ensures that the area of the obstacle appears on the path
        if (obs_x <= x <= obs_x + (obs_width * delta)) and (
            obs_y <= y <= obs_y + (obs_height * delta)
        ):
            return True, i
    return False, i


def detect_obstacle_collision_noIndex(x, y, obstacles):
    for obs in obstacles:
        # add a slight offset to avoid absolute collisions. This can be described as a safety distance
        delta = 1.5
        # Get the bottom-left corner, width, and height of the obstacle
        obs_x, obs_y = obs.get_xy()
        obs_width = obs.get_width() * delta
        obs_height = obs.get_height() * delta

        # Check if the point (x, y) lies within the bounds of the rectangle
        #
        # This ensures that the area of the obstacle appears on the path
        if (obs_x <= x <= obs_x + obs_width) and (obs_y <= y <= obs_y + obs_height):
            return True
    return False


def deter_obstacle_collision(
    x, y, upper_x, upper_y, lower_x, lower_y, obstacles, index
):
    # calculate the distance of the obstacles from the bound and not the path
    # because the path is a straight line
    # get the index of the obstacle
    obs = obstacles[index]
    obs_x, obs_y = obs.get_xy()

    dist_to_upper = np.hypot(upper_x - obs_x, upper_y - obs_y)
    dist_to_lower = np.hypot(lower_x - obs_x, lower_y - obs_y)
    if dist_to_upper > dist_to_lower:
        # Offset towards the upper bound direction
        offset_x = upper_x - x
        offset_y = upper_y - y
    else:
        # Offset towards the lower bound direction
        offset_x = lower_x - x
        offset_y = lower_y - y

    # Apply a small step in the chosen direction
    step_size = 0.1
    x += step_size * np.sign(offset_x)
    y += step_size * np.sign(offset_y)

    # Re-check for collisions at the new position
    while detect_obstacle_collision_noIndex(x, y, obstacles):
        # Increase the step size or move in the direction of the offset
        x += step_size * np.sign(offset_x)
        y += step_size * np.sign(offset_y)
    return x, y
