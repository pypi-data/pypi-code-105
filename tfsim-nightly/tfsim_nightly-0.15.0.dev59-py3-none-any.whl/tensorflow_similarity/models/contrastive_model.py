from collections import defaultdict
from copy import copy
from pathlib import Path
import json
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np
from tabulate import tabulate
import tensorflow as tf
from tqdm.auto import tqdm

from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.losses import Loss
from tensorflow.keras.metrics import Metric

from tensorflow_similarity.classification_metrics import ClassificationMetric
from tensorflow_similarity.classification_metrics import make_classification_metric  # noqa
from tensorflow_similarity.distances import Distance
from tensorflow_similarity.losses import MetricLoss
from tensorflow_similarity.training_metrics import DistanceMetric
from tensorflow_similarity.evaluators.evaluator import Evaluator
from tensorflow_similarity.indexer import Indexer
from tensorflow_similarity.matchers import ClassificationMatch
from tensorflow_similarity.retrieval_metrics import RetrievalMetric
from tensorflow_similarity.distances import distance_canonicalizer
from tensorflow_similarity.stores import Store
from tensorflow_similarity.search import Search
from tensorflow_similarity.types import FloatTensor, Lookup, IntTensor, Tensor
from tensorflow_similarity.types import PandasDataFrame, CalibrationResults
from termcolor import cprint


