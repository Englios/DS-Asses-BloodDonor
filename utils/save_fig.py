import os
import matplotlib.pyplot as plt

def save_fig(fname: str):
    try:
        plt.savefig(fname)
    except:
        os.remove(fname)
    else:
        plt.savefig(fname)
    finally:
        plt.close()
