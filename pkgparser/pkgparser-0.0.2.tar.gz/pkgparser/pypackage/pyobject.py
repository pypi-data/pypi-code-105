import re

from pkgparser import configuration

class PyObject:
    """
    PyObject is a representation of a Python Class or Function.
    """

    def __init__(self, object, object_path, directory_path):
        """
        Args:
            directory_path (string): package directory path
            object (object): Python Class || Python Function
            object_path (string): class or function path
        """
        self.docstring = object.__doc__ if object.__doc__ else str()
        self.object_path = object_path

        # open file
        with open("%s/%s.py" % (directory_path, "/".join(self.object_path.split(".")[0:-1])), "r") as file:

            # load raw file line content
            self.rawfile = [d.strip() for d in file.readlines() if d.strip() != str()]

        # parse class documentation
        self.parse()

    def parse(self):
        """
        Parse docstring into native python objects.
        """

        attrs = list()
        descriptions = list()
        notes = list()
        tracked_lines = list()
        self.returns = str()

        # split blob on line return
        lines = [d.strip() for d in self.docstring.split("\n") if d.strip() is not str()] if self.docstring else list()

        # loop through lines
        for i, line in enumerate(lines):

            # set expression
            regex = re.compile("returns:", re.IGNORECASE)

            # check for return statement
            if regex.match(line):

                # update self
                self.returns = lines[i + 1].strip() if i + 1 < len(lines) else str()

                # add to tracker
                tracked_lines.append(i)
                tracked_lines.append(i+1)

            else:

                attr_or_note = re.match("\w+:", line)

                # check if line appears as a key/value set
                if attr_or_note:

                    # split off the key
                    key = attr_or_note.group(0).split(":")[0]

                    # if the key has content immediatley following the colon
                    # it is not a key/value store but some kind of note
                    # in additioon to the description
                    if re.match("\w+: ", line):

                        # split on :
                        toks = [d.strip() for d in line.split(":")[1:]]

                        # see if value is appended on same line
                        note_description = ":".join(toks)

                        # add to list
                        notes.append({
                            "key": key,
                            "value": note_description if note_description else lines[i + 1].strip()
                        })

                        # add to tracker
                        tracked_lines.append(i)

                    else:

                        # stash data
                        attr_set = {
                            "key": key,
                            "values": list()
                        }

                        # loop through lines of docstring
                        for j, l in enumerate(lines):

                            # start after attribute index
                            if j > i:

                                # stop if hit a line that looks like an attribute or note key
                                if re.match("\w+:", l):
                                    break

                                # add values to attribute set
                                attr_set["values"].append({
                                    "key": l.split("(")[0].strip(),
                                    "type": l.split("(")[-1].split(")")[0].strip(),
                                    "value": l.split(":")[-1].strip(),
                                    "required": True,
                                    "default": str()
                                })

                                # add to tracker
                                tracked_lines.append(j)

                        # add to list
                        attrs.append(attr_set)

                        # add to tracker
                        tracked_lines.append(i)

            # check if we processed the line
            if i not in tracked_lines:

                # any unstructured text will be assumed to be description
                descriptions.append(line)

        # update self
        self.attrs = attrs
        self.descriptions = descriptions
        self.notes = notes
