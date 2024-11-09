import matplotlib.patches as patches
import matplotlib.pyplot as plt


def generate_plot(path, bounds: slice):
    fig, ax = plt.subplots()

    patch = patches.PathPatch(path, facecolor="none", lw=2)
    ax.add_patch(patch)
    ax.set_title("Straight Line Path")
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.grid(True)
    plt.show()


def dynamic_plot_generator(bounds: slice):
    fig, ax = plt.subplots()
    ax.set_title("Dynamic Path Generator")
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.grid(True)
    return fig, ax
