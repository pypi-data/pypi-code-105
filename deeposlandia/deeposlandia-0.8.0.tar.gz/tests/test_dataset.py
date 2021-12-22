"""Unit test related to the dataset creation, population and loading
"""

import os
import shutil
from pathlib import Path

import pytest

from deeposlandia.datasets.aerial import AerialDataset
from deeposlandia.datasets.mapillary import MapillaryDataset
from deeposlandia.datasets.shapes import ShapeDataset
from deeposlandia.datasets.tanzania import TanzaniaDataset


def test_mapillary_dataset_creation(
    mapillary_image_size, mapillary_nb_labels, mapillary_input_config
):
    """Create a Mapillary dataset from a configuration file"""
    dataset = MapillaryDataset(mapillary_image_size, mapillary_input_config)
    assert dataset.image_size == mapillary_image_size
    assert dataset.get_nb_labels(see_all=True) == mapillary_nb_labels
    assert dataset.get_nb_images() == 0


def test_mapillary_dataset_population(
    mapillary_image_size,
    mapillary_raw_sample,
    mapillary_nb_images,
    mapillary_nb_labels,
    mapillary_input_config,
    mapillary_config,
    mapillary_temp_dir,
):
    """Populate a Mapillary dataset"""
    dataset = MapillaryDataset(mapillary_image_size, mapillary_input_config)
    dataset.populate(
        str(mapillary_temp_dir),
        mapillary_raw_sample,
        nb_images=mapillary_nb_images,
    )
    dataset.save(str(mapillary_config))
    assert dataset.get_nb_labels(see_all=True) == mapillary_nb_labels
    assert dataset.get_nb_images() == mapillary_nb_images
    assert os.path.isfile(str(mapillary_config))
    assert all(
        len(os.listdir(os.path.join(str(mapillary_temp_dir), tmp_dir)))
        == mapillary_nb_images
        for tmp_dir in ["images", "labels"]
    )


def test_mapillary_dataset_population_without_labels(
    mapillary_image_size,
    mapillary_input_config,
    mapillary_sample_without_labels_dir,
    mapillary_nb_images,
    mapillary_temp_dir,
):
    """Fail at populating a Mapillary dataset without labelled images"""
    dataset = MapillaryDataset(mapillary_image_size, mapillary_input_config)
    with pytest.raises(FileNotFoundError) as excinfo:
        dataset.populate(
            str(mapillary_temp_dir),
            mapillary_sample_without_labels_dir,
            nb_images=mapillary_nb_images,
        )
    assert (
        str(excinfo.value).split(":", maxsplit=1)[0]
        == "[Errno 2] No such file or directory"
    )


def test_mapillary_dataset_loading(
    mapillary_image_size,
    mapillary_nb_images,
    mapillary_input_config,
    mapillary_nb_labels,
    mapillary_sample_config,
):
    """Load images into a Mapillary dataset"""
    dataset = MapillaryDataset(mapillary_image_size, mapillary_input_config)
    dataset.load(mapillary_sample_config)
    assert dataset.get_nb_labels() == mapillary_nb_labels
    assert dataset.get_nb_images() == mapillary_nb_images


def test_shape_dataset_creation(shapes_image_size, shapes_nb_labels):
    """Create a Shapes dataset"""
    dataset = ShapeDataset(shapes_image_size)
    assert dataset.image_size == shapes_image_size
    assert dataset.get_nb_labels() == shapes_nb_labels
    assert dataset.get_nb_images() == 0


def test_shape_dataset_population(
    shapes_image_size,
    shapes_nb_images,
    shapes_nb_labels,
    shapes_config,
    shapes_temp_dir,
):
    """Populate a Shapes dataset"""
    dataset = ShapeDataset(shapes_image_size)
    dataset.populate(str(shapes_temp_dir), nb_images=shapes_nb_images)
    dataset.save(str(shapes_config))
    assert dataset.get_nb_labels() == shapes_nb_labels
    assert dataset.get_nb_images() == shapes_nb_images
    assert os.path.isfile(str(shapes_config))
    assert all(
        len(os.listdir(os.path.join(str(shapes_temp_dir), tmp_dir))) == shapes_nb_images
        for tmp_dir in ["images", "labels"]
    )


def test_shape_dataset_loading(
    shapes_image_size, shapes_nb_images, shapes_nb_labels, shapes_sample_config
):
    """Load images into a Shapes dataset"""
    dataset = ShapeDataset(shapes_image_size)
    dataset.load(shapes_sample_config)
    assert dataset.get_nb_labels() == shapes_nb_labels
    assert dataset.get_nb_images() == shapes_nb_images


def test_aerial_dataset_creation(aerial_image_size, aerial_nb_labels):
    """Create a AerialImage dataset"""
    dataset = AerialDataset(aerial_image_size)
    assert dataset.image_size == aerial_image_size
    assert dataset.get_nb_labels() == aerial_nb_labels
    assert dataset.get_nb_images() == 0


def test_aerial_training_dataset_population(
    aerial_image_size,
    aerial_training_temp_dir,
    aerial_raw_sample,
    aerial_nb_images,
    nb_tiles_per_image,
    aerial_training_config,
    aerial_nb_labels,
    aerial_nb_output_training_images,
):
    """Populate a Aerial dataset"""
    dataset = AerialDataset(aerial_image_size)
    dataset.populate(
        str(aerial_training_temp_dir),
        aerial_raw_sample,
        nb_images=aerial_nb_images,
        nb_tiles_per_image=nb_tiles_per_image,
    )
    dataset.save(str(aerial_training_config))
    assert dataset.get_nb_labels() == aerial_nb_labels
    assert dataset.get_nb_images() >= 0.1 * aerial_nb_output_training_images
    assert dataset.get_nb_images() <= aerial_nb_output_training_images + 3
    assert os.path.isfile(str(aerial_training_config))
    assert all(
        len(os.listdir(os.path.join(str(aerial_training_temp_dir), tmp_dir)))
        == dataset.get_nb_images()
        for tmp_dir in ["images", "labels"]
    )


