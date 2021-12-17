"""
The core of this module takes as input a collection of points, and generates
the associated diffusion map and diffusion Markov chain, with the aim of
producing features that are characteristic of the input geometry.

Taken as a whole the diffusion analysis pipeline provides statistical test
results and figures that assess the efficacy of diffusion-related metrics as
discriminators of selected correlates.
"""

from ...environment.workflow_modules import WorkflowModules
from ...dataset_designs.multiplexed_imaging.halo_cell_metadata_design import HALOCellMetadataDesign
from .job_generator import DiffusionJobGenerator
from .analyzer import DiffusionAnalyzer
from .computational_design import DiffusionDesign
from .integrator import DiffusionAnalysisIntegrator

components =  {
    'Multiplexed IF diffusion' : WorkflowModules(
        generator = DiffusionJobGenerator,
        dataset_design = HALOCellMetadataDesign,
        computational_design = DiffusionDesign,
        analyzer = DiffusionAnalyzer,
        integrator = DiffusionAnalysisIntegrator,
    ),
}
