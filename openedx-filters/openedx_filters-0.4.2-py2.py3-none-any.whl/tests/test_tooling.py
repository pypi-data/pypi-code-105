"""
Tests for pipeline runner used by filters.
"""
from unittest.mock import Mock, patch

import ddt
from django.test import TestCase, override_settings

from openedx_filters import PipelineStep
from openedx_filters.exceptions import OpenEdxFilterException
from openedx_filters.tooling import OpenEdxPublicFilter


class PreEnrollmentFilterMock(OpenEdxPublicFilter):

    filter_type = "org.openedx.learning.course.enrollment.started.v1"


class FirstPipelineStep(PipelineStep):
    """
    Utility function used when getting steps for pipeline.
    """

    def run_filter(self, **kwargs):
        pass


class SecondPipelineStep(PipelineStep):
    """
    Utility class used when getting steps for pipeline.
    """

    def run_filter(self, **kwargs):
        pass


@ddt.ddt
class TestOpenEdxFiltersUtilities(TestCase):
    """
    Test class to verify standard behavior of utility methods that belong to OpenEdxPublicFilter.
    """

    def test_get_empty_function_list(self):
        """
        This method is used to verify the behavior of get_steps_for_pipeline when an empty pipeline is
        passed as argument.

        Expected behavior:
            Returns an empty list.
        """
        pipeline = []

        function_list = PreEnrollmentFilterMock.get_steps_for_pipeline(pipeline)

        self.assertEqual(function_list, pipeline)

    def test_get_non_existing_function(self):
        """
        This method is used to verify the behavior of get_steps_for_pipeline when a non-existing function
        path is passed inside the pipeline argument.

        Expected behavior:
            Returns a list without the non-existing function.
        """
        pipeline = [
            "openedx_filters.tests.test_tooling.FirstPipelineStep",
            "openedx_filters.tests.test_tooling.non_existant",
        ]
        log_message = "Failed to import '{}'.".format(
            "openedx_filters.tests.test_tooling.non_existant",
        )

        with self.assertLogs() as captured:
            step_list = PreEnrollmentFilterMock.get_steps_for_pipeline(pipeline)

        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )
        self.assertEqual(step_list, [FirstPipelineStep])

    def test_get_non_existing_module_func(self):
        """
        This method is used to verify the behavior of get_steps_for_pipeline when a non-existing module
        path is passed inside the pipeline argument.

        Expected behavior:
            Returns a list without the non-existing function.
        """
        pipeline = [
            "openedx_filters.tests.test_tooling.FirstPipelineStep",
            "openedx_filters.non_existent.test_tooling.FirstPipelineStep",
        ]
        log_message = "Failed to import '{}'.".format(
            "openedx_filters.non_existent.test_tooling.FirstPipelineStep"
        )

        with self.assertLogs() as captured:
            step_list = PreEnrollmentFilterMock.get_steps_for_pipeline(pipeline)

        self.assertEqual(captured.records[0].getMessage(), log_message)
        self.assertEqual(step_list, [FirstPipelineStep])

    def test_get_step_list(self):
        """
        This method is used to verify the behavior of get_steps_for_pipeline when a list of steps
        paths is passed as the pipeline parameter.

        Expected behavior:
            Returns a list with the function objects.
        """
        pipeline = [
            "openedx_filters.tests.test_tooling.FirstPipelineStep",
            "openedx_filters.tests.test_tooling.SecondPipelineStep",
        ]

        function_list = PreEnrollmentFilterMock.get_steps_for_pipeline(pipeline)

        self.assertEqual(function_list, [FirstPipelineStep, SecondPipelineStep])

    def test_get_empty_filter_config(self):
        """
        This method is used to verify the behavior of
        get_filter_config when a trigger without a
        OPEN_EDX_FILTERS_CONFIG is passed as parameter.

        Expected behavior:
            Returns an empty dictionary.
        """
        result = PreEnrollmentFilterMock.get_filter_config()

        self.assertEqual(result, {})

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": False,
                "log_level": "debug",
            },
        },
    )
    def test_get_filter_config(self):
        """
        This method is used to verify the behavior of
        get_filter_config when a trigger with
        OPEN_EDX_FILTERS_CONFIG defined is passed as parameter.

        Expected behavior:
            Returns a tuple with pipeline configurations.
        """
        expected_result = {
            "pipeline": [
                "openedx_filters.tests.test_tooling.FirstPipelineStep",
                "openedx_filters.tests.test_tooling.SecondPipelineStep",
            ],
            "fail_silently": False,
            "log_level": "debug",
        }

        result = PreEnrollmentFilterMock.get_filter_config()

        self.assertDictEqual(result, expected_result)

    @patch("openedx_filters.tooling.OpenEdxPublicFilter.get_filter_config")
    @ddt.data(
        (
            {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                ],
                "fail_silently": False,
                "log_level": "debug",
            },
            (
                [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                ],
                False,
                {"log_level": "debug"},
            ),
        ),
        (
            [
                "openedx_filters.tests.test_tooling.FirstPipelineStep",
                "openedx_filters.tests.test_tooling.FirstPipelineStep",
            ],
            (
                [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                ],
                True,
                {}
            ),
        ),
        (
            "openedx_filters.tests.test_tooling.FirstPipelineStep",
            (["openedx_filters.tests.test_tooling.FirstPipelineStep", ], True, {},),
        ),
    )
    @ddt.unpack
    def test_get_pipeline_config(self, config, expected_result, get_filter_config_mock):
        """
        This method is used to verify the behavior of get_pipeline_configuration when a trigger with
        OPEN_EDX_FILTERS_CONFIG defined is passed as parameter.

        Expected behavior:
            Returns a tuple with the pipeline and exception handling
            configuration.
        """
        get_filter_config_mock.return_value = config

        result = PreEnrollmentFilterMock.get_pipeline_configuration()

        self.assertTupleEqual(result, expected_result)


