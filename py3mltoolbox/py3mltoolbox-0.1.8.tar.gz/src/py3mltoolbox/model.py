import os, sys
import numpy as np
import py3toolbox as tb


def init_model(models=None, name=None):
  assert name is not None, "name cannot be None"
  new_model = {
    "name"        : name,
    "model"       : None,
    "history"     : None,
    "summary"     : None,
    "result"      : None,
    "performance" : None
  }

  if models is None:
    models = {  name: new_model  }
  else:
    models[name] = new_model

  return models



def output_models_summary(model=None, output_folder=None):
  assert model is not None, "model cannot be None"

  # create model specific folder
  output_folder = output_folder + "/" +  model["name"]
  tb.mk_folder (output_folder)


  model = model["model"]
  summary_lines = []
  model.summary(line_length=120, print_fn=lambda x: summary_lines.append(x))

  summary_text = "\n".join(summary_lines)
  summary_json = tb.pretty_json(model.to_json())

  if output_folder is not None:
    summary_file = output_folder + "/model.summary"
    tb.write_file(file_name=summary_file + ".txt",   text=summary_text, mode="w")
    tb.write_file(file_name=summary_file + ".json",  text=summary_json, mode="w")
  
  print (summary_text)  
  return summary_text


if __name__ == '__main__':
  pass

