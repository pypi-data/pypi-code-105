"""Unit test related to the generator building and feeding
"""

import numpy as np
import pytest

from deeposlandia import AVAILABLE_MODELS, generator, utils


def test_feature_detection_labelling_concise():
    """Test `feature_detection_labelling` function in `generator` module by
    considering a concise labelling, *i.e.* all labels are represented into the
    array:
    * as a preliminary verification, check if passing string labels raises an
    AttributeError exception
    * test if output shape is first input shape (batch size) + an additional
    dimension given by the `label_ids` length
    * test if both representation provides the same information (native array
    on the first hand and its one-hot version on the second hand)
    """
    array = np.array(
        [
            [
                [[10, 10, 200], [10, 10, 200], [10, 10, 200]],
                [[200, 200, 200], [200, 200, 200], [10, 10, 200]],
                [[200, 200, 200], [200, 200, 200], [200, 200, 200]],
            ],
            [
                [[10, 200, 10], [10, 200, 10], [10, 10, 200]],
                [[200, 10, 10], [10, 200, 10], [10, 10, 200]],
                [[10, 200, 10], [200, 10, 10], [10, 10, 200]],
            ],
        ]
    )
    labels = np.unique(array.reshape(-1, 3), axis=0).tolist()
    wrong_config = [
        {"id": "0", "color": [10, 10, 200], "is_evaluate": True},
        {"id": "1", "color": [200, 10, 10], "is_evaluate": True},
        {"id": "2", "color": [10, 200, 10], "is_evaluate": True},
        {"id": "3", "color": [200, 200, 200], "is_evaluate": True},
    ]
    with pytest.raises(ValueError):
        res = generator.feature_detection_labelling(array, wrong_config)
    config = [
        {"id": 0, "color": [10, 10, 200], "is_evaluate": True},
        {"id": 1, "color": [200, 10, 10], "is_evaluate": True},
        {"id": 2, "color": [10, 200, 10], "is_evaluate": True},
        {"id": 3, "color": [200, 200, 200], "is_evaluate": True},
    ]
    res = generator.feature_detection_labelling(array, config)
    assert res.shape == (array.shape[0], len(labels))
    assert res.tolist() == [
        [True, False, False, True],
        [True, True, True, False],
    ]


def test_feature_detection_labelling_sparse():
    """Test `feature_detection_labelling` function in `generator` module by
    considering a sparse labelling, *i.e.* the array contains unknown values
    (to mimic the non-evaluated label situations):
    * as a preliminary verification, check if passing string labels raises an
    AttributeError exception
    * test if label length is different from the list of values in the array
    * test if output shape is first input shape (batch size) + an additional
    dimension given by the `label_ids` length
    * test if both representation provides the same information (native array
    on the first hand and its one-hot version on the second hand)
    """
    array = np.array(
        [
            [
                [[10, 10, 200], [10, 10, 200], [10, 10, 200], [200, 10, 10]],
                [
                    [200, 200, 200],
                    [200, 200, 200],
                    [10, 10, 200],
                    [200, 10, 10],
                ],
                [
                    [200, 200, 200],
                    [200, 200, 200],
                    [200, 200, 200],
                    [10, 10, 200],
                ],
                [
                    [200, 200, 200],
                    [200, 200, 200],
                    [200, 200, 200],
                    [10, 10, 200],
                ],
            ],
            [
                [[200, 10, 10], [200, 10, 10], [10, 200, 10], [200, 10, 10]],
                [[200, 200, 200], [10, 200, 10], [10, 200, 10], [10, 200, 10]],
                [[200, 10, 10], [200, 10, 10], [200, 10, 10], [200, 200, 200]],
                [[200, 10, 10], [200, 10, 10], [10, 200, 10], [200, 200, 200]],
            ],
        ]
    )
    labels = np.unique(array.reshape(-1, 3), axis=0).tolist()[:-1]
    wrong_config = [
        {"id": "0", "color": [10, 10, 200], "is_evaluate": True},
        {"id": "1", "color": [200, 10, 10], "is_evaluate": True},
        {"id": "2", "color": [10, 200, 10], "is_evaluate": True},
    ]
    with pytest.raises(ValueError):
        res = generator.feature_detection_labelling(array, wrong_config)
    config = [
        {"id": 0, "color": [10, 10, 200], "is_evaluate": True},
        {"id": 1, "color": [200, 10, 10], "is_evaluate": True},
        {"id": 2, "color": [10, 200, 10], "is_evaluate": True},
    ]
    res = generator.feature_detection_labelling(array, config)
    assert len(labels) != np.amax(array) - np.amin(array) + 1
    assert res.tolist() == [[True, True, False], [False, True, True]]
    assert res.shape == (array.shape[0], len(labels))


