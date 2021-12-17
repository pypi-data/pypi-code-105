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

class Process(object):
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
        'type': 'ProcessType',
        'project_id': 'str',
        'project': 'Project',
        'status': 'str',
        'process_jobs': 'list[ProcessJob]',
        'analysis_id': 'str',
        'analysis': 'Analysis',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'type': 'type',
        'project_id': 'projectId',
        'project': 'project',
        'status': 'status',
        'process_jobs': 'processJobs',
        'analysis_id': 'analysisId',
        'analysis': 'analysis',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, type=None, project_id=None, project=None, status=None, process_jobs=None, analysis_id=None, analysis=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Process - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._type = None
        self._project_id = None
        self._project = None
        self._status = None
        self._process_jobs = None
        self._analysis_id = None
        self._analysis = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.type = type
        self.project_id = project_id
        if project is not None:
            self.project = project
        if status is not None:
            self.status = status
        if process_jobs is not None:
            self.process_jobs = process_jobs
        if analysis_id is not None:
            self.analysis_id = analysis_id
        if analysis is not None:
            self.analysis = analysis
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
        """Gets the id of this Process.  # noqa: E501


        :return: The id of this Process.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Process.


        :param id: The id of this Process.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def type(self):
        """Gets the type of this Process.  # noqa: E501


        :return: The type of this Process.  # noqa: E501
        :rtype: ProcessType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Process.


        :param type: The type of this Process.  # noqa: E501
        :type: ProcessType
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def project_id(self):
        """Gets the project_id of this Process.  # noqa: E501


        :return: The project_id of this Process.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Process.


        :param project_id: The project_id of this Process.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def project(self):
        """Gets the project of this Process.  # noqa: E501


        :return: The project of this Process.  # noqa: E501
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Process.


        :param project: The project of this Process.  # noqa: E501
        :type: Project
        """

        self._project = project

    @property
    def status(self):
        """Gets the status of this Process.  # noqa: E501


        :return: The status of this Process.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Process.


        :param status: The status of this Process.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def process_jobs(self):
        """Gets the process_jobs of this Process.  # noqa: E501


        :return: The process_jobs of this Process.  # noqa: E501
        :rtype: list[ProcessJob]
        """
        return self._process_jobs

    @process_jobs.setter
    def process_jobs(self, process_jobs):
        """Sets the process_jobs of this Process.


        :param process_jobs: The process_jobs of this Process.  # noqa: E501
        :type: list[ProcessJob]
        """

        self._process_jobs = process_jobs

    @property
    def analysis_id(self):
        """Gets the analysis_id of this Process.  # noqa: E501


        :return: The analysis_id of this Process.  # noqa: E501
        :rtype: str
        """
        return self._analysis_id

    @analysis_id.setter
    def analysis_id(self, analysis_id):
        """Sets the analysis_id of this Process.


        :param analysis_id: The analysis_id of this Process.  # noqa: E501
        :type: str
        """

        self._analysis_id = analysis_id

    @property
    def analysis(self):
        """Gets the analysis of this Process.  # noqa: E501


        :return: The analysis of this Process.  # noqa: E501
        :rtype: Analysis
        """
        return self._analysis

    @analysis.setter
    def analysis(self, analysis):
        """Sets the analysis of this Process.


        :param analysis: The analysis of this Process.  # noqa: E501
        :type: Analysis
        """

        self._analysis = analysis

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Process.  # noqa: E501


        :return: The last_updated_by of this Process.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Process.


        :param last_updated_by: The last_updated_by of this Process.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this Process.  # noqa: E501


        :return: The created_by of this Process.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Process.


        :param created_by: The created_by of this Process.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this Process.  # noqa: E501


        :return: The created_at of this Process.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Process.


        :param created_at: The created_at of this Process.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Process.  # noqa: E501


        :return: The updated_at of this Process.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Process.


        :param updated_at: The updated_at of this Process.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Process.  # noqa: E501


        :return: The version of this Process.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Process.


        :param version: The version of this Process.  # noqa: E501
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
        if issubclass(Process, dict):
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
        if not isinstance(other, Process):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
