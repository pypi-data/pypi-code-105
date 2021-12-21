"""Unit test related to the simple layer creation
"""

from tensorflow import keras as K

from deeposlandia.network import ConvolutionalNeuralNetwork


def test_convolution_shape(shapes_image_size, kernel_size, conv_depth, conv_strides):
    """Test the convolution operation through its output layer shape"""
    cnn = ConvolutionalNeuralNetwork("test", shapes_image_size)
    y = cnn.convolution(
        cnn.in_tensor,
        nb_filters=conv_depth,
        kernel_size=kernel_size,
        strides=conv_strides,
        block_name="convtest",
    )
    model = K.models.Model(cnn.in_tensor, y)
    output_shape = model.output_shape
    assert len(output_shape) == 4
    assert output_shape[1:] == (
        shapes_image_size // conv_strides,
        shapes_image_size // conv_strides,
        conv_depth,
    )


def test_transposed_convolution_shape(
    shapes_image_size, conv_depth, kernel_size, conv_strides
):
    """Test the transposed convolution operation through its output layer shape"""
    cnn = ConvolutionalNeuralNetwork("test", shapes_image_size)
    y = cnn.transposed_convolution(
        cnn.in_tensor,
        nb_filters=conv_depth,
        kernel_size=kernel_size,
        strides=conv_strides,
        block_name="transconvtest",
    )
    model = K.models.Model(cnn.in_tensor, y)
    output_shape = model.output_shape
    assert len(output_shape) == 4
    assert output_shape[1:] == (
        shapes_image_size * conv_strides,
        shapes_image_size * conv_strides,
        conv_depth,
    )


def test_maxpooling_shape(shapes_image_size, nb_channels, pool_size, pool_strides):
    """Test the max pooling operation through its output layer shape"""
    cnn = ConvolutionalNeuralNetwork("test", shapes_image_size, nb_channels)
    y = cnn.maxpool(
        cnn.in_tensor, pool_size=pool_size, strides=pool_strides, block_name="pooltest"
    )
    model = K.models.Model(cnn.in_tensor, y)
    output_shape = model.output_shape
    assert len(output_shape) == 4
    assert output_shape[1:] == (
        shapes_image_size // pool_strides,
        shapes_image_size // pool_strides,
        nb_channels,
    )


def test_dense_shape(shapes_image_size, conv_depth):
    """Test the fully-connected layer through its output shape"""
    cnn = ConvolutionalNeuralNetwork("test", shapes_image_size)
    y = cnn.dense(cnn.in_tensor, depth=conv_depth, block_name="fctest")
    model = K.models.Model(cnn.in_tensor, y)
    output_shape = model.output_shape
    assert len(output_shape) == 4
    assert output_shape[1:] == (
        shapes_image_size,
        shapes_image_size,
        conv_depth,
    )


def test_flatten_shape(shapes_image_size, nb_channels):
    """Test the flattening layer through its output shape"""
    cnn = ConvolutionalNeuralNetwork(
        "test", image_size=shapes_image_size, nb_channels=nb_channels
    )
    y = cnn.flatten(cnn.in_tensor, block_name="flattentest")
    model = K.models.Model(cnn.in_tensor, y)
    output_shape = model.output_shape
    assert len(output_shape) == 2
    assert output_shape[1] == shapes_image_size * shapes_image_size * nb_channels


def test_layer_name(shapes_image_size, kernel_size, conv_depth, conv_strides):
    """Test the convolution operation through its output layer shape"""
    cnn = ConvolutionalNeuralNetwork("test", shapes_image_size)
    y = cnn.convolution(
        cnn.in_tensor,
        nb_filters=conv_depth,
        kernel_size=kernel_size,
        strides=conv_strides,
    )
    y = cnn.convolution(
        y, nb_filters=conv_depth, kernel_size=kernel_size, strides=conv_strides
    )
    model = K.models.Model(cnn.in_tensor, y)
    assert [layer.name for layer in model.layers[1:]] == [
        "conv2d",
        "batch_normalization",
        "activation",
        "conv2d_1",
        "batch_normalization_1",
        "activation_1",
    ]
