import logging
from typing import Any, Callable, List

import numpy as np
from _pta_python_binaries import SamplerSettings

from .commons import fill_common_sampling_settings, split_R

logger = logging.getLogger(__name__)


def estimate_proposal_distribution(
    sampler_function: Callable[[SamplerSettings, np.array], np.ndarray],
    get_chains_function: Callable[[Any], np.array],
    settings: SamplerSettings,
    num_samples: int,
    dimensionality: int,
    iteration_steps: List[int],
    gain: float = 1.0,
) -> np.ndarray:

    logger.info("Estimating proposal distribution ...")
    direction_weights = np.ones(dimensionality)

    for steps in iteration_steps:
        # Adjust the number of steps for the current iteration.
        fill_common_sampling_settings(
            settings,
            "",
            num_samples,
            steps,
            settings.num_chains,
            log_interval=settings.log_interval,
        )

        # Run the sampler.
        chains = get_chains_function(
            sampler_function(settings, np.diag(direction_weights))
        )

        # Compute convergence statistics.
        psrf = split_R(chains)

        # Update the weights.
        weights_multiplier = psrf
        weights_multiplier[weights_multiplier < 1.0] = 1.0
        weights_multiplier = weights_multiplier ** 2 - 1
        weights_multiplier = weights_multiplier / np.amax(weights_multiplier) * gain + 1
        direction_weights = direction_weights * weights_multiplier

        logger.info(
            f"> Iteration completed. Coefficients rage: "
            f"{np.amin(direction_weights):.2f} - {np.amax(direction_weights):.2f}"
        )

    logger.info("Estimation completed.")
    return np.diag(direction_weights)
