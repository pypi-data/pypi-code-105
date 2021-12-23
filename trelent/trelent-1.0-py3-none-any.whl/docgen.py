# Copyright (c) 2021 Trelent Inc.

# External modules
from difflib import Differ
import math
import os
import requests
import sys
import textwrap

# Internal modules
import trelent.utils as utils


verbose = False

documented_function_counts = {
    "python": 0,
    "java": 0,
    "javascript": 0
}

num_documented_funcs = 0
num_skipped_funcs = 0
num_invalid_funcs = 0

def document_function(func, func_def, func_code, indentation, input_path, file_text, user_api_key):
    # TODO: func_def is based on what is parsed by the tree_hugger lib, which may not
    # always match the source code definition. As a result, if no match is found
    # the docstring will not be used. We need to do our own parsing eventually because
    # we will miss many functions this way. We log these in repo_metadata so that we can track our
    # progress over time: missed_funcs = num_functions - (num_originally_documented + num_trelent_documented)

    # Check for a definition mis-match
    if(func_def not in file_text):
        return file_text

    print("Generating for function '" + func + "' in '" + input_path + "'")
    # Call the Trelent API to get a docstring for the given function
    result = requests.post("https://trelent.npkn.net/document-public-repo/", json={
        "branded": False,
        "snippet": func_code,
        "language": "python",
        "sender": "trelent-cli"
    }, headers={
        "Api-Key": user_api_key,
        "X-Trelent-API-Key": user_api_key
    })

    # Create our docstring
    doc_str = result.json()["docstring"]
    doc_str = textwrap.indent(doc_str, ' '*indentation)
    new_func_def = func_def + doc_str + '\n'

    # Update our code!
    file_text = file_text.replace(func_def, new_func_def)
    documented_function_counts["python"] += 1
    return file_text

def document_folder(api_key, should_insert, folder, verbose_output):

    # Set whether or not to output verbose
    verbose = verbose_output

    # Recursively search the provided directory for source code files
    for root, dirs, files in os.walk(folder):
        for filename in files:

            # Check if this is a python file
            input_path = os.path.join(root, filename)
            lang = input_path[-3:]

            #  or lang == ".js" or lang == ".java"
            if(lang == ".py" and "test" not in input_path and "docs" not in input_path and "documentation" not in input_path and "examples" not in input_path):
                if(lang == ".py"):
                    lang = "python"
                    end_str = ":\n"
                elif(lang == ".js"):
                    lang = "javascript"
                    end_str = ") {"
                else:
                    # Default to Python
                    lang = "python" 
                    end_str = ":\n"

                # Document it!
                if(verbose): print("Parsing " + input_path + "...")

                with open(input_path, 'r+') as file:

                    # Split our file into lines
                    file_text = file.read()
                    original_text = file_text
                    lines = file_text.splitlines(keepends=True)

                    # Call our parsing API
                    parsed_file = requests.get("https://lambda.trelent.net/api/ParseFileFunctions", json={
                        "source": file_text,
                    })

                    parsed_file = parsed_file.json()
                    #print(parsed_file)

                    function_names = parsed_file["names"]
                    function_docstrings = parsed_file["docstrings"]
                    function_boddies = parsed_file["boddies"]

                    # Iterate through all the function names and retrieve the underlying code
                    for func in function_names:

                        # Check if there is already a docstring for this function
                        if(func not in function_docstrings.keys() and func in function_boddies.keys()):

                            # Fetch the desired code
                            func_code = function_boddies[func]
                            token_approx = math.ceil(len(func_code) * 1.1 / 4)

                            # Only generate for functions sufficiently long to be effective
                            if(token_approx > 50):
                                if(token_approx < 4000):

                                    # Check if the function indentation is valid (something we can work with)

                                    # Get the location of our docstring
                                    #if(lang == "javascript"):
                                    #    async_func_def = "async function " + func + "("
                                    #    func_def = "function " + func + "("
#
                                    #    docstring_index = file_text.find(async_func_def)
#
                                    #    if(docstring_index == -1):
                                    #        docstring_index = file_text.find(func_def)
                                    #    else:
                                    #        func_def = async_func_def
#
                                    #    # Retrieve indentation from the source text
                                    #    indentation = utils.get_indentation(lines, func, -1, lang)
#
                                    #    docstring_index -= (indentation + 1)
                                    #else:

                                    # Retrieve function code
                                    func_code = function_boddies[func]
                                    docstring_index = func_code.find(end_str) + 2
                                    func_def = func_code[0:docstring_index]

                                    if("," in func_def):
                                        num_args = len(func_def.split(','))
                                    else:
                                        num_args = 1

                                    # Retrieve indentation from the source text
                                    indentation = utils.get_indentation(lines, func, num_args, lang)
                            
                                    if(indentation != -1):
                                        file_text = document_function(func, func_def, func_code, indentation, input_path, file_text, api_key)
                                    else:
                                        if(verbose): print(f"Invalid function: {func}. Possibly a duplicate function name or other indentation error.")
                                else:
                                    if(verbose): print("Invalid function. Too many tokens (it's too long).")
                            else:
                                if(verbose): print("Invalid function. Too few tokens (it's too short).")

                    # Overwrite our file if there were changes
                    if(original_text != file_text):

                        # Check for insert mode first
                        if(should_insert):
                            file.seek(0)
                            file.write(file_text)
                            file.truncate()
                            if(verbose): print("Added docstrings into " + input_path)
                        else:
                            # Generate diff file
                            differ = Differ()

                            original_lines = original_text.splitlines(keepends=True)
                            updated_lines = file_text.splitlines(keepends=True)

                            diff_file_text = ''.join(differ.compare(original_lines, updated_lines))

                            diff_file_path = input_path + ".diff"
                            with open(diff_file_path, 'w+') as diff_file:
                                diff_file.seek(0)
                                diff_file.write(diff_file_text)
                                diff_file.truncate()

                            if(verbose): print("Added docstrings into " + diff_file_path)

                    else:
                        if(verbose): ("File fully documented, no changes necessary.")
            else:
                if(verbose): print("Skipping non-python, doc, test or example file '" + input_path + "'")

    num_documented_funcs = documented_function_counts["java"] + documented_function_counts["javascript"] + documented_function_counts["python"]


    print(" ")
    print("###########################")
    print(" ")
    print(f'Finished documenting {folder}!')
    print(f'Documented {num_documented_funcs} functions.')
    if(should_insert):
        print(f'Inserted documentation directly into source files.')
    else:
        print(f'Inserted documentation into diff files next to source.')
    print(" ")
    print("###########################")