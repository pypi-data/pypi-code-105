import matplotlib.pyplot as plt
from dasy.synthesizers.uniform import UniformSynth
from dasy.labelers.regression.linear import LinearRegressionLabeler

def main():
    dim = 1
    n = 50
    synth = UniformSynth()
    labeler = LinearRegressionLabeler(dim=dim)
    X = synth.sample(n=n, dim=dim)
    y = labeler.assign(X)

    plt.scatter(X, y)
    plt.show()

if __name__ == '__main__':
    main()


