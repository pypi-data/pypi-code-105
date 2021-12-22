import matplotlib.pyplot as plt

def plot_the_best_plot():
    print("Printing the best plot")
    
    plt.hist([1, 1, 1, 2, 2, 3] * 5)
    plt.show()
    
    print("The best plot was printed")
