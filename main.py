import matplotlib.pyplot as plt

from obs import generate_obstacles
from path import draw_bounds, dynamic_path_generator, generate_bounds
from plot import dynamic_plot_generator

# Robot starting position
start = (10, 10)

# finish
goal = (90, 90)

# limits of the plot
bounds = [(0, 100), (0, 100)]

# obstacles
obstacles = [(30, 30), (50, 50), (70, 20), (80, 80)]


def main():
    # Generate the path
    fig, ax = dynamic_plot_generator(bounds)
    obstacle_bounds = generate_bounds(start, goal, 10)

    draw_bounds(ax, obstacle_bounds)
    obstacles = generate_obstacles(start, goal)
    for obstacle in obstacles:
        ax.add_patch(obstacle)

    dynamic_path_generator(start, goal, ax, obstacles, obstacle_bounds)
    plt.show()


main()