class TestOpenEdxFiltersExecution(TestCase):
    """
    Test class to verify standard behavior of the Pipeline runner.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.kwargs = {
            "request": Mock(),
        }
        self.metadata = {
            "filter_type": "org.openedx.learning.course.enrollment.started.v1",
            "running_pipeline": [
                "openedx_filters.tests.test_tooling.FirstPipelineStep",
                "openedx_filters.tests.test_tooling.SecondPipelineStep",
            ],
            "log_level": "debug",
        }

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [],
                "fail_silently": False,
                "log_level": "debug",
            },
        },
    )
    def test_run_empty_pipeline(self):
        """
        This method runs an empty pipeline, i.e, a pipeline without
        defined functions.

        Expected behavior:
            Returns the same input arguments.
        """
        result = PreEnrollmentFilterMock.run_pipeline(**self.kwargs)

        self.assertDictEqual(result, self.kwargs)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": False,
                "log_level": "debug",
            },
        },
    )
    @patch("openedx_filters.tests.test_tooling.SecondPipelineStep")
    @patch("openedx_filters.tests.test_tooling.FirstPipelineStep")
    def test_raise_filter_exception(self, filter_step_fail, filter_step_success):
        """
        This method runs a pipeline with a step that raises OpenEdxFilterException.

        Expected behavior:
            The pipeline re-raises the exception caught.
        """
        filter_step_fail.__name__ = "SecondPipelineStep"
        exception_message = "There was an error executing filter X."
        filter_step_fail.return_value.run_filter.side_effect = OpenEdxFilterException(message=exception_message)

        with self.assertRaises(OpenEdxFilterException):
            PreEnrollmentFilterMock.run_pipeline(**self.kwargs)
        filter_step_success.return_value.run_filter.assert_not_called()

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": True,
                "log_level": "debug",
            },
        },
    )
    @patch("openedx_filters.tests.test_tooling.SecondPipelineStep")
    @patch("openedx_filters.tests.test_tooling.FirstPipelineStep")
    def test_raise_common_exception(self, filter_step_success, filter_step_fail):
        """
        This method runs a pipeline with a function that raises
        OpenEdxFilterException but raise_exception is set to False. This means
        fail_silently must be set to True or not defined.

        Expected behavior:
            The pipeline does not re-raise the exception caught.
        """
        return_value = {
            "request": Mock(),
        }
        filter_step_success.return_value.run_filter.return_value = return_value
        filter_step_fail.return_value.run_filter.side_effect = TypeError
        filter_step_success.__name__ = "FirstPipelineStep"
        filter_step_fail.__name__ = "SecondPipelineStep"
        result = PreEnrollmentFilterMock.run_pipeline(**self.kwargs)

        self.assertDictEqual(result, return_value)
        filter_step_success.return_value.run_filter.assert_called_once_with(**self.kwargs)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": True,
                "log_level": "debug",
            },
        },
    )
    @patch("openedx_filters.tests.test_tooling.SecondPipelineStep")
    @patch("openedx_filters.tests.test_tooling.FirstPipelineStep")
    def test_not_raise_regular_exception(self, filter_step_success, filter_step_fail):
        """
        This method runs a pipeline with a function that raises a common Exception.

        Expected behavior:
            The pipeline continues execution after caughting Exception.
        """
        return_value = {
            "request": Mock(),
        }
        filter_step_fail.return_value.run_filter.side_effect = ValueError("Value error exception")
        filter_step_success.return_value.run_filter.return_value = return_value
        filter_step_success.__name__ = "FirstPipelineStep"
        filter_step_fail.__name__ = "SecondPipelineStep"

        result = PreEnrollmentFilterMock.run_pipeline(**self.kwargs)

        self.assertDictEqual(result, return_value)
        filter_step_success.return_value.run_filter.assert_called_once_with(**self.kwargs)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": False,
                "log_level": "debug",
            },
        },
    )
    @patch("openedx_filters.tests.test_tooling.SecondPipelineStep")
    @patch("openedx_filters.tests.test_tooling.FirstPipelineStep")
    def test_getting_pipeline_result(self, first_filter, second_filter):
        """
        This method runs a pipeline with functions defined via configuration.

        Expected behavior:
            Returns the processed dictionary.
        """
        return_value_1st = {
            "request": Mock(),
        }
        return_value_2nd = {
            "user": Mock(),
        }
        return_overall_value = {**return_value_1st, **return_value_2nd}
        first_filter.__name__ = "FirstPipelineStep"
        second_filter.__name__ = "SecondPipelineStep"
        first_filter.return_value.run_filter.return_value = return_value_1st
        second_filter.return_value.run_filter.return_value = return_value_2nd

        result = PreEnrollmentFilterMock.run_pipeline(**self.kwargs)

        first_filter.return_value.run_filter.assert_called_once_with(**self.kwargs)
        second_filter.return_value.run_filter.assert_called_once_with(**return_value_1st)
        self.assertDictEqual(result, return_overall_value)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course.enrollment.started.v1": {
                "pipeline": [
                    "openedx_filters.tests.test_tooling.FirstPipelineStep",
                    "openedx_filters.tests.test_tooling.SecondPipelineStep",
                ],
                "fail_silently": False,
                "log_level": "debug",
            },
        },
    )
    @patch("openedx_filters.tests.test_tooling.SecondPipelineStep")
    @patch("openedx_filters.tests.test_tooling.FirstPipelineStep")
    def test_partial_pipeline(self, first_filter, second_filter):
        """
        This method runs a pipeline with functions defined via configuration.
        At some point, returns an object to stop execution.

        Expected behavior:
            Returns the object used to stop execution.
        """
        first_filter.return_value.run_filter.return_value = Mock()
        first_filter.__name__ = "FirstPipelineStep"
        second_filter.__name__ = "SecondPipelineStep"
        log_message = "Pipeline stopped by 'FirstPipelineStep' for returning an object different from a dictionary."

        with self.assertLogs() as captured:
            PreEnrollmentFilterMock.run_pipeline(**self.kwargs)

        self.assertEqual(
            captured.records[0].getMessage(), log_message,
        )
        first_filter.return_value.run_filter.assert_called_once_with(**self.kwargs)
        second_filter.return_value.run_filter.assert_not_called()
