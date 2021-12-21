from trojai.attacks.TrojNLPTransformations import TrojWordSwapQWERTY, PronounSwap
from textattack.goal_functions import UntargetedClassification
from textattack.search_methods import GreedySearch
from textattack.constraints.pre_transformation import *
from textattack.transformations.word_swaps import *
from textattack import Attack

class QWERTYAttack:
    '''
    Performs an attack which simulates typos which occur when typing too fast.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), MaxModificationRate(0.2), RepeatModification()]
        search_method = GreedySearch()
        transformation = TrojWordSwapQWERTY()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack


class ContractionAttack:
    '''
    Performs an attack which swaps words with their contractions. i.e they're -> they are

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), RepeatModification()]
        search_method = GreedySearch()
        transformation = WordSwapContract()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack

class DeletionAttack:
    '''
    Performs an attack which deletes characters in words.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), MaxModificationRate(0.15), RepeatModification()]
        search_method = GreedySearch()
        transformation = WordSwapRandomCharacterDeletion()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack

class InsertionAttack:
    '''
    Performs an attack which inserts new characters into words.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), MaxModificationRate(0.15), RepeatModification()]
        search_method = GreedySearch()
        transformation = WordSwapRandomCharacterInsertion()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack

class SwapAttack:
    '''
    Performs an attack which randomly swaps characters in words.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), MaxModificationRate(0.15), RepeatModification()]
        search_method = GreedySearch()
        transformation = WordSwapRandomCharacterSubstitution()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack


class SynonymAttack:
    '''
    Performs a synonym replacement attack.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MinWordLength(2), MaxModificationRate(0.2), RepeatModification()]
        search_method = GreedySearch()
        transformation = WordSwapWordNet()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack

class PronounAttack:
    '''
    Performs an attack which swaps masculine for feminine pronouns and vice-versa.

    '''
    @staticmethod
    def build(model):
        attack_constraints = [MaxModificationRate(0.2), RepeatModification()]
        search_method = GreedySearch()
        transformation = PronounSwap()
        goal_function = UntargetedClassification(model)
        attack = Attack(goal_function, attack_constraints, transformation, search_method)
        return attack