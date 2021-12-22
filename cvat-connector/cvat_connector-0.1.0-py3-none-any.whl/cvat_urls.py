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
from dataclasses import dataclass


@dataclass
class CVATUrls:
	"""
	API v1 urls
	"""
	base_api_url = "/api/v1/"

	login_url = base_api_url + "/auth/login"
	logout_url = base_api_url + "/auth/logout"

	users_url = base_api_url + "/users"

	tasks_url = base_api_url + "/tasks"

	task_url = base_api_url + "/tasks/{0}"
	task_data_url = base_api_url + "/tasks/{0}/data"
	task_status_url = base_api_url + "/tasks/{0}/status"
