import logging
import os
import re
from typing import Any, Dict, List, Optional, Text, Union, Type

import warnings
from rasa.nlu.utils import write_json_to_file

import numpy as np
import copy

from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
import rasa.utils.io
import rasa.utils.io
import scipy.sparse
from rasa.nlu import utils
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
)
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

from rasa.nlu.featurizers.sparse_featurizer.count_vectors_featurizer import CountVectorsFeaturizer

import pyspace
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

logger = logging.getLogger(__name__)

class CountVectorsFeaturizer20210826(CountVectorsFeaturizer):

    def train(self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any) -> None:

        super().train(training_data, config, **kwargs)

        for pname in self.component_config['additional_partition_name_list'] :
            for message in getattr(training_data, pname):
                super().process(message, **kwargs)