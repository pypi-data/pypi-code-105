
# %%
import logging
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.nlp.task.date_extractor import DateParser

from pyspace.rasa.components.data_management import TrainingDataManager

# %%
import copy
import pickle

from rasa.core.domain import Domain
from pathlib import Path

import random
import datetime

try:
    from pymongo import MongoClient
    pymongo_bool = True
except:
    pymongo_bool = False

class RegexPostProcessing(Component):

    defaults = {
        "db_name" : 'sofieIvr',
        "project_id" : 'bf',
    }

    def __init__(self, component_config: Dict[Text, Any] = None, response_dict=None) -> None:
        super(RegexPostProcessing, self).__init__(component_config)
        self.read_config()
        logging.warning(os.environ.get('MONGO_URL',''))

    def read_config(self,):
        mongo_url = os.environ.get('MONGO_URL','')
        if mongo_url == '':
            self.post_processing_config = []
        else:
            client = MongoClient(mongo_url)
            db = client[self.component_config['db_name']]
            projects_col = db.projects
            ## TODO regex_post_processing_config - read from config
            self.post_processing_config = projects_col.find_one({'_id':self.component_config['project_id']})['regex_post_processing_config']
            self.post_processing_config = sorted(self.post_processing_config, key=lambda x: x['priority'])
            client.close()

    def apply_post_processing(self, message):

        for c in self.post_processing_config:
            text = message.text
            if 'intent_read_attr' in c['input']:
                intent = message.get(c['input']['intent_read_attr'])
            else:
                intent = message.get(INTENT)
            intent_name = intent['name']
            intent_conf = intent['confidence']
            
            if 'entity_read_attr' in c['input']:
                entities = message.get(c['input']['entity_read_attr'])
            else:
                entities = message.get(ENTITIES,[])
            matched_entity = None

            intent_ranking = message.get("intent_ranking")
            second_conf = 0.0 if len(intent_ranking) < 2 else intent_ranking[1]['confidence']

            conditions = []

            if 'text' in c['input']:
                conditions.append( bool(re.findall(c['input']['text'], text)) )
            if 'intent' in c['input']:
                # conditions.append( intent_name == c['input']['intent'] )
                conditions.append( bool(re.findall(c['input']['intent'], intent_name)) )
            if 'entity_text' in c['input'] or 'entity' in c['input'] or 'role' in c['input']:
                
                for e in entities:
                    e_conditions = []
                    if 'entity_text' in c['input']:
                        e_conditions.append( bool(re.findall(c['input']['entity_text'], e['value'])) )
                    if 'entity' in c['input']:
                        # e_conditions.append( c['input']['entity'] == e['entity'] )
                        e_conditions.append( bool(re.findall(c['input']['entity'], e['entity'])) )
                    if 'role' in c['input']:
                        if 'role' in e:
                            e_conditions.append( c['input']['role'] == e['role'] )
                        else:
                            e_conditions.append(False)
                    if all(e_conditions):
                        conditions.append(True)
                        matched_entity = e
                        break
                if matched_entity is None:
                    conditions.append(False)

            if 'second_conf' in c['input']:
                conditions.append( second_conf > c['input']['second_conf'] )

            if all(conditions):
                if 'intent' in c['output']:
                    if 'intent_write_attr' in c['output']:
                        message.set(c['output']['intent_write_attr'], c['output']['intent'], add_to_output=True)
                    else:
                        message.set(INTENT, c['output']['intent'])
                if 'entity_mode' in c['output']:
                    if c['output']['entity_mode'] == 'update' and matched_entity is not None:
                        matched_entity['entity'] = c['output']['entity']
                    elif c['output']['entity_mode'] == 'overwrite':
                        if 'entity_write_attr' in c['output']:
                            message.set(c['output']['entity_write_attr'], c['output']['entities'], add_to_output=True)
                        else:
                            message.set(ENTITIES, c['output']['entities'])
                # break


    def process(self, message: Message, **kwargs: Any) -> None:
        ## TODO sofie_regex_post_processing_config_update - read from config
        if message.text[:41] == 'sofie_regex_post_processing_config_update':
            self.read_config()
        else:
            self.apply_post_processing(message)