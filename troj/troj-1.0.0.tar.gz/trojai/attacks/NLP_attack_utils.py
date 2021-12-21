from textattack.attack_recipes import BAEGarg2019, DeepWordBugGao2018, CheckList2020, CLARE2020, GeneticAlgorithmAlzantot2018
from textattack.attack_recipes import FasterGeneticAlgorithmJia2019, Kuleshov2017, PSOZang2020, PWWSRen2019
from trojai.attacks.TrojNLPAttacks import QWERTYAttack, ContractionAttack, DeletionAttack, InsertionAttack, SwapAttack
from trojai.attacks.TrojNLPAttacks import SynonymAttack, PronounAttack

textattack_dict = {'BAE': BAEGarg2019, 'DeepWordBug': DeepWordBugGao2018, 'Checklist': CheckList2020, 'CLARE': CLARE2020,
            'GeneticAlgorithm': GeneticAlgorithmAlzantot2018, 'FasterGeneticAlgorithm': FasterGeneticAlgorithmJia2019,
            'Kuleshov2017': Kuleshov2017, 'ParticleSwarm': PSOZang2020, 'PWWS': PWWSRen2019}

trojattack_dict = {'QWERTYAttack':QWERTYAttack, 'ContractionAttack':ContractionAttack, 'DeletionAttack':DeletionAttack,
                   'InsertionAttack':InsertionAttack, 'SwapAttack':SwapAttack, 'SynonymAttack':SynonymAttack, 'PronounAttack':PronounAttack}

att_dict = {**textattack_dict, **trojattack_dict}

#TODO add attack description dictionary as a lookup helper

def list_attacks():
    '''

    :return: A list containing the names of the different available attacks
    '''
    attack_list = list(att_dict.keys())
    return attack_list

def get_attack(attack_name):
    '''


    :param attack_name: The name of an attack in the attack dictionary (to get all names, call ``list_attacks()``).
    :return: The attack class.
    '''
    att = att_dict[attack_name]
    return att

def build_attack(attack, model):
    '''

    :param attack: An attack class (from ``get_attack``)
    :param model: A wrapped textattack model.
    :return:
    '''
    initialized_attack = attack.build(model)
    return initialized_attack

def parse_attack_list(attack_name_list, model):
    '''
    Builds the attack dictionary from the attack building dictionary.

    :param attack_build_list: A list containing the different attack names.
    :param model: A wrapped textattack model.
    :return: A dictionary where the keys are attack names and the values are initialized attacks.
    '''
    initialized_dict = {}
    for key in list(attack_name_list):
        assert key in att_dict, '{} is an invalid attack name'.format(key)
        uninit_att = get_attack(key)
        attack = build_attack(uninit_att, model)
        initialized_dict[key] = attack
    return initialized_dict