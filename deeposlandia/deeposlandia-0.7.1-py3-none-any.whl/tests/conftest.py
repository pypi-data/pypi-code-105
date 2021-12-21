"""Test config setup for training dataset handling
"""

import json
import math
import os

import pytest
from tensorflow.keras import backend as K


@pytest.fixture(autouse=True)
def clear_session_after_test():
    """Test wrapper to clean up after TensorFlow and CNTK tests.
    This wrapper runs for all the tests in the keras test suite.
    """
    yield
    if K.backend() == "tensorflow" or K.backend() == "cntk":
        K.clear_session()


@pytest.fixture
def nb_channels():
    return 3


@pytest.fixture
def kernel_size():
    return 3


@pytest.fixture
def conv_depth():
    return 8


@pytest.fixture
def conv_strides():
    return 2


@pytest.fixture
def pool_strides():
    return 2


@pytest.fixture
def pool_size():
    return 2


@pytest.fixture
def mapillary_image_size():
    return 224


@pytest.fixture
def mapillary_input_config():
    return "tests/data/mapillary/config_aggregate.json"


@pytest.fixture
def mapillary_sample_config():
    return "tests/data/mapillary/training.json"


@pytest.fixture
def mapillary_raw_sample():
    """Sample of Mapillary original images (called for populate a Mapillary
    dataset)

    """
    return "tests/data/mapillary/sample/"


@pytest.fixture
def mapillary_sample():
    """Sample of preprocessed Mapillary images"""
    return "tests/data/mapillary/training/"


@pytest.fixture
def mapillary_sample_without_labels_dir():
    return "tests/data/mapillary/sample_no_label/"


@pytest.fixture
def mapillary_nb_images(mapillary_sample):  # pylint: disable=W0621
    return len(os.listdir(os.path.join(mapillary_sample, "images")))


@pytest.fixture
def mapillary_nb_labels(mapillary_input_config):  # pylint: disable=W0621
    with open(mapillary_input_config) as fobj:
        config = json.load(fobj)
    return len(config["labels"])


@pytest.fixture(scope="session")
def mapillary_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("mapillary.json")


@pytest.fixture(scope="session")
def mapillary_temp_dir(tmpdir_factory):
    mapillary_subdir = tmpdir_factory.mktemp("mapillary", numbered=False)
    os.makedirs(os.path.join(mapillary_subdir, "images"))
    os.makedirs(os.path.join(mapillary_subdir, "labels"))
    os.makedirs(os.path.join(mapillary_subdir, "checkpoints"))
    return mapillary_subdir


@pytest.fixture
def shapes_image_size():
    return 64


@pytest.fixture
def shapes_nb_images():
    return 10


@pytest.fixture
def shapes_nb_labels():
    return 4


@pytest.fixture(scope="session")
def shapes_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("shapes.json")


@pytest.fixture
def shapes_sample_config():
    return "tests/data/shapes/training.json"


@pytest.fixture
def shapes_sample():
    return "tests/data/shapes/training/"


@pytest.fixture(scope="session")
def shapes_temp_dir(tmpdir_factory):
    shapes_subdir = tmpdir_factory.mktemp("shapes", numbered=False)
    os.makedirs(os.path.join(shapes_subdir, "images"))
    os.makedirs(os.path.join(shapes_subdir, "labels"))
    os.makedirs(os.path.join(shapes_subdir, "checkpoints"))
    return shapes_subdir


@pytest.fixture
def aerial_raw_image_size():
    return 5000


@pytest.fixture
def aerial_test_image_size():
    return 1000


@pytest.fixture
def aerial_image_size():
    return 240


@pytest.fixture
def aerial_nb_images():
    return 1


@pytest.fixture
def nb_tiles_per_image():
    return 10


@pytest.fixture
def aerial_nb_output_training_images():
    return 10


@pytest.fixture
def aerial_nb_output_testing_images(
    aerial_nb_images, aerial_test_image_size, aerial_image_size
):  # pylint: disable=W0621
    return aerial_nb_images * math.ceil(aerial_test_image_size / aerial_image_size) ** 2


@pytest.fixture
def aerial_nb_labels():
    return 2


@pytest.fixture(scope="session")
def aerial_training_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("aerial_training.json")


@pytest.fixture(scope="session")
def aerial_testing_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("aerial_testing.json")


@pytest.fixture
def aerial_sample_config():
    return "tests/data/aerial/preprocessed/240/training.json"


@pytest.fixture
def aerial_sample():
    return "tests/data/aerial/preprocessed/240/training/"


@pytest.fixture
def aerial_raw_sample():
    """Sample of AerialImage original images (called for populate a AerialImage
    dataset)

    """
    return "tests/data/aerial/input/training/"


@pytest.fixture(scope="session")
def aerial_training_temp_dir(tmpdir_factory):
    aerial_subdir = tmpdir_factory.mktemp("aerial_training", numbered=False)
    os.makedirs(os.path.join(aerial_subdir, "images"))
    os.makedirs(os.path.join(aerial_subdir, "labels"))
    os.makedirs(os.path.join(aerial_subdir, "checkpoints"))
    return aerial_subdir


@pytest.fixture(scope="session")
def aerial_testing_temp_dir(tmpdir_factory):
    aerial_subdir = tmpdir_factory.mktemp("aerial_testing", numbered=False)
    os.makedirs(os.path.join(aerial_subdir, "images"))
    os.makedirs(os.path.join(aerial_subdir, "labels"))
    os.makedirs(os.path.join(aerial_subdir, "checkpoints"))
    return aerial_subdir


@pytest.fixture(scope="session")
def aerial_temp_conf(tmpdir_factory):
    temp_conf = tmpdir_factory.mktemp(".").join("aerial.json")
    return temp_conf


@pytest.fixture
def tanzania_raw_image_size():
    return 1000


@pytest.fixture
def tanzania_image_size():
    return 384


@pytest.fixture
def tanzania_nb_images():
    return 1


@pytest.fixture
def tanzania_nb_output_training_images():
    return 10


@pytest.fixture
def tanzania_nb_output_testing_images(
    tanzania_nb_images, tanzania_raw_image_size, tanzania_image_size
):  # pylint: disable=W0621
    return (
        tanzania_nb_images
        * math.ceil(tanzania_raw_image_size / tanzania_image_size) ** 2
    )


@pytest.fixture
def tanzania_nb_labels():
    return 4


@pytest.fixture(scope="session")
def tanzania_training_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("tanzania_training.json")


@pytest.fixture(scope="session")
def tanzania_testing_config(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("tanzania_testing.json")


@pytest.fixture
def tanzania_sample_config():
    return "tests/data/tanzania/preprocessed/384/training.json"


@pytest.fixture
def tanzania_sample():
    return "tests/data/tanzania/preprocessed/384/training/"


@pytest.fixture
def tanzania_raw_sample():
    """Sample of Tanzania original images (called for populate a
    TanzaniaDataset)

    """
    return "tests/data/tanzania/input/training/"


@pytest.fixture
def tanzania_example_image(tanzania_raw_sample):  # pylint: disable=W0621
    return os.path.join(tanzania_raw_sample, "images", "tanzania_sample.tif")


@pytest.fixture
def tanzania_example_labels(tanzania_raw_sample):  # pylint: disable=W0621
    return os.path.join(tanzania_raw_sample, "labels", "tanzania_sample.geojson")


@pytest.fixture(scope="session")
def tanzania_training_temp_dir(tmpdir_factory):
    tanzania_subdir = tmpdir_factory.mktemp("tanzania_training", numbered=False)
    os.makedirs(os.path.join(tanzania_subdir, "images"))
    os.makedirs(os.path.join(tanzania_subdir, "labels"))
    os.makedirs(os.path.join(tanzania_subdir, "checkpoints"))
    return tanzania_subdir


@pytest.fixture(scope="session")
def tanzania_testing_temp_dir(tmpdir_factory):
    tanzania_subdir = tmpdir_factory.mktemp("tanzania_testing", numbered=False)
    os.makedirs(os.path.join(tanzania_subdir, "images"))
    os.makedirs(os.path.join(tanzania_subdir, "labels"))
    os.makedirs(os.path.join(tanzania_subdir, "checkpoints"))
    return tanzania_subdir


@pytest.fixture(scope="session")
def tanzania_temp_conf(tmpdir_factory):
    temp_conf = tmpdir_factory.mktemp(".").join("tanzania.json")
    return temp_conf


@pytest.fixture(scope="session")
def datapath_repo(tmpdir_factory):
    datapath_subdir = tmpdir_factory.mktemp("datapath", numbered=False)
    return datapath_subdir
