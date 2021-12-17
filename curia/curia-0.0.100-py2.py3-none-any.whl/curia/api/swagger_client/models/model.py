# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 1.26.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Model(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'outcome_type': 'str',
        'aggregation_type': 'str',
        'aggregation_column': 'str',
        'feature_store': 'str',
        'description': 'str',
        'status': 'str',
        'project_id': 'str',
        'project': 'Project',
        'analysis_id': 'str',
        'analysis': 'Analysis',
        'batch_id': 'str',
        'batch': 'ModelBatch',
        'cohorts': 'list[Cohort]',
        'model_jobs': 'list[ModelJob]',
        'user_favorites': 'list[UserFavorite]',
        'model_datasets': 'list[ModelDataset]',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'outcome_type': 'outcomeType',
        'aggregation_type': 'aggregationType',
        'aggregation_column': 'aggregationColumn',
        'feature_store': 'featureStore',
        'description': 'description',
        'status': 'status',
        'project_id': 'projectId',
        'project': 'project',
        'analysis_id': 'analysisId',
        'analysis': 'analysis',
        'batch_id': 'batchId',
        'batch': 'batch',
        'cohorts': 'cohorts',
        'model_jobs': 'modelJobs',
        'user_favorites': 'userFavorites',
        'model_datasets': 'modelDatasets',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, type=None, outcome_type=None, aggregation_type=None, aggregation_column=None, feature_store=None, description=None, status=None, project_id=None, project=None, analysis_id=None, analysis=None, batch_id=None, batch=None, cohorts=None, model_jobs=None, user_favorites=None, model_datasets=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Model - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._type = None
        self._outcome_type = None
        self._aggregation_type = None
        self._aggregation_column = None
        self._feature_store = None
        self._description = None
        self._status = None
        self._project_id = None
        self._project = None
        self._analysis_id = None
        self._analysis = None
        self._batch_id = None
        self._batch = None
        self._cohorts = None
        self._model_jobs = None
        self._user_favorites = None
        self._model_datasets = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        self.type = type
        if outcome_type is not None:
            self.outcome_type = outcome_type
        if aggregation_type is not None:
            self.aggregation_type = aggregation_type
        if aggregation_column is not None:
            self.aggregation_column = aggregation_column
        self.feature_store = feature_store
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        self.project_id = project_id
        if project is not None:
            self.project = project
        if analysis_id is not None:
            self.analysis_id = analysis_id
        if analysis is not None:
            self.analysis = analysis
        if batch_id is not None:
            self.batch_id = batch_id
        if batch is not None:
            self.batch = batch
        if cohorts is not None:
            self.cohorts = cohorts
        if model_jobs is not None:
            self.model_jobs = model_jobs
        if user_favorites is not None:
            self.user_favorites = user_favorites
        if model_datasets is not None:
            self.model_datasets = model_datasets
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this Model.  # noqa: E501


        :return: The id of this Model.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Model.


        :param id: The id of this Model.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Model.  # noqa: E501


        :return: The name of this Model.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Model.


        :param name: The name of this Model.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this Model.  # noqa: E501


        :return: The type of this Model.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Model.


        :param type: The type of this Model.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def outcome_type(self):
        """Gets the outcome_type of this Model.  # noqa: E501


        :return: The outcome_type of this Model.  # noqa: E501
        :rtype: str
        """
        return self._outcome_type

    @outcome_type.setter
    def outcome_type(self, outcome_type):
        """Sets the outcome_type of this Model.


        :param outcome_type: The outcome_type of this Model.  # noqa: E501
        :type: str
        """
        allowed_values = ["regression", "occurrence"]  # noqa: E501
        if outcome_type not in allowed_values:
            raise ValueError(
                "Invalid value for `outcome_type` ({0}), must be one of {1}"  # noqa: E501
                .format(outcome_type, allowed_values)
            )

        self._outcome_type = outcome_type

    @property
    def aggregation_type(self):
        """Gets the aggregation_type of this Model.  # noqa: E501


        :return: The aggregation_type of this Model.  # noqa: E501
        :rtype: str
        """
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """Sets the aggregation_type of this Model.


        :param aggregation_type: The aggregation_type of this Model.  # noqa: E501
        :type: str
        """
        allowed_values = ["count", "sum", "average", "min", "max"]  # noqa: E501
        if aggregation_type not in allowed_values:
            raise ValueError(
                "Invalid value for `aggregation_type` ({0}), must be one of {1}"  # noqa: E501
                .format(aggregation_type, allowed_values)
            )

        self._aggregation_type = aggregation_type

    @property
    def aggregation_column(self):
        """Gets the aggregation_column of this Model.  # noqa: E501


        :return: The aggregation_column of this Model.  # noqa: E501
        :rtype: str
        """
        return self._aggregation_column

    @aggregation_column.setter
    def aggregation_column(self, aggregation_column):
        """Sets the aggregation_column of this Model.


        :param aggregation_column: The aggregation_column of this Model.  # noqa: E501
        :type: str
        """

        self._aggregation_column = aggregation_column

    @property
    def feature_store(self):
        """Gets the feature_store of this Model.  # noqa: E501


        :return: The feature_store of this Model.  # noqa: E501
        :rtype: str
        """
        return self._feature_store

    @feature_store.setter
    def feature_store(self, feature_store):
        """Sets the feature_store of this Model.


        :param feature_store: The feature_store of this Model.  # noqa: E501
        :type: str
        """
        if feature_store is None:
            raise ValueError("Invalid value for `feature_store`, must not be `None`")  # noqa: E501
        allowed_values = ["curia_data_lake", "byod"]  # noqa: E501
        if feature_store not in allowed_values:
            raise ValueError(
                "Invalid value for `feature_store` ({0}), must be one of {1}"  # noqa: E501
                .format(feature_store, allowed_values)
            )

        self._feature_store = feature_store

    @property
    def description(self):
        """Gets the description of this Model.  # noqa: E501


        :return: The description of this Model.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Model.


        :param description: The description of this Model.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def status(self):
        """Gets the status of this Model.  # noqa: E501


        :return: The status of this Model.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Model.


        :param status: The status of this Model.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def project_id(self):
        """Gets the project_id of this Model.  # noqa: E501


        :return: The project_id of this Model.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Model.


        :param project_id: The project_id of this Model.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def project(self):
        """Gets the project of this Model.  # noqa: E501


        :return: The project of this Model.  # noqa: E501
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Model.


        :param project: The project of this Model.  # noqa: E501
        :type: Project
        """

        self._project = project

    @property
    def analysis_id(self):
        """Gets the analysis_id of this Model.  # noqa: E501


        :return: The analysis_id of this Model.  # noqa: E501
        :rtype: str
        """
        return self._analysis_id

    @analysis_id.setter
    def analysis_id(self, analysis_id):
        """Sets the analysis_id of this Model.


        :param analysis_id: The analysis_id of this Model.  # noqa: E501
        :type: str
        """

        self._analysis_id = analysis_id

    @property
    def analysis(self):
        """Gets the analysis of this Model.  # noqa: E501


        :return: The analysis of this Model.  # noqa: E501
        :rtype: Analysis
        """
        return self._analysis

    @analysis.setter
    def analysis(self, analysis):
        """Sets the analysis of this Model.


        :param analysis: The analysis of this Model.  # noqa: E501
        :type: Analysis
        """

        self._analysis = analysis

    @property
    def batch_id(self):
        """Gets the batch_id of this Model.  # noqa: E501


        :return: The batch_id of this Model.  # noqa: E501
        :rtype: str
        """
        return self._batch_id

    @batch_id.setter
    def batch_id(self, batch_id):
        """Sets the batch_id of this Model.


        :param batch_id: The batch_id of this Model.  # noqa: E501
        :type: str
        """

        self._batch_id = batch_id

    @property
    def batch(self):
        """Gets the batch of this Model.  # noqa: E501


        :return: The batch of this Model.  # noqa: E501
        :rtype: ModelBatch
        """
        return self._batch

    @batch.setter
    def batch(self, batch):
        """Sets the batch of this Model.


        :param batch: The batch of this Model.  # noqa: E501
        :type: ModelBatch
        """

        self._batch = batch

    @property
    def cohorts(self):
        """Gets the cohorts of this Model.  # noqa: E501


        :return: The cohorts of this Model.  # noqa: E501
        :rtype: list[Cohort]
        """
        return self._cohorts

    @cohorts.setter
    def cohorts(self, cohorts):
        """Sets the cohorts of this Model.


        :param cohorts: The cohorts of this Model.  # noqa: E501
        :type: list[Cohort]
        """

        self._cohorts = cohorts

    @property
    def model_jobs(self):
        """Gets the model_jobs of this Model.  # noqa: E501


        :return: The model_jobs of this Model.  # noqa: E501
        :rtype: list[ModelJob]
        """
        return self._model_jobs

    @model_jobs.setter
    def model_jobs(self, model_jobs):
        """Sets the model_jobs of this Model.


        :param model_jobs: The model_jobs of this Model.  # noqa: E501
        :type: list[ModelJob]
        """

        self._model_jobs = model_jobs

    @property
    def user_favorites(self):
        """Gets the user_favorites of this Model.  # noqa: E501


        :return: The user_favorites of this Model.  # noqa: E501
        :rtype: list[UserFavorite]
        """
        return self._user_favorites

    @user_favorites.setter
    def user_favorites(self, user_favorites):
        """Sets the user_favorites of this Model.


        :param user_favorites: The user_favorites of this Model.  # noqa: E501
        :type: list[UserFavorite]
        """

        self._user_favorites = user_favorites

    @property
    def model_datasets(self):
        """Gets the model_datasets of this Model.  # noqa: E501


        :return: The model_datasets of this Model.  # noqa: E501
        :rtype: list[ModelDataset]
        """
        return self._model_datasets

    @model_datasets.setter
    def model_datasets(self, model_datasets):
        """Sets the model_datasets of this Model.


        :param model_datasets: The model_datasets of this Model.  # noqa: E501
        :type: list[ModelDataset]
        """

        self._model_datasets = model_datasets

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Model.  # noqa: E501


        :return: The last_updated_by of this Model.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Model.


        :param last_updated_by: The last_updated_by of this Model.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this Model.  # noqa: E501


        :return: The created_by of this Model.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Model.


        :param created_by: The created_by of this Model.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this Model.  # noqa: E501


        :return: The created_at of this Model.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Model.


        :param created_at: The created_at of this Model.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Model.  # noqa: E501


        :return: The updated_at of this Model.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Model.


        :param updated_at: The updated_at of this Model.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Model.  # noqa: E501


        :return: The version of this Model.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Model.


        :param version: The version of this Model.  # noqa: E501
        :type: float
        """

        self._version = version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Model, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Model):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
