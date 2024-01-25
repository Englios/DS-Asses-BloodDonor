import os
import matplotlib.pyplot as plt

IMAGE_DIR = './images'

def save_fig(fname: str):
    try:
        plt.savefig(os.path.join(IMAGE_DIR,fname))
    except:
        os.remove(os.path.join(IMAGE_DIR,fname))
    else:
        plt.savefig(os.path.join(IMAGE_DIR,fname))
    finally:
        plt.close()
