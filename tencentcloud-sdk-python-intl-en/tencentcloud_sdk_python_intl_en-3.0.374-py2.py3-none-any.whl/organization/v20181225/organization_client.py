# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.organization.v20181225 import models


class OrganizationClient(AbstractClient):
    _apiVersion = '2018-12-25'
    _endpoint = 'organization.tencentcloudapi.com'
    _service = 'organization'


    def AcceptOrganizationInvitation(self, request):
        """This API is used to accept an invitation to an organization.

        :param request: Request instance for AcceptOrganizationInvitation.
        :type request: :class:`tencentcloud.organization.v20181225.models.AcceptOrganizationInvitationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.AcceptOrganizationInvitationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AcceptOrganizationInvitation", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AcceptOrganizationInvitationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddOrganizationNode(self, request):
        """This API is used to add an organizational unit.

        :param request: Request instance for AddOrganizationNode.
        :type request: :class:`tencentcloud.organization.v20181225.models.AddOrganizationNodeRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.AddOrganizationNodeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AddOrganizationNode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddOrganizationNodeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CancelOrganizationInvitation(self, request):
        """This API is used to cancel an invitation to an organization.

        :param request: Request instance for CancelOrganizationInvitation.
        :type request: :class:`tencentcloud.organization.v20181225.models.CancelOrganizationInvitationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.CancelOrganizationInvitationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CancelOrganizationInvitation", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CancelOrganizationInvitationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateOrganization(self, request):
        """This API is used to create an organization.

        :param request: Request instance for CreateOrganization.
        :type request: :class:`tencentcloud.organization.v20181225.models.CreateOrganizationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.CreateOrganizationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateOrganization", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateOrganizationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteOrganization(self, request):
        """This API is used to delete an organization.

        :param request: Request instance for DeleteOrganization.
        :type request: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteOrganization", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteOrganizationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteOrganizationMemberFromNode(self, request):
        """This API is used to delete an organization member.

        :param request: Request instance for DeleteOrganizationMemberFromNode.
        :type request: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationMemberFromNodeRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationMemberFromNodeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteOrganizationMemberFromNode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteOrganizationMemberFromNodeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteOrganizationMembers(self, request):
        """This API is used to delete multiple organization members in a single request.

        :param request: Request instance for DeleteOrganizationMembers.
        :type request: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationMembersRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationMembersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteOrganizationMembers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteOrganizationMembersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteOrganizationNodes(self, request):
        """This API is used to delete multiple organizational units in a single request.

        :param request: Request instance for DeleteOrganizationNodes.
        :type request: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationNodesRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.DeleteOrganizationNodesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteOrganizationNodes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteOrganizationNodesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DenyOrganizationInvitation(self, request):
        """This API is used to decline an invitation to an organization.

        :param request: Request instance for DenyOrganizationInvitation.
        :type request: :class:`tencentcloud.organization.v20181225.models.DenyOrganizationInvitationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.DenyOrganizationInvitationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DenyOrganizationInvitation", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DenyOrganizationInvitationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetOrganization(self, request):
        """This API is used to obtain information on organizations.

        :param request: Request instance for GetOrganization.
        :type request: :class:`tencentcloud.organization.v20181225.models.GetOrganizationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.GetOrganizationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetOrganization", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetOrganizationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetOrganizationMember(self, request):
        """This API is used to obtain information on organization members.

        :param request: Request instance for GetOrganizationMember.
        :type request: :class:`tencentcloud.organization.v20181225.models.GetOrganizationMemberRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.GetOrganizationMemberResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetOrganizationMember", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetOrganizationMemberResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListOrganizationInvitations(self, request):
        """This API is used to obtain an invitation list.

        :param request: Request instance for ListOrganizationInvitations.
        :type request: :class:`tencentcloud.organization.v20181225.models.ListOrganizationInvitationsRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.ListOrganizationInvitationsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListOrganizationInvitations", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListOrganizationInvitationsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListOrganizationMembers(self, request):
        """This API is used to obtain a list of organization members.

        :param request: Request instance for ListOrganizationMembers.
        :type request: :class:`tencentcloud.organization.v20181225.models.ListOrganizationMembersRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.ListOrganizationMembersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListOrganizationMembers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListOrganizationMembersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListOrganizationNodeMembers(self, request):
        """This API is used to obtain a list of organizational unit members.

        :param request: Request instance for ListOrganizationNodeMembers.
        :type request: :class:`tencentcloud.organization.v20181225.models.ListOrganizationNodeMembersRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.ListOrganizationNodeMembersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListOrganizationNodeMembers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListOrganizationNodeMembersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListOrganizationNodes(self, request):
        """This API is used to obtain a list of organizational units.

        :param request: Request instance for ListOrganizationNodes.
        :type request: :class:`tencentcloud.organization.v20181225.models.ListOrganizationNodesRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.ListOrganizationNodesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListOrganizationNodes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListOrganizationNodesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def MoveOrganizationMembersToNode(self, request):
        """This API is used to move members to a specified organizational unit.

        :param request: Request instance for MoveOrganizationMembersToNode.
        :type request: :class:`tencentcloud.organization.v20181225.models.MoveOrganizationMembersToNodeRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.MoveOrganizationMembersToNodeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("MoveOrganizationMembersToNode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.MoveOrganizationMembersToNodeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def QuitOrganization(self, request):
        """This API is used to quit an organization.

        :param request: Request instance for QuitOrganization.
        :type request: :class:`tencentcloud.organization.v20181225.models.QuitOrganizationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.QuitOrganizationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("QuitOrganization", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.QuitOrganizationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendOrganizationInvitation(self, request):
        """This API is used to send an invitation to join an organization.

        :param request: Request instance for SendOrganizationInvitation.
        :type request: :class:`tencentcloud.organization.v20181225.models.SendOrganizationInvitationRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.SendOrganizationInvitationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendOrganizationInvitation", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendOrganizationInvitationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateOrganizationMember(self, request):
        """This API is used to update information on organization members.

        :param request: Request instance for UpdateOrganizationMember.
        :type request: :class:`tencentcloud.organization.v20181225.models.UpdateOrganizationMemberRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.UpdateOrganizationMemberResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateOrganizationMember", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateOrganizationMemberResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateOrganizationNode(self, request):
        """This API is used to update organizational units.

        :param request: Request instance for UpdateOrganizationNode.
        :type request: :class:`tencentcloud.organization.v20181225.models.UpdateOrganizationNodeRequest`
        :rtype: :class:`tencentcloud.organization.v20181225.models.UpdateOrganizationNodeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UpdateOrganizationNode", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateOrganizationNodeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)