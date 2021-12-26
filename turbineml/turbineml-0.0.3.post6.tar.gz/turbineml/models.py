from genericpath import exists
import requests
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import tempfile
import datetime

from requests.sessions import default_headers

from turbineml.configuration import _config


class TurbineClientModelRegistry:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
    
    def _default_headers(self):
        return {"Authorization": "Bearer " + self.api_key}
    

    def get_model_file(self, org_key, project_key, registry_name, model_id, format_name, path, target_file):
        headers = self._default_headers()
        r = requests.get(
            f"{self.api_url}/modelRegistry/modelFile?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&modelId={model_id}&formatName={format_name}&path={path}",
            headers=headers, stream=True)
        r.raise_for_status()

        with open(target_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        os.chmod(target_file, S_IREAD|S_IRGRP|S_IROTH)
        return target_file

    def list_model_files(self, org_key, project_key, registry_name, model_id, format_name):
        headers = self._default_headers()
        r = requests.get(
            f"{self.api_url}/modelRegistry/listModelFiles?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&modelId={model_id}&formatName={format_name}",
            headers=headers, stream=True)
        r.raise_for_status()

        return r.json()

    def create_model(self, org_key, project_key, registry_name, repository_name):
        headers = self._default_headers()
        r = requests.post(
            f"{self.api_url}/modelRegistry/createModel?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&repositoryName={repository_name}",
            headers=headers)
        r.raise_for_status()

        id = r.json()["id"]
        return id

    def create_model_format(self, org_key, project_key, registry_name, model_id, format_name):
        headers = self._default_headers()
        r = requests.post(
            f"{self.api_url}/modelRegistry/createModelFormat?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&modelId={model_id}&formatName={format_name}",
            headers=headers)
        r.raise_for_status()

    def upload_model_file(self, org_key, project_key, registry_name, model_id, format_name, path, source_file):
        with open(source_file, "rb") as f:
            headers = self._default_headers()
            r = requests.post(
                f"{self.api_url}/modelRegistry/uploadModelFile?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&modelId={model_id}&formatName={format_name}&path={path}",
                headers=headers,
                data=f)
            r.raise_for_status()

    def create_metric_set(self, org_key, project_key, registry_name, model_id, metric_set_name):
        headers = self._default_headers()
        r = requests.post(
            f"{self.api_url}/metrics/createModelMetricSet?organizationKey={org_key}&projectKey={project_key}&registryName={registry_name}&modelId={model_id}&metricSetName={metric_set_name}",
            headers=headers)
        r.raise_for_status()
        id = r.json()["id"]
        return id

    def log_metrics(self, metric_set_id, metrics_list):
        headers = self._default_headers()
        r = requests.post(
            f"{self.api_url}/metrics/logMetrics?metricSetId={metric_set_id}",
            headers=headers,
            json=metrics_list)
        r.raise_for_status()
    
    def log_series_media(self, metric_set_id, step, name, index, mime_type, display_type, file_name):
        with open(file_name,'rb') as payload:
            headers = self._default_headers()
            r = requests.post(
                f"{self.api_url}/metrics/logSeriesMedia?metricSetId={metric_set_id}&step={step}&name={name}&index={index}&mimeType={mime_type}&displayType={display_type}",
                headers=headers,
                data=payload)
            r.raise_for_status()

def _create_client():
    return TurbineClientModelRegistry(_config.get_api_url(), _config.get_api_key())

def get_model_file(org_key, project_key, registry_name, model_id, format_name, path, suffix=None):
    client = _create_client()

    #handle, filename = tempfile.mkstemp(suffix=suffix)
    #os.close(handle)
    filename = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    client.get_model_file(org_key, project_key, registry_name, model_id, format_name, path, filename)
    return filename

def download_model(org_key, project_key, registry_name, model_id, format_name):
    client = _create_client()
    base_dir = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    os.makedirs(base_dir)

    files = client.list_model_files(org_key, project_key, registry_name, model_id, format_name)
    for file in files:
        local_file = os.path.join(base_dir, file)

        dir_name = os.path.dirname(local_file)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
    
        client.get_model_file(org_key, project_key, registry_name, model_id, format_name, file, local_file)
    
    return base_dir

def create_model(org_key, project_key, registry_name, repository_name):
    client = _create_client()
    return client.create_model(org_key, project_key, registry_name, repository_name)

def create_model_format(org_key, project_key, registry_name, model_id, format_name):
    client = _create_client()
    client.create_model_format(org_key, project_key, registry_name, model_id, format_name)

def upload_model_file(org_key, project_key, registry_name, model_id, format_name, path, source_file):
    client = _create_client()
    client.upload_model_file(org_key, project_key, registry_name, model_id, format_name, path, source_file)

def create_metric_set(org_key, project_key, registry_name, model_id, metric_set_name):
    client = _create_client()
    return client.create_metric_set(org_key, project_key, registry_name, model_id, metric_set_name)

def log_metrics(metric_set_id, step, **kwargs):
    client = _create_client()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    metrics_list = [
        {
            "name": k,
            "timestamp": timestamp,
            "step": step,
            "value": kwargs[k]
        }
        for k in kwargs
    ]
    return client.log_metrics(metric_set_id, metrics_list)

def log_series_media(metric_set_id, step, name, index, mime_type, display_type, file_name):
    client = _create_client()
    client.log_series_media(metric_set_id, step, name, index, mime_type, display_type, file_name)
