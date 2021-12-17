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

class ProcessJob(object):
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
        'process_id': 'str',
        'process': 'Process',
        'project_id': 'str',
        'project': 'Project',
        'execution_id': 'str',
        'status': 'str',
        'config': 'object',
        'statuses': 'list[ProcessJobStatus]',
        'outputs': 'list[ProcessJobOutput]',
        'analysis_job_id': 'str',
        'analysis_job': 'AnalysisJob',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'process_id': 'processId',
        'process': 'process',
        'project_id': 'projectId',
        'project': 'project',
        'execution_id': 'executionId',
        'status': 'status',
        'config': 'config',
        'statuses': 'statuses',
        'outputs': 'outputs',
        'analysis_job_id': 'analysisJobId',
        'analysis_job': 'analysisJob',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, process_id=None, process=None, project_id=None, project=None, execution_id=None, status=None, config=None, statuses=None, outputs=None, analysis_job_id=None, analysis_job=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """ProcessJob - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._process_id = None
        self._process = None
        self._project_id = None
        self._project = None
        self._execution_id = None
        self._status = None
        self._config = None
        self._statuses = None
        self._outputs = None
        self._analysis_job_id = None
        self._analysis_job = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.process_id = process_id
        if process is not None:
            self.process = process
        self.project_id = project_id
        if project is not None:
            self.project = project
        if execution_id is not None:
            self.execution_id = execution_id
        if status is not None:
            self.status = status
        if config is not None:
            self.config = config
        if statuses is not None:
            self.statuses = statuses
        if outputs is not None:
            self.outputs = outputs
        if analysis_job_id is not None:
            self.analysis_job_id = analysis_job_id
        if analysis_job is not None:
            self.analysis_job = analysis_job
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
        """Gets the id of this ProcessJob.  # noqa: E501


        :return: The id of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProcessJob.


        :param id: The id of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def process_id(self):
        """Gets the process_id of this ProcessJob.  # noqa: E501


        :return: The process_id of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._process_id

    @process_id.setter
    def process_id(self, process_id):
        """Sets the process_id of this ProcessJob.


        :param process_id: The process_id of this ProcessJob.  # noqa: E501
        :type: str
        """
        if process_id is None:
            raise ValueError("Invalid value for `process_id`, must not be `None`")  # noqa: E501

        self._process_id = process_id

    @property
    def process(self):
        """Gets the process of this ProcessJob.  # noqa: E501


        :return: The process of this ProcessJob.  # noqa: E501
        :rtype: Process
        """
        return self._process

    @process.setter
    def process(self, process):
        """Sets the process of this ProcessJob.


        :param process: The process of this ProcessJob.  # noqa: E501
        :type: Process
        """

        self._process = process

    @property
    def project_id(self):
        """Gets the project_id of this ProcessJob.  # noqa: E501


        :return: The project_id of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ProcessJob.


        :param project_id: The project_id of this ProcessJob.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def project(self):
        """Gets the project of this ProcessJob.  # noqa: E501


        :return: The project of this ProcessJob.  # noqa: E501
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ProcessJob.


        :param project: The project of this ProcessJob.  # noqa: E501
        :type: Project
        """

        self._project = project

    @property
    def execution_id(self):
        """Gets the execution_id of this ProcessJob.  # noqa: E501


        :return: The execution_id of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this ProcessJob.


        :param execution_id: The execution_id of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def status(self):
        """Gets the status of this ProcessJob.  # noqa: E501


        :return: The status of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ProcessJob.


        :param status: The status of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def config(self):
        """Gets the config of this ProcessJob.  # noqa: E501


        :return: The config of this ProcessJob.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this ProcessJob.


        :param config: The config of this ProcessJob.  # noqa: E501
        :type: object
        """

        self._config = config

    @property
    def statuses(self):
        """Gets the statuses of this ProcessJob.  # noqa: E501


        :return: The statuses of this ProcessJob.  # noqa: E501
        :rtype: list[ProcessJobStatus]
        """
        return self._statuses

    @statuses.setter
    def statuses(self, statuses):
        """Sets the statuses of this ProcessJob.


        :param statuses: The statuses of this ProcessJob.  # noqa: E501
        :type: list[ProcessJobStatus]
        """

        self._statuses = statuses

    @property
    def outputs(self):
        """Gets the outputs of this ProcessJob.  # noqa: E501


        :return: The outputs of this ProcessJob.  # noqa: E501
        :rtype: list[ProcessJobOutput]
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this ProcessJob.


        :param outputs: The outputs of this ProcessJob.  # noqa: E501
        :type: list[ProcessJobOutput]
        """

        self._outputs = outputs

    @property
    def analysis_job_id(self):
        """Gets the analysis_job_id of this ProcessJob.  # noqa: E501


        :return: The analysis_job_id of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._analysis_job_id

    @analysis_job_id.setter
    def analysis_job_id(self, analysis_job_id):
        """Sets the analysis_job_id of this ProcessJob.


        :param analysis_job_id: The analysis_job_id of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._analysis_job_id = analysis_job_id

    @property
    def analysis_job(self):
        """Gets the analysis_job of this ProcessJob.  # noqa: E501


        :return: The analysis_job of this ProcessJob.  # noqa: E501
        :rtype: AnalysisJob
        """
        return self._analysis_job

    @analysis_job.setter
    def analysis_job(self, analysis_job):
        """Sets the analysis_job of this ProcessJob.


        :param analysis_job: The analysis_job of this ProcessJob.  # noqa: E501
        :type: AnalysisJob
        """

        self._analysis_job = analysis_job

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ProcessJob.  # noqa: E501


        :return: The last_updated_by of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ProcessJob.


        :param last_updated_by: The last_updated_by of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ProcessJob.  # noqa: E501


        :return: The created_by of this ProcessJob.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ProcessJob.


        :param created_by: The created_by of this ProcessJob.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this ProcessJob.  # noqa: E501


        :return: The created_at of this ProcessJob.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ProcessJob.


        :param created_at: The created_at of this ProcessJob.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ProcessJob.  # noqa: E501


        :return: The updated_at of this ProcessJob.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ProcessJob.


        :param updated_at: The updated_at of this ProcessJob.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this ProcessJob.  # noqa: E501


        :return: The version of this ProcessJob.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ProcessJob.


        :param version: The version of this ProcessJob.  # noqa: E501
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
        if issubclass(ProcessJob, dict):
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
        if not isinstance(other, ProcessJob):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