@tf.keras.utils.register_keras_serializable(package="Similarity")
class ContrastiveModel(tf.keras.Model):
    def __init__(
        self,
        backbone: tf.keras.Model,
        projector: tf.keras.Model,
        predictor: Optional[tf.keras.Model] = None,
        algorithm: str = "simsiam",
        projector_embedding_layer_name: str = '',
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.backbone = backbone
        self.projector = projector
        self.predictor = predictor
        if projector_embedding_layer_name:
            self.embedding = tf.keras.Model(
                    self.projector.input,
                    self.projector.get_layer(name=projector_embedding_layer_name).output,
            )
        else:
            self.embedding = self.projector

        self.outputs = [self.embedding.output]
        self.output_names = ["projector_output"]
        self.algorithm = algorithm
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")
        self.supported_algorithms = ("simsiam", "simclr", "barlow")

        if self.algorithm not in self.supported_algorithms:
            raise ValueError(
                f"{self.algorithm} is not a supported algorithm."
                f"Supported algorithms are {self.supported_algorithms}."
            )

    def compile(
        self,
        optimizer: Union[Optimizer, str, Dict, List] = "rmsprop",
        loss: Optional[Union[Loss, MetricLoss, str, Dict, List]] = None,
        metrics: Optional[Union[Metric, DistanceMetric, str, Dict, List]] = None,  # noqa
        loss_weights: Optional[Union[List, Dict]] = None,
        weighted_metrics: Optional[Union[Metric, DistanceMetric, str, Dict, List]] = None,  # noqa
        run_eagerly: bool = False,
        steps_per_execution: int = 1,
        distance: Union[Distance, str] = "cosine",
        embedding_output: int = 0,
        kv_store: Union[Store, str] = "memory",
        search: Union[Search, str] = "nmslib",
        evaluator: Union[Evaluator, str] = "memory",
        stat_buffer_size: int = 1000,
        **kwargs
    ):
        """Configures the model for training.

        Args:
            optimizer: String (name of optimizer) or optimizer instance. See
              [tf.keras.optimizers](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers).

            loss: String (name of objective function), objective function, any
              `tensorflow_similarity.loss.*` instance or a `tf.keras.losses.Loss`
              instance. See the [Losses documentation](../losses.md) for a list of
              metric learning specific losses offered by TensorFlow Similairy and
              [tf.keras.losses](https://www.tensorflow.org/api_docs/python/tf/keras/losses)
              for the losses available directly in TensorFlow.

              metrics: List of metrics to be evaluated by the model during
              training and testing. Each of those can be a string, a function or a
              [tensorflow_similairty.metrics.*](../metrics.md) instance. Note that
              the metrics used for some type of metric-learning such as distance
              learning (e.g via triplet loss) have a different prototype than the
              metrics used in standard models and you can't use the
              `tf.keras.metrics` for those type of learning.

              Additionally many distance metrics are computed based of the
              [Indexer()](../indexer.md) performance. E.g Matching Top 1 accuracy.
              For technical and performance reasons, indexing data at each
              training batch to compute those is impractical so those metrics are
              computed at epoch end via the [EvalCallback](../callbacks.md)

              See [Evaluation Metrics](../eval_metrics.md) for a list of available
              metrics.

              For multi-output models you can specify different metrics for
              different outputs by passing a dictionary, such as
              `metrics={'similarity': 'min_neg_gap', 'other': ['accuracy',
              'mse']}`.  You can also pass a list (len = len(outputs)) of lists of
              metrics such as `metrics=[['min_neg_gap'], ['accuracy', 'mse']]` or
              `metrics=['min_neg_gap', ['accuracy', 'mse']]`. For outputs which
              are not related to metrics learning, you can use any of the standard
              `tf.keras.metrics`.

            loss_weights: Optional list or dictionary specifying scalar
              coefficients (Python floats) to weight the loss contributions of
              different model outputs. The loss value that will be minimized by
              the model will then be the *weighted sum* of all individual losses,
              weighted by the `loss_weights` coefficients.  If a list, it is
              expected to have a 1:1 mapping to the model's outputs. If a dict, it
              is expected to map output names (strings) to scalar coefficients.

            weighted_metrics: List of metrics to be evaluated and weighted by
              sample_weight or class_weight during training and testing.

            run_eagerly: Bool. Defaults to `False`. If `True`, this `Model`'s
              logic will not be wrapped in a `tf.function`. Recommended to leave
              this as `None` unless your `Model` cannot be run inside a
              `tf.function`.

            steps_per_execution: Int. Defaults to 1. The number of batches to
              run during each `tf.function` call. Running multiple batches inside
              a single `tf.function` call can greatly improve performance on TPUs
              or small models with a large Python overhead.  At most, one full
              epoch will be run each execution. If a number larger than the size
              of the epoch is passed,  the execution will be truncated to the size
              of the epoch.  Note that if `steps_per_execution` is set to `N`,
              `Callback.on_batch_begin` and `Callback.on_batch_end` methods will
              only be called every `N` batches (i.e. before/after each
              `tf.function` execution).

            distance: Distance used to compute embeddings proximity.  Defaults
              to 'cosine'.

            kv_store: How to store the indexed records.  Defaults to 'memory'.

            search: Which `Search()` framework to use to perform KNN search.
              Defaults to 'nmslib'.

            evaluator: What type of `Evaluator()` to use to evaluate index
              performance. Defaults to in-memory one.

            embedding_output: Which model output head predicts the embeddings
              that should be indexed. Defaults to 0 which is for single output
              model. For multi-head model, the callee, usually the
              `SimilarityModel()` class is responsible for passing the correct
              one.

            stat_buffer_size: Size of the sliding windows buffer used to compute
              index performance. Defaults to 1000.

        Raises:
            ValueError: In case of invalid arguments for
                `optimizer`, `loss` or `metrics`.
        """
        distance_obj = distance_canonicalizer(distance)

        # init index
        self.create_index(
            distance=distance_obj,
            search=search,
            kv_store=kv_store,
            evaluator=evaluator,
            embedding_output=embedding_output,
            stat_buffer_size=stat_buffer_size,
        )

        # call underlying keras method
        super().compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics,
            loss_weights=loss_weights,
            weighted_metrics=weighted_metrics,
            run_eagerly=run_eagerly,
            steps_per_execution=steps_per_execution,
            **kwargs
        )

    @tf.function
    def train_step(self, data):
        view1, view2 = self._parse_views(data)

        # Forward pass through the encoder and predictor
        with tf.GradientTape() as tape:
            loss, p1, p2, z1, z2 = self._forward_pass(view1, view2)

        # collect train variables from both the encoder and the projector
        tvars = self.backbone.trainable_variables
        tvars += self.projector.trainable_variables
        if self.predictor:
            tvars += self.predictor.trainable_variables

        # Compute gradients
        gradients = tape.gradient(loss, tvars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, tvars))

        # Update metrics
        # !This are contrastive metrics with different input
        # TODO: figure out interesting metrics -- z Mae?
        # TODO: check metrics are of the right type in compile?
        if self.predictor:
            y = [p2, p1]
        else:
            y = [z2, z1]
        self.compiled_metrics.update_state([z1, z2], y)

        # report loss manually
        self.loss_tracker.update_state(loss)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}

    @tf.function
    def test_step(self, data):
        view1, view2 = self._parse_views(data)

        loss, p1, p2, z1, z2 = self._forward_pass(view1, view2)

        # Update metrics
        # !This are contrastive metrics with different input
        # TODO: figure out interesting metrics -- z Mae?
        # TODO: check metrics are of the right type in compile?
        if self.predictor:
            y = [p2, p1]
        else:
            y = [z2, z1]
        # report test loss manually
        self.loss_tracker.update_state(loss)

        self.compiled_metrics.update_state([z1, z2], y)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}

    def _forward_pass(self, view1, view2):
        h1 = self.backbone(view1)
        h2 = self.backbone(view2)

        z1 = self.projector(h1)
        z2 = self.projector(h2)

        if self.predictor:
            p1 = self.predictor(z1)
            p2 = self.predictor(z2)
        else:
            p1, p2 = None, None

        if self.algorithm == "simsiam":
            h1 = tf.stop_gradient(h1)
            h2 = tf.stop_gradient(h2)
            l1 = self.compiled_loss(z1, p2)
            l2 = self.compiled_loss(z2, p1)
        elif self.algorithm == "simclr":
            l1 = self.compiled_loss(z1, z2)
            l2 = self.compiled_loss(z2, z1)
        elif self.algorithm == "barlow":
            l1 = self.compiled_loss(z1, z2)
            l2 = 0

        loss = l1 + l2

        return loss, p1, p2, z1, z2

    # fix TF 2.x < 2.7 bugs when using generator
    def call(self, inputs):
        return inputs

    def get_encoder(self):
        "Return encoder model"
        return self.encoder

    def summary(self):
        cprint("[Encoder]", "green")
        self.encoder.summary()
        cprint("\n[Projector]", "magenta")
        self.projector.summary()

    def save(
        self,
        filepath: Union[str, Path],
        save_index: bool = True,
        compression: bool = True,
        overwrite: bool = True,
        include_optimizer: bool = True,
        save_format: Optional[str] = None,
        signatures: Optional[Union[Callable, Mapping[str, Callable]]] = None,
        options: Optional[tf.saved_model.SaveOptions] = None,
        save_traces: bool = True,
    ) -> None:
        """Save Constrative model encoder and projector

        Args:
            filepath: where to save the model.
            save_index: Save the index content. Defaults to True.
            compression: Compress index data. Defaults to True.
            overwrite: Overwrite previous model. Defaults to True.
            include_optimizer: Save optimizer state. Defaults to True.
            save_format: Either 'tf' or 'h5', indicating whether to save the
              model to Tensorflow SavedModel or HDF5. Defaults to 'tf' in
              TF 2.X, and 'h5' in TF 1.X.  signatures: Signatures to save with
              the model. Defaults to None.
            signatures: Signatures to save with the SavedModel. Applicable to
              the 'tf' format only. Please see the signatures argument in
              tf.saved_model.save for details.
            options: A `tf.saved_model.SaveOptions` to save with the model.
              Defaults to None.
            save_traces (optional): When enabled, the SavedModel will store the
              function traces for each layer. This can be disabled, so that only
              the configs of each layer are stored.  Defaults to True. Disabling
              this will decrease serialization time and reduce file size, but it
              requires that all custom layers/models implement a get_config()
              method.
        """
        spath = Path(filepath)
        backbone_path = spath / "backbone"
        proj_path = spath / "projector"
        pred_path = spath / "predictor"
        config_path = spath / "config.json"

        cprint("[Saving backbone model]", "blue")
        cprint("|-path:%s" % backbone_path, "green")
        self.backbone.save(
            str(backbone_path),
            overwrite=overwrite,
            include_optimizer=include_optimizer,
            save_format=save_format,
            signatures=signatures,
            options=options,
            save_traces=save_traces,
        )

        cprint("[Saving projector model]", "blue")
        cprint("|-path:%s" % proj_path, "green")
        self.projector.save(
            str(proj_path),
            overwrite=overwrite,
            include_optimizer=include_optimizer,
            save_format=save_format,
            signatures=signatures,
            options=options,
            save_traces=save_traces,
        )

        cprint("[Saving predictor model]", "blue")
        cprint("|-path:%s" % pred_path, "green")
        self.projector.save(
            str(pred_path),
            overwrite=overwrite,
            include_optimizer=include_optimizer,
            save_format=save_format,
            signatures=signatures,
            options=options,
            save_traces=save_traces,
        )

        super().save(
            str(spath),
            overwrite=overwrite,
            include_optimizer=include_optimizer,
            save_format=save_format,
            signatures=signatures,
            options=options,
            save_traces=save_traces,
        )

        with open(str(config_path), "w+") as o:
            config = self.get_config()
            json.dump(config, o)

        if hasattr(self, "_index") and self._index and save_index:
            self.save_index(filepath, compression=compression)
        else:
            print("Index not saved as save_index=False")

    def get_config(self) -> Dict[str, Any]:
        config = {
            "backbone": self.backbone,
            "projector": self.projector,
            "predictor": self.predictor,
            "algorithm": self.algorithm,
        }
        base_config = super().get_config()
        return {**base_config, **config}

    def _parse_views(
        self, data: Sequence[FloatTensor]
    ) -> Tuple[FloatTensor, FloatTensor]:
        if len(data) == 2:
            view1 = data[0]
            view2 = data[1]
        else:
            view1 = data[0]
            view2 = data[0]

        return view1, view2

    def predict(
        self,
        x: FloatTensor,
        batch_size: Optional[int] = None,
        verbose: int = 0,
        steps: Optional[int] = None,
        callbacks: Optional[tf.keras.callbacks.Callback] = None,
        max_queue_size: int = 10,
        workers: int = 1,
        use_multiprocessing: bool = False,
    ) -> FloatTensor:
        x = self.backbone.predict(
            x,
            batch_size,
            verbose,
            steps,
            callbacks,
            max_queue_size,
            workers,
            use_multiprocessing,
        )
        output: FloatTensor = self.embedding.predict(
            x,
            batch_size,
            verbose,
            steps,
            callbacks,
            max_queue_size,
            workers,
            use_multiprocessing,
        )

        return output

    # TODO (ovallis): Refactor the following indexing code into a MixIn.

    def create_index(
        self,
        distance: Union[Distance, str] = "cosine",
        search: Union[Search, str] = "nmslib",
        kv_store: Union[Store, str] = "memory",
        evaluator: Union[Evaluator, str] = "memory",
        embedding_output: int = 0,
        stat_buffer_size: int = 1000,
    ) -> None:
        """Create the model index to make embeddings searchable via KNN.

        This method is normally called as part of `SimilarityModel.compile()`.
        However, this method is provided if users want to define a custom index
        outside of the `compile()` method.

        NOTE: This method sets `SimilarityModel._index` and will replace any
        existing index.

        Args:
            distance: Distance used to compute embeddings proximity. Defaults to
            'auto'.

            kv_store: How to store the indexed records.  Defaults to 'memory'.

            search: Which `Search()` framework to use to perform KNN search.
            Defaults to 'nmslib'.

            evaluator: What type of `Evaluator()` to use to evaluate index
            performance. Defaults to in-memory one.

            embedding_output: Which model output head predicts the embeddings
            that should be indexed. Defaults to 0 which is for single output
            model. For multi-head model, the callee, usually the
            `SimilarityModel()` class is responsible for passing the correct
            one.

            stat_buffer_size: Size of the sliding windows buffer used to compute
            index performance. Defaults to 1000.

        Raises:
            ValueError: Invalid search framework or key value store.
        """
        # check if we we need to set the embedding head
        num_outputs = len(self.output_names)
        if embedding_output >= num_outputs:
            raise ValueError(
                "Embedding_output value exceed number of model outputs"
            )

        # fetch embedding size as some ANN libs requires it for init
        self.embedding_size = self.outputs[embedding_output].shape[1]

        self._index = Indexer(
            embedding_size=self.embedding_size,
            distance=distance,
            search=search,
            kv_store=kv_store,
            evaluator=evaluator,
            embedding_output=embedding_output,
            stat_buffer_size=stat_buffer_size,
        )

    def index(
        self,
        x: Tensor,
        y: IntTensor = None,
        data: Optional[Tensor] = None,
        build: bool = True,
        verbose: int = 1,
    ):
        """Index data.

        Args:
            x: Samples to index.

            y: class ids associated with the data if any. Defaults to None.

            store_data: store the data associated with the samples in the key
            value store. Defaults to True.

            build: Rebuild the index after indexing. This is needed to make the
            new samples searchable. Set it to false to save processing time
            when calling indexing repeatidly without the need to search between
            the indexing requests. Defaults to True.

            verbose: Output indexing progress info. Defaults to 1.
        """

        if not self._index:
            raise Exception(
                "You need to compile the model with a valid"
                "distance to be able to use the indexing"
            )
        if verbose:
            print("[Indexing %d points]" % len(x))
            print("|-Computing embeddings")
        predictions = self.predict(x)

        self._index.batch_add(
            predictions=predictions,
            labels=y,
            data=data,
            build=build,
            verbose=verbose,
        )

    def index_single(self,
                     x: Tensor,
                     y: IntTensor = None,
                     data: Optional[Tensor] = None,
                     build: bool = True,
                     verbose: int = 1):
        """Index data.

        Args:
            x: Sample to index.

            y: class id associated with the data if any. Defaults to None.

            data: store the data associated with the samples in the key
            value store. Defaults to None.

            build: Rebuild the index after indexing. This is needed to make the
            new samples searchable. Set it to false to save processing time
            when calling indexing repeatidly without the need to search between
            the indexing requests. Defaults to True.

            verbose: Output indexing progress info. Defaults to 1.
        """

        if not self._index:
            raise Exception('You need to compile the model with a valid'
                            'distance to be able to use the indexing')
        if verbose:
            print('[Indexing 1 point]')
            print('|-Computing embeddings')

        x = tf.expand_dims(x, axis=0)
        prediction = self.predict(x)
        self._index.add(prediction=prediction,
                        label=y,
                        data=data,
                        build=build,
                        verbose=verbose)

    def lookup(
        self, x: Tensor, k: int = 5, verbose: int = 1
    ) -> List[List[Lookup]]:
        """Find the k closest matches in the index for a set of samples.

        Args:
            x: Samples to match.

            k: Number of nearest neighboors to lookup. Defaults to 5.

            verbose: display progress. Default to 1.

        Returns
            list of list of k nearest neighboors:
            List[List[Lookup]]
        """
        predictions = self.predict(x)
        return self._index.batch_lookup(
            predictions=predictions, k=k, verbose=verbose
        )

    def single_lookup(self, x: Tensor, k: int = 5) -> List[Lookup]:
        """Find the k closest matches in the index for a given sample.

        Args:
            x: Sample to match.

            k: Number of nearest neighboors to lookup. Defaults to 5.

        Returns
            list of the k nearest neigboors info:
            List[Lookup]
        """
        x = tf.expand_dims(x, axis=0)
        prediction = self.predict(x)
        return self._index.single_lookup(prediction=prediction, k=k)

    def index_summary(self):
        "Display index info summary."
        self._index.print_stats()

    def calibrate(
        self,
        x: FloatTensor,
        y: IntTensor,
        thresholds_targets: MutableMapping[str, float] = {},
        k: int = 1,
        calibration_metric: Union[str, ClassificationMetric] = "f1",
        matcher: Union[str, ClassificationMatch] = "match_nearest",
        extra_metrics: MutableSequence[Union[str, ClassificationMetric]] = [
            "precision", "recall"
        ],  # noqa
        rounding: int = 2,
        verbose: int = 1,
    ) -> CalibrationResults:
        """Calibrate model thresholds using a test dataset.

        TODO: more detailed explaination.

        Args:

            x: examples to use for the calibration.

            y: labels associated with the calibration examples.

            thresholds_targets: Dict of performance targets to (if possible)
            meet with respect to the `calibration_metric`.

            calibration_metric:
            [ClassificationMetric()](classification_metrics/overview.md) used
            to evaluate the performance of the index.

            k: How many neighboors to use during the calibration.
            Defaults to 1.

            matcher: {'match_nearest', 'match_majority_vote'} or
            ClassificationMatch object. Defines the classification matching,
            e.g., match_nearest will count a True Positive if the query_label
            is equal to the label of the nearest neighbor and the distance is
            less than or equal to the distance threshold. Defaults to
            'match_nearest'.

            extra_metrics: List of additional
            `tf.similarity.classification_metrics.ClassificationMetric()`
            to compute and report. Defaults to ['precision', 'recall'].


            rounding: Metric rounding. Default to 2 digits.

            verbose: Be verbose and display calibration results.
            Defaults to 1.

        Returns:
            CalibrationResults containing the thresholds and cutpoints Dicts.
        """

        # predict
        predictions = self.predict(x)

        # calibrate
        return self._index.calibrate(
            predictions=predictions,
            target_labels=y,
            thresholds_targets=thresholds_targets,
            k=k,
            calibration_metric=calibration_metric,
            matcher=matcher,
            extra_metrics=extra_metrics,
            rounding=rounding,
            verbose=verbose,
        )

    def match(
        self,
        x: FloatTensor,
        cutpoint="optimal",
        no_match_label=-1,
        k=1,
        matcher: Union[str, ClassificationMatch] = "match_nearest",
        verbose=0,
    ):
        """Match a set of examples against the calibrated index

        For the match function to work, the index must be calibrated using
        calibrate().

        Args:
            x: Batch of examples to be matched against the index.

            cutpoint: Which calibration threshold to use.
            Defaults to 'optimal' which is the optimal F1 threshold computed
            using calibrate().

            no_match_label: Which label value to assign when there is no
            match. Defaults to -1.

            k: How many neighboors to use during the calibration.
            Defaults to 1.

            matcher: {'match_nearest', 'match_majority_vote'} or
            ClassificationMatch object. Defines the classification matching,
            e.g., match_nearest will count a True Positive if the query_label
            is equal to the label of the nearest neighbor and the distance is
            less than or equal to the distance threshold.

            verbose. Be verbose. Defaults to 0.

        Returns:
            List of class ids that matches for each supplied example

        Notes:
            This function matches all the cutpoints at once internally as there
            is little performance downside to do so and allows to do the
            evaluation in a single go.

        """
        # basic checks
        if not self._index.is_calibrated:
            raise ValueError("Uncalibrated model: run model.calibration()")

        # get predictions
        predictions = self.predict(x)

        # matching
        matches = self._index.match(
            predictions,
            no_match_label=no_match_label,
            k=k,
            matcher=matcher,
            verbose=verbose,
        )

        # select which matches to return
        if cutpoint == "all":  # returns all the cutpoints for eval purpose.
            return matches
        else:  # normal match behavior - returns a specific cut point
            return matches[cutpoint]

    def evaluate_retrieval(
        self,
        x: Tensor,
        y: IntTensor,
        retrieval_metrics: Sequence[RetrievalMetric],  # noqa
        verbose: int = 1,
    ) -> Dict[str, np.ndarray]:
        """Evaluate the quality of the index against a test dataset.

        Args:
            x: Examples to be matched against the index.

            y: Label associated with the examples supplied.

            retrieval_metrics: List of
            [RetrievalMetric()](retrieval_metrics/overview.md) to compute.

            verbose (int, optional): Display results if set to 1 otherwise
            results are returned silently. Defaults to 1.

        Returns:
            Dictionary of metric results where keys are the metric names and
            values are the metrics values.

        Raises:
            IndexError: Index must contain embeddings but is currently empty.
        """
        if self._index.size() == 0:
            raise IndexError("Index must contain embeddings but is "
                             "currently empty. Have you run model.index()?")

        # get embeddings
        if verbose:
            print("|-Computing embeddings")
        predictions = self.predict(x)

        if verbose:
            print("|-Computing retrieval metrics")

        results = self._index.evaluate_retrieval(
            predictions=predictions,
            target_labels=y,
            retrieval_metrics=retrieval_metrics,
            verbose=verbose,
        )

        if verbose:
            table = zip(results.keys(), results.values())
            headers = ["metric", "Value"]
            print("\n [Summary]\n")
            print(tabulate(table, headers=headers))

        return results

    def evaluate_classification(
        self,
        x: Tensor,
        y: IntTensor,
        k: int = 1,
        extra_metrics: MutableSequence[Union[str, ClassificationMetric]] = [
            "precision", "recall"
        ],  # noqa
        matcher: Union[str, ClassificationMatch] = "match_nearest",
        verbose: int = 1,
    ) -> DefaultDict[str, Dict[str, Union[str, np.ndarray]]]:
        """Evaluate model classification matching on a given evaluation dataset.

        Args:
            x: Examples to be matched against the index.

            y: Label associated with the examples supplied.

            k: How many neighbors to use to perform the evaluation.
            Defaults to 1.

            extra_metrics: List of additional
            `tf.similarity.classification_metrics.ClassificationMetric()` to
            compute and report. Defaults to ['precision', 'recall'].

            matcher: {'match_nearest', 'match_majority_vote'} or
            ClassificationMatch object. Defines the classification matching,
            e.g., match_nearest will count a True Positive if the query_label
            is equal to the label of the nearest neighbor and the distance is
            less than or equal to the distance threshold.

            verbose (int, optional): Display results if set to 1 otherwise
            results are returned silently. Defaults to 1.

        Returns:
            Dictionary of (distance_metrics.md)[evaluation metrics]

        Raises:
            IndexError: Index must contain embeddings but is currently empty.
            ValueError: Uncalibrated model: run model.calibration()")
        """
        # There is some code duplication in this function but that is the best
        # solution to keep the end-user API clean and doing inferences once.
        if self._index.size() == 0:
            raise IndexError("Index must contain embeddings but is "
                             "currently empty. Have you run model.index()?")

        if not self._index.is_calibrated:
            raise ValueError("Uncalibrated model: run model.calibration()")

        cal_metric = self._index.get_calibration_metric()

        # get embeddings
        if verbose:
            print("|-Computing embeddings")
        predictions = self.predict(x)

        results: DefaultDict[
            str, Dict[str, Union[str, np.ndarray]]
        ] = defaultdict(dict)

        if verbose:
            pb = tqdm(
                total=len(self._index.cutpoints), desc="Evaluating cutpoints"
            )

        for cp_name, cp_data in self._index.cutpoints.items():
            # create a metric that match at the requested k and threshold
            distance_threshold = float(cp_data["distance"])
            metric = make_classification_metric(cal_metric.name)
            metrics = copy(extra_metrics)
            metrics.append(metric)

            res: Dict[str, Union[str, np.ndarray]] = {}
            res.update(
                self._index.evaluate_classification(
                    predictions,
                    y,
                    [distance_threshold],
                    metrics=metrics,
                    matcher=matcher,
                    k=k,
                )
            )
            res["distance"] = tf.constant([distance_threshold])
            res["name"] = cp_name
            results[cp_name] = res
            if verbose:
                pb.update()

        if verbose:
            pb.close()

        if verbose:
            headers = ["name", cal_metric.name]
            for i in results["optimal"].keys():
                if i not in headers:
                    headers.append(str(i))
            rows = []
            for data in results.values():
                rows.append([data[v] for v in headers])
            print("\n [Summary]\n")
            print(tabulate(rows, headers=headers))

        return results

    def reset_index(self):
        "Reinitialize the index"
        self._index.reset()

    def index_size(self) -> int:
        "Return the index size"
        return self._index.size()

    def load_index(self, filepath: str):
        """Load Index data from a checkpoint and initialize underlying
        structure with the reloaded data.

        Args:
            path: Directory where the checkpoint is located.
            verbose: Be verbose. Defaults to 1.
        """

        index_path = Path(filepath) / "index"
        self._index = Indexer.load(index_path)

    def save_index(self, filepath, compression=True):
        """Save the index to disk

        Args:
            path: directory where to save the index
            compression: Store index data compressed. Defaults to True.
        """
        index_path = Path(filepath) / "index"
        self._index.save(index_path, compression=compression)

    def to_data_frame(self, num_items: int = 0) -> PandasDataFrame:
        """Export data as pandas dataframe

        Args:
            num_items (int, optional): Num items to export to the dataframe.
            Defaults to 0 (unlimited).

        Returns:
            pd.DataFrame: a pandas dataframe.
        """
        return self._index.to_data_frame(num_items=num_items)

    # We don't need from_config as the index is reloaded separatly.
    # this is kept as a reminder that it was looked into and decided to split
    # the index reloading instead of overloading this method.
    # @classmethod
    # def from_config(cls, config):
    #     return super().from_config(**config)
