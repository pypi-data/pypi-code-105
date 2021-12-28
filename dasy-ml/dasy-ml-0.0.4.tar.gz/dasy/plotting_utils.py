import matplotlib.pyplot as plt

def plot_bisectors(a, b, ax=plt):
    midpoint = (a + b) / 2
    slope = - (b[0] - a[0]) / (b[1] - a[1])
    #plt.plot([midpoint[0], midpoint[0] + 1], [midpoint[1], midpoint[1] + slope], '-')
    ax.axline((midpoint[0], midpoint[1]), slope=slope, linestyle='--')
