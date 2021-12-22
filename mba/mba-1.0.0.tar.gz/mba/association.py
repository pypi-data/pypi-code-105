from mlxtend.frequent_patterns import apriori, association_rules

from mba.config.core import config
from mba.processing.association_features import Feature

class AssociationRule(object):
    def __init__(self):
        pass

    def get_frequent_items(self, min_support):
        apriori_model_colnames = apriori(
            online_encoder_df,
            min_support=min_support,
            use_colnames=True,
            low_memory=True,
        )
        return apriori_model_colnames

    def get_rules(self, min_support=0.01, metric="lift", min_threshold=1, recalculate=False):
        global online_encoder_df
        online_encoder_df = Feature()._prepare_data(recalculate)
        f = self.get_frequent_items(min_support)
        rules = association_rules(
            f,
            metric=metric,
            min_threshold=min_threshold,
            support_only=False
        )
        return rules.sort_values(metric,  ascending=False)