def test_aerial_testing_dataset_population(
    aerial_image_size,
    aerial_testing_temp_dir,
    aerial_raw_sample,
    aerial_nb_images,
    aerial_testing_config,
    aerial_nb_labels,
    aerial_nb_output_testing_images,
):
    """Populate a Aerial dataset"""
    dataset = AerialDataset(aerial_image_size)
    dataset.populate(
        str(aerial_testing_temp_dir),
        aerial_raw_sample,
        nb_images=aerial_nb_images,
        labelling=False,
    )
    dataset.save(str(aerial_testing_config))
    assert dataset.get_nb_labels() == aerial_nb_labels
    assert dataset.get_nb_images() == aerial_nb_output_testing_images
    assert os.path.isfile(str(aerial_testing_config))
    assert (
        len(os.listdir(os.path.join(str(aerial_testing_temp_dir), "images")))
        == dataset.get_nb_images()
    )


def test_aerial_dataset_loading(
    aerial_image_size,
    aerial_testing_config,
    aerial_nb_labels,
    aerial_nb_output_testing_images,
):
    """Load images into a AerialImage dataset"""
    dataset = AerialDataset(aerial_image_size)
    dataset.load(aerial_testing_config)
    assert dataset.get_nb_labels() == aerial_nb_labels
    assert dataset.get_nb_images() == aerial_nb_output_testing_images


def test_tanzania_dataset_creation(tanzania_image_size, tanzania_nb_labels):
    """Create a Tanzania dataset"""
    dataset = TanzaniaDataset(tanzania_image_size)
    assert dataset.image_size == tanzania_image_size
    assert dataset.get_nb_labels() == tanzania_nb_labels
    assert dataset.get_nb_images() == 0


def test_tanzania_training_dataset_population(
    tanzania_image_size,
    tanzania_training_temp_dir,
    tanzania_raw_sample,
    tanzania_nb_images,
    nb_tiles_per_image,
    tanzania_training_config,
    tanzania_nb_labels,
    tanzania_nb_output_training_images,
):
    """Populate a Tanzania dataset"""
    dataset = TanzaniaDataset(tanzania_image_size)
    dataset.populate(
        str(tanzania_training_temp_dir),
        tanzania_raw_sample,
        nb_images=tanzania_nb_images,
        nb_tiles_per_image=nb_tiles_per_image,
    )
    dataset.save(str(tanzania_training_config))
    assert dataset.get_nb_labels() == tanzania_nb_labels
    assert dataset.get_nb_images() >= 0.1 * tanzania_nb_output_training_images
    assert dataset.get_nb_images() <= tanzania_nb_output_training_images + 3
    assert os.path.isfile(str(tanzania_training_config))
    assert all(
        len(os.listdir(os.path.join(str(tanzania_training_temp_dir), tmp_dir)))
        == dataset.get_nb_images()
        for tmp_dir in ["images", "labels"]
    )


def test_tanzania_testing_dataset_population(
    tanzania_image_size,
    tanzania_testing_temp_dir,
    tanzania_raw_sample,
    tanzania_nb_images,
    tanzania_testing_config,
    tanzania_nb_labels,
    tanzania_nb_output_testing_images,
    tanzania_example_image,
):
    """Populate a Tanzania dataset"""
    dataset = TanzaniaDataset(tanzania_image_size)
    dataset.populate(
        str(tanzania_testing_temp_dir),
        tanzania_raw_sample,
        nb_images=tanzania_nb_images,
        labelling=False,
    )
    dataset.save(str(tanzania_testing_config))
    assert dataset.get_nb_labels() == tanzania_nb_labels
    assert dataset.get_nb_images() == tanzania_nb_output_testing_images
    assert os.path.isfile(str(tanzania_testing_config))
    assert (
        len(os.listdir(os.path.join(str(tanzania_testing_temp_dir), "images")))
        == dataset.get_nb_images()
    )
    # Test if one may re-populate with other images: should append the new images to the dataset
    image_basename = Path(tanzania_example_image).stem
    copied_image_basename = Path(tanzania_example_image).stem.replace(
        image_basename, image_basename + "-copy"
    )
    tanzania_example_copied_image = (
        Path(tanzania_example_image).parent / copied_image_basename
    )
    shutil.copy(tanzania_example_image, tanzania_example_copied_image)
    dataset.populate(
        str(tanzania_testing_temp_dir),
        tanzania_raw_sample,
        image_basenames=[copied_image_basename],
        labelling=False,
    )
    assert dataset.get_nb_images() == 2 * tanzania_nb_output_testing_images
    assert (
        len(os.listdir(os.path.join(str(tanzania_testing_temp_dir), "images")))
        == dataset.get_nb_images()
    )
    tanzania_example_copied_image.unlink()


def test_tanzania_testing_dataset_loading(
    tanzania_image_size,
    tanzania_testing_config,
    tanzania_nb_labels,
    tanzania_nb_output_testing_images,
):
    """Load images into a Tanzania dataset"""
    dataset = TanzaniaDataset(tanzania_image_size)
    dataset.load(tanzania_testing_config)
    assert dataset.get_nb_labels() == tanzania_nb_labels
    assert dataset.get_nb_images() == tanzania_nb_output_testing_images