def test_featdet_mapillary_generator(
    mapillary_image_size,
    mapillary_sample,
    mapillary_sample_config,
    nb_channels,
):
    """Test the data generator for the Mapillary dataset"""
    batch_size = 10
    config = utils.read_config(mapillary_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "mapillary",
        "featdet",
        mapillary_sample,
        mapillary_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        mapillary_image_size,
        mapillary_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (batch_size, len(label_ids))


def test_featdet_shape_generator(
    shapes_image_size, shapes_sample, shapes_sample_config, nb_channels
):
    """Test the data generator for the shape dataset"""
    batch_size = 10
    config = utils.read_config(shapes_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "shapes",
        "featdet",
        shapes_sample,
        shapes_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        shapes_image_size,
        shapes_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (batch_size, len(label_ids))


def test_semantic_segmentation_labelling_concise():
    """Test `semantic_segmentation_labelling` function in `generator` module by
    considering a concise labelling, *i.e.* the labels correspond to array
    values
    * as a preliminary verification, check if passing string labels raises an
    AttributeError exception
    * test if output shape is input shape + an additional dimension given by
    the `label_ids` length
    * test if both representation provides the same information (native array
    on the first hand and its one-hot version on the second hand)

    """
    array = np.array(
        [
            [
                [[200, 10, 10], [200, 10, 10], [200, 200, 200]],
                [[200, 200, 200], [200, 200, 200], [200, 10, 10]],
                [[200, 200, 200], [200, 200, 200], [200, 200, 200]],
            ],
            [
                [[200, 10, 10], [200, 10, 10], [10, 10, 200]],
                [[10, 200, 10], [10, 200, 10], [10, 10, 200]],
                [[200, 10, 10], [200, 10, 10], [10, 10, 200]],
            ],
        ]
    )
    labels = np.unique(array.reshape(-1, 3), axis=0).tolist()
    wrong_config = [
        {"id": "0", "color": [10, 10, 200], "is_evaluate": True},
        {"id": "1", "color": [200, 10, 10], "is_evaluate": True},
        {"id": "2", "color": [10, 200, 10], "is_evaluate": True},
        {"id": "3", "color": [200, 200, 200], "is_evaluate": True},
    ]
    with pytest.raises(ValueError):
        res = generator.semantic_segmentation_labelling(array, wrong_config)
    config = [
        {"id": 0, "color": [10, 10, 200], "is_evaluate": True},
        {"id": 1, "color": [200, 10, 10], "is_evaluate": True},
        {"id": 2, "color": [10, 200, 10], "is_evaluate": True},
        {"id": 3, "color": [200, 200, 200], "is_evaluate": True},
    ]
    res = generator.semantic_segmentation_labelling(array, config)
    assert res.shape == (array.shape[0], array.shape[1], array.shape[2], len(labels))
    assert res.tolist() == [
        [
            [
                [False, True, False, False],
                [False, True, False, False],
                [False, False, False, True],
            ],
            [
                [False, False, False, True],
                [False, False, False, True],
                [False, True, False, False],
            ],
            [
                [False, False, False, True],
                [False, False, False, True],
                [False, False, False, True],
            ],
        ],
        [
            [
                [False, True, False, False],
                [False, True, False, False],
                [True, False, False, False],
            ],
            [
                [False, False, True, False],
                [False, False, True, False],
                [True, False, False, False],
            ],
            [
                [False, True, False, False],
                [False, True, False, False],
                [True, False, False, False],
            ],
        ],
    ]


def test_semantic_segmentation_labelling_sparse():
    """Test `semantic_segmentation_labelling` function in `generator` module by
    considering a sparse labelling, *i.e.* the array contains unknown values
    (to mimic the non-evaluated label situations)
    * as a preliminary verification, check if passing string labels raises an
    AttributeError exception
    * test if output shape is input shape + an additional dimension given by
    the `label_ids` length
    * test if both representation provides the same information (native array
    on the first hand and its one-hot version on the second hand)

    """
    array = np.array(
        [
            [
                [[200, 10, 10], [200, 10, 10], [200, 200, 200]],
                [[200, 200, 200], [200, 200, 200], [200, 10, 10]],
                [[200, 200, 200], [100, 100, 100], [200, 200, 200]],
            ],
            [
                [[200, 10, 10], [200, 10, 10], [10, 10, 200]],
                [[200, 200, 200], [100, 100, 100], [10, 10, 200]],
                [[200, 10, 10], [200, 10, 10], [10, 10, 200]],
            ],
        ]
    )
    wrong_config = [
        {"id": "0", "color": [10, 10, 200], "is_evaluate": True},
        {"id": "2", "color": [10, 200, 10], "is_evaluate": True},
        {"id": "3", "color": [200, 200, 200], "is_evaluate": True},
    ]
    with pytest.raises(ValueError):
        res = generator.semantic_segmentation_labelling(array, wrong_config)
    config = [
        {"id": 0, "color": [10, 10, 200], "is_evaluate": True},
        {"id": 2, "color": [10, 200, 10], "is_evaluate": True},
        {"id": 3, "color": [200, 200, 200], "is_evaluate": True},
    ]
    labels = [item["id"] for item in config]
    res = generator.semantic_segmentation_labelling(array, config)
    assert len(labels) != np.amax(array) - np.amin(array) + 1
    assert res.shape == (array.shape[0], array.shape[1], array.shape[2], len(labels))
    assert res.tolist() == [
        [
            [
                [False, False, False],
                [False, False, False],
                [False, False, True],
            ],
            [
                [False, False, True],
                [False, False, True],
                [False, False, False],
            ],
            [
                [False, False, True],
                [False, False, False],
                [False, False, True],
            ],
        ],
        [
            [
                [False, False, False],
                [False, False, False],
                [True, False, False],
            ],
            [
                [False, False, True],
                [False, False, False],
                [True, False, False],
            ],
            [
                [False, False, False],
                [False, False, False],
                [True, False, False],
            ],
        ],
    ]


def test_semseg_mapillary_generator(
    mapillary_image_size,
    mapillary_sample,
    mapillary_sample_config,
    nb_channels,
):
    """Test the data generator for the Mapillary dataset"""
    batch_size = 10
    config = utils.read_config(mapillary_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "mapillary",
        "semseg",
        mapillary_sample,
        mapillary_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        mapillary_image_size,
        mapillary_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (
        batch_size,
        mapillary_image_size,
        mapillary_image_size,
        len(label_ids),
    )


def test_semseg_shape_generator(
    shapes_image_size, shapes_sample, shapes_sample_config, nb_channels
):
    """Test the data generator for the shape dataset"""
    batch_size = 10
    config = utils.read_config(shapes_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "shapes",
        "semseg",
        shapes_sample,
        shapes_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        shapes_image_size,
        shapes_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (
        batch_size,
        shapes_image_size,
        shapes_image_size,
        len(label_ids),
    )


def test_semseg_aerial_generator(
    aerial_image_size, aerial_sample, aerial_sample_config, nb_channels
):
    """Test the data generator for the AerialImage dataset"""
    batch_size = 4
    config = utils.read_config(aerial_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "aerial",
        "semseg",
        aerial_sample,
        aerial_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        aerial_image_size,
        aerial_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (
        batch_size,
        aerial_image_size,
        aerial_image_size,
        len(label_ids),
    )


def test_semseg_tanzania_generator(
    tanzania_image_size, tanzania_sample, tanzania_sample_config, nb_channels
):
    """Test the data generator for the Open AI Tanzania dataset"""
    batch_size = 3
    config = utils.read_config(tanzania_sample_config)
    label_ids = [x["id"] for x in config["labels"]]
    gen = generator.create_generator(
        "tanzania",
        "semseg",
        tanzania_sample,
        tanzania_image_size,
        batch_size,
        config["labels"],
    )
    item = next(gen)
    assert len(item) == 2
    im_shape = item[0].shape
    assert im_shape == (
        batch_size,
        tanzania_image_size,
        tanzania_image_size,
        nb_channels,
    )
    label_shape = item[1].shape
    assert label_shape == (
        batch_size,
        tanzania_image_size,
        tanzania_image_size,
        len(label_ids),
    )


def test_wrong_model_dataset_generator(shapes_sample_config):
    """Test a wrong model and wrong dataset"""
    dataset = "fake"
    model = "conquer_the_world"
    image_size = 10
    batch_size = 10
    datapath = "./tests/data/" + dataset + "/training"
    config = utils.read_config(shapes_sample_config)

    # wrong dataset name
    with pytest.raises(ValueError) as excinfo:
        generator.create_generator(
            dataset,
            "featdet",
            datapath,
            image_size,
            batch_size,
            config["labels"],
        )
    assert str(excinfo.value) == "Wrong dataset name {}".format(dataset)

    # wrong model name
    with pytest.raises(ValueError) as excinfo:
        generator.create_generator(
            "shapes", model, datapath, image_size, batch_size, config["labels"]
        )
    expected_failure_msg = "Wrong model name {} (choose amongst {})".format(
        model, AVAILABLE_MODELS
    )
    assert str(excinfo.value) == expected_failure_msg
