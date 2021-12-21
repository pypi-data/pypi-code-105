__version__ = '0.1.0'

import ipywidgets


class S3Bucket:
  def __init__(self, session):
    regions = session.get_available_regions('s3')
    self.session = session
    self.region_dropdown = ipywidgets.Dropdown(options=[''] + regions,
                                          description='AWS Region:')
  
  def form(self):
      return ipywidgets.VBox([
          self.region_dropdown,
      ])
