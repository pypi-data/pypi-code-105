from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from classification_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    validated_data = input_data.copy()
    new_vars_with_na = [
        var for var in validated_data if validated_data[var].isnull().sum() > 0
    ]

    validated_data.dropna(subset=[new_vars_with_na])

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        MultipleBettingDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class BettingDataInputSchema(BaseModel):
    q1_first: Optional[bool]
    q1_second: Optional[bool]
    q2_first: Optional[bool]
    q2_second: Optional[bool]
    q3_first: Optional[bool]
    q3_second: Optional[bool]
    p1_plays: Optional[bool]
    p2_plays: Optional[bool]
    p3_plays: Optional[bool]
    q1_diff: Optional[int]
    q2_diff: Optional[int]
    q3_diff: Optional[int]
    max_score_diff_pos: Optional[int]
    max_score_diff_neg: Optional[int]
    underdog_odds: Optional[float]
    avg_score_diff: Optional[float]
    pct_3p: Optional[float]
    pct_fg: Optional[float]
    pct_3p_reg: Optional[float]
    pct_fg_reg: Optional[float]


class MultipleBettingDataInputs(BaseModel):
    inputs: List[BettingDataInputSchema]
