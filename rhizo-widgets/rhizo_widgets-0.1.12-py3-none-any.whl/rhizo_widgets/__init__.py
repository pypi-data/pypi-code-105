__version__ = '0.1.0'

import ipywidgets
import os

from boto3.session import Session

def s3_regions():
  return Session().get_available_regions('s3')

class S3Bucket:
  def __init__(self):
    regions = s3_regions()
    
    self._debug_view = ipywidgets.Output(layout={'border': '1px solid black'})
    self._region_dropdown = ipywidgets.Dropdown(options=[''] + regions,
                                          description='AWS Region:')

    self._bucket_name_text = ipywidgets.Text(
    placeholder='my-bucket',
    description='S3 Bucket Name:')

    self._download_bucket_path_text = ipywidgets.Text(
    placeholder='/bucket/prefix/',
    description='Bucket Path:')
    
    self._upload_bucket_path_text = ipywidgets.Text(
    placeholder='/bucket/prefix/',
    description='Bucket Path:')

    self._download_folder_text = ipywidgets.Text(
    placeholder='./local/folder',
    description='Local folder:' )
    
    self._upload_folder_text = ipywidgets.Text(
    placeholder='./local/folder',
    description='Local folder:' )
  
  @property
  def region(self):
    return self._region_dropdown.value

  @property
  def bucket_name(self):
    return self._bucket_name_text.value

  @property
  def download_bucket_path(self):
    return (self._download_bucket_path_text.value.rstrip('/') + '/').lstrip('/') # guarantees either empty string or a prefix with no leading / and a trailing /
  
  @property
  def upload_bucket_path(self):
    return (self._upload_bucket_path_text.value.rstrip('/') + '/').lstrip('/') # guarantees either empty string or a prefix with no leading / and a trailing /
  
  @property
  def download_folder(self):
    return os.path.abspath(self._download_folder_text.value)

  @property
  def upload_folder(self):
    return os.path.abspath(self._upload_folder_text.value)

  def bucket_form(self):
      return ipywidgets.VBox([
          self._region_dropdown,
          self._bucket_name_text,
      ])

  def download_form(self):
      return ipywidgets.VBox([
          self._region_dropdown,
          self._bucket_name_text,
          self._download_bucket_path_text,
          self._download_folder_text,
      ])

  def upload_form(self):
    return ipywidgets.VBox([
        self._upload_folder_text,
        self._region_dropdown,
        self._bucket_name_text,
        self._upload_bucket_path_text,
    ])
