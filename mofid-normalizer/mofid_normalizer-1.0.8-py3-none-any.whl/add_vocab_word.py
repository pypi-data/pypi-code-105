from .data_helper import DataHelper
import pickle
import os


class VocabConfig:
    """
    You can add new words to the vocabulary in this file
    Parameters
    ----------
    add_list : list word will
    remove_list :

    """

    def __init__(self, add_list=[], remove_list=[]):
        self.data_helper = DataHelper()
        base_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.noun_lexicon = self.data_helper.load_var(
            base_dir + "resource/stemmer/stem_lex.pckl")  # 100,000 most freq words
        self.mini_noun_lex_path = self.data_helper.load_var(
            base_dir + "resource/stemmer/original_parsivar_stem_lex.pckl")  # parivar orginal words ~21,000
        self.remove_list = remove_list
        self.add_list = add_list

    def save_pickle(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/" + "resource/stemmer/stem_lex.pckl", 'wb') as f:
            pickle.dump(self.noun_lexicon, f)

        with open(
                os.path.dirname(os.path.realpath(__file__)) + "/" + "resource/stemmer/original_parsivar_stem_lex.pckl",
                'wb') as f:
            pickle.dump(self.mini_noun_lex_path, f)

    def remove_words(self):
        self.noun_lexicon.difference_update(self.remove_list)
        self.mini_noun_lex_path.difference_update(self.remove_list)

    def add_words(self):
        self.noun_lexicon.update(self.add_list)
        self.mini_noun_lex_path.update(self.add_list)

    def modifier(self):
        self.add_words()
        self.remove_words()
        self.save_pickle()

    def get_mini_vocab(self):
        return self.mini_noun_lex_path

    def get_big_vocab(self):
        return self.noun_lexicon
