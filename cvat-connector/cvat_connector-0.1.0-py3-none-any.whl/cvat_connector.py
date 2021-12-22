#  Copyright (c) 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging
import os.path
import time
from typing import Dict, Optional, List

import requests
from requests_toolbelt.multipart import encoder

from cvat_connector.cvat_urls import CVATUrls


class CVATConnector:
	"""
	CVAT API client
	"""

	def __init__(self, host_url: str = "http://localhost:8080/"):
		self.__urls = CVATUrls()

		self._base_url = host_url
		self.__token = None
		self.__auth_header = None

	def _get(self, url: str, json_data: Dict = None, headers: Dict = None) -> Dict:
		"""
		generic get function
		:param url: get url
		:param json_data: json data
		:param headers: get header
		:return: if get is successful response data, else empty dict
		"""
		if headers is None:
			headers = self.__auth_header

		response = requests.get(self._base_url + url, json=json_data, headers=headers)
		if 200 <= response.status_code < 300:
			return response.json()
		else:
			return {}

	def _post(self, url: str, json_data: Dict = None, data: Optional[encoder.MultipartEncoder] = None,
	          headers: Dict = None) -> Dict:
		"""
		generic post function
		:param url: get url
		:param json_data: json data
		:param data: binary data to upload
		:param headers: get header
		:return: if get is successful response data, else empty dict
		"""
		if headers is None:
			headers = self.__auth_header

		response = requests.post(self._base_url + url, json=json_data, data=data, headers=headers)
		if 200 <= response.status_code < 300:
			return response.json()
		else:
			return {}

	def _patch(self, url: str, json_data: Dict = None, headers: Dict = None) -> Dict:
		"""
		generic patch function
		:param url: get url
		:param json_data: json data
		:param headers: get header
		:return: if get is successful response data, else empty dict
		"""
		if headers is None:
			headers = self.__auth_header

		response = requests.patch(self._base_url + url, json=json_data, headers=headers)
		if 200 <= response.status_code < 300:
			return response.json()
		else:
			return {}

	def _delete(self, url: str, json_data: Dict = None, headers: Dict = None) -> Dict:
		"""
		generic patch function
		:param url: get url
		:param json_data: json data
		:param headers: get header
		:return: if get is successful response data, else empty dict
		"""
		if headers is None:
			headers = self.__auth_header

		response = requests.delete(self._base_url + url, json=json_data, headers=headers)
		if 200 <= response.status_code < 300:
			return response.json()
		else:
			return {}

	def login(self, username: str, password: str) -> bool:
		"""
		login function
		:param username: username
		:param password: password
		:return: login response
		"""
		response = requests.post(
			self._base_url + self.__urls.login_url,
			json={'username': username, 'password': password}
		)
		if response.status_code != 200:
			return False
		self.__token = response.json()['key']
		self.__auth_header = {"Authorization": f"Token {self.__token}"}
		return True

	def logout(self) -> None:
		"""
		logout function
		"""
		response = requests.post(self._base_url + self.__urls.logout_url)
		if 200 <= response.status_code < 300:
			logging.info(response.json()['detail'])
		else:
			logging.error("logout error: %s", response.content)

	def get_all_users(self) -> Dict[str, Dict]:
		"""
		gets all users
		:return: dictionary of users. key is username and value is the user details
		"""
		if self.__token is None:
			raise ValueError("not logged in")
		all_users = {}

		next_url = self.__urls.users_url

		while next_url is not None:
			response = self._get(next_url)

			if not bool(response):
				break
			for result in response['results']:
				all_users[result['username']] = result

			next_url = response['next']
		return all_users

	def create_task(self, name: str, project_id: int, assignee_id: int = 0) -> Optional[int]:
		"""
		creates a new task
		:param name: task name
		:param project_id: project id
		:param assignee_id: assignee id
		:return: newly created task's id
		"""
		if self.__token is None:
			raise ValueError("not logged in")

		task_data = {
			'name': name,
			'project_id': project_id,
			'assignee_id': assignee_id
		}
		response = self._post(self.__urls.tasks_url, json_data=task_data)

		task_id = response.get("id")
		return task_id

	def upload_task_data(self, video_path: str, task_id: int,
	                     sync: bool = True, image_quality: int = 50) -> None:
		"""
		upload a video to a given task
		:param video_path: video file path
		:param task_id: task id to upload
		:param sync: wait for cvat to process uploaded data
		:param image_quality: image quality
		:return:
		"""
		if self.__token is None:
			raise ValueError("not logged in")

		if not os.path.exists(video_path):
			return None

		video_name = os.path.basename(video_path)

		video_file = open(video_path, 'rb')
		fields = {
			'client_files[0]': (video_name, video_file, 'video/mp4'), 'image_quality': str(image_quality),
			'use_zip_chunks': 'true',
			'use_cache': 'true'}

		m_data = encoder.MultipartEncoder(fields)

		upload_auth_header = {
			"Authorization": f"Token {self.__token}", 'Content-Type': '', 'Content-Length': '',
			'Accept': 'application/json, text/plain, */*', 'Connection': 'keep-alive'
		}

		# Content type setting is important
		upload_auth_header['Content-Type'] = m_data.content_type
		upload_auth_header['Content-Length'] = str(m_data.len)

		response = self._post(self.__urls.task_data_url.format(task_id),
		                      data=m_data, headers=upload_auth_header)
		if not bool(response):
			print(f"error uploading data for task {task_id}")
		video_file.close()

		fail_count = 0
		while sync:
			response = self._get(self.__urls.task_status_url.format(task_id))
			if not bool(response):
				fail_count += 1
				if fail_count == 10:
					break

			if response['state'] == "Finished":
				break
			time.sleep(1)

	def get_tasks(self, limit: Optional[int] = None, status: Optional[str] = None,
	              assignee: Optional[str] = "all") -> List:
		"""
		gets tasks
		if the limit is none then all the tasks are fetched
		:param limit: limit on fetched tasks
		:param status: annotation, validation or complete
		:param assignee: assignee name. if none, fetch only unassigned tasks. if all, fetch all
		:return: tasks list
		"""

		if self.__token is None:
			raise ValueError("not logged in")

		append_params = []
		if status is not None:
			append_params.append(f"status={status}")
		if assignee is not None and assignee != "all":
			append_params.append(f"assignee={assignee}")

		if len(append_params) > 0:
			append_url = "?" + "&".join(append_params)
		else:
			append_url = ""

		all_tasks = []
		next_url = self.__urls.tasks_url + append_url
		while next_url is not None:
			response = self._get(next_url)
			if not bool(response):
				break

			if assignee is None:
				to_append = []
				for task in response['results']:
					if task['assignee'] is None:
						to_append.append(task)
			else:
				to_append = response['results']

			all_tasks.extend(to_append)
			next_url = response['next']

			if limit is not None and len(all_tasks) >= limit:
				all_tasks = all_tasks[:limit]
				break

		return all_tasks

	def get_unassigned_tasks(self, limit: int = None) -> List:
		"""
		gets tasks
		if the limit is none then all the tasks are fetched
		:param limit: limit on fetched tasks
		:return: tasks list
		"""
		if self.__token is None:
			raise ValueError("not logged in")

		return self.get_tasks(limit=limit, status="annotation", assignee=None)

	def assign_task_to_user(self, task_id: int, user_id: int) -> Dict:
		"""
		assigns a task to a user
		:param task_id: task id
		:param user_id: user id
		:return: assigned task's detail
		"""

		if self.__token is None:
			raise ValueError("not logged in")

		return self._patch(self.__urls.task_url.format(task_id), json_data={'assignee_id': user_id})

	def delete_task(self, task_id: int) -> Dict:
		"""
		deletes a task
		:param task_id: task id
		:return: delete response
		"""

		if self.__token is None:
			raise ValueError("not logged in")

		response = self._delete(self.__urls.tasks_url + "/" + str(task_id))
		return response
