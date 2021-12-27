import sklearn.ensemble

from .bayes_code_generator import BayesCodeGenerator
from .mlp_code_generator import MlpCodeGenerator
from .random_forest_generator import RandomForestCodeGenerator
from .tree_code_generator import TreeCodeGenerator


class GeneratorFactory:

    recognized_classifiers = {
        sklearn.tree.DecisionTreeClassifier: TreeCodeGenerator,
        sklearn.naive_bayes.GaussianNB: BayesCodeGenerator,
        sklearn.neural_network.MLPClassifier: MlpCodeGenerator,
        sklearn.ensemble.RandomForestClassifier: RandomForestCodeGenerator
    }

    def get_generator(self, clf):
        if clf.__class__ in self.recognized_classifiers.keys():
            return self.recognized_classifiers[clf.__class__](clf)
        else:
            print("Sorry, but this is not recognized type of classifier")
            return None
