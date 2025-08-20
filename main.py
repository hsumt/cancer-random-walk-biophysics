import numpy as np
import matplotlib.pyplot as plt
import random
import config


def move_walker(x,y,z):
    directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    weights = [1,1,1,1,1+config.oxygen_bias, 1-config.oxygen_bias]
    weights = np.array(weights) / np.sum(weights)
    dx, dy, dz = directions[np.random.choice(len(directions), p=weights)]
    nx, ny, nz = x+dx, y+dy, z+dz


    if (0 <= nx <= config.grid_size) and (0 <= ny <= config.grid_size) and (0 <= nz <= config.grid_size):
        return nx, ny, nz
    else:
        return x, y, z


def simulate(grid_size, oxygen_bias, nw_bias, num_steps, max_Walkers):
    grid = np.zeros(((grid_size), (grid_size), (grid_size)))
    positions, walker_counts, cancer_cell_counts = [], [], []
    walkers = [((grid_size//2),(grid_size//2),(grid_size//2))]
    grid[((grid_size//2),(grid_size//2),(grid_size//2))] = 1
    oxygen = np.linspace(0,1,grid_size)

    
    for step in range(num_steps): #Cycle checker per walker over steps.
        new_walkers = []
        for i in range(len(walkers)):
            x,y,z = walkers[i]
    
            death_prob = 1 - oxygen[z]
            if random.random() < death_prob * 0.05:
                continue
    
            nx,ny,nz = move_walker(x,y,z)
            if grid[nx,ny,nz] == 0:
                grid[nx, ny, nz] = 1
                walkers[i] = (nx,ny,nz)
                positions.append((nx,ny,nz))
            else:
                continue
    
        if random.random() < 0.02 and positions:
            popped = positions.pop()
            grid[popped[0], popped[1], popped[2]] = 0
        if (len(new_walkers) + len(walkers) <= config.max_walkers) and (random.random() < nw_bias):
            new_walkers.append((nx, ny, nz))
    
        walkers.extend(new_walkers)
        walker_counts.append(len(walkers))
        cancer_cell_counts.append(len(positions))
    return positions, walker_counts, cancer_cell_counts, grid

def plot_results(positions, walker_counts, cancer_cell_counts, grid):
    # --------- GRAPHING & DISPLAY -----------
    x_steps, y_steps, z_steps = zip(*positions)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_steps, y_steps, z_steps, c = 'red', marker='o')
    
    # 3D scatter
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_steps, y_steps, z_steps, c='red', marker='o')
    ax.set_title("3D Biased Cancer Cell Random Walk")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()
    fig.savefig("graph.png", dpi=300)
    plt.show()

    # Walker Counts
    fig2 = plt.figure()
    plt.plot(walker_counts, color='blue')
    plt.title("Walker Counts over Time")
    plt.xlabel("Step")
    plt.ylabel("Walker Counts")
    plt.grid(True)
    fig2.savefig("walkercount.png", dpi=300)
    plt.show()

    # Cancer Cell Counts
    fig3 = plt.figure()
    plt.plot(cancer_cell_counts, color='orange')
    plt.title("Total Cancer Cells Over Time")
    plt.xlabel("Step")
    plt.ylabel("Total Cancer Cells")
    plt.grid(True)
    fig3.savefig("cellcount.png", dpi=300)
    plt.show()

    # Z-axis distribution
    occupied = np.argwhere(grid == 1)
    z_vals = occupied[:,2]
    fig4 = plt.figure()
    plt.hist(z_vals, bins=20, color='green', edgecolor='black')
    plt.title("Cell Distribution Along Oxygen Gradient (Z-axis)")
    plt.xlabel("Z Position")
    plt.ylabel("Cell Count")
    plt.grid(True)
    fig4.savefig("distribution.png", dpi=300)
    plt.show()
    
def main():
    positions, walker_counts, cancer_cell_counts, grid = simulate(config.grid_size, config.oxygen_bias, config.nw_bias, config.num_steps, config.max_walkers)
    plot_results(positions, walker_counts, cancer_cell_counts, grid)
if __name__ == "__main__":
    main()
