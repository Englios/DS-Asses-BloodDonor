import os
import matplotlib.pyplot as plt

IMAGE_DIR = './images'

def save_fig(fname: str):
    """
    Save the current figure to a file.

    Parameters:
    - fname (str): The filename to save the figure to.
    - dpi (int): The resolution of the saved figure in dots per inch. Default is 300.

    Returns:
    None
    """
    try:
        plt.savefig(os.path.join(IMAGE_DIR, fname))
    except:
        os.remove(os.path.join(IMAGE_DIR, fname))
    else:
        plt.savefig(os.path.join(IMAGE_DIR, fname))
    finally:
        plt.close()
