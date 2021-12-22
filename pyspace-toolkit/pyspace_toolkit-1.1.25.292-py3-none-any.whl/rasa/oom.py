
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

import numpy as np


class OOM(Component):

    
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        ALLOCATIONS = []
        while True:
            ALLOCATIONS.append(np.ones((1024 * 1024 * 128)))