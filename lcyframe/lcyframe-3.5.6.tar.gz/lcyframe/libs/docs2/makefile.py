# -*- coding: utf-8 -*-


class MakeFile(object):

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')

    def set_make_file(self):
        """

        :param make_file_path:
        :return:
        """
        content = """# Minimal makefile for LcyFrame documentation
#
current_root=`pwd`

doc:
	@python -mananasdoc.template $(current_root)

%: Makefile
	@python -msphinx -M html . build
        """
        f = open(self.path + "/Makefile", "w+", encoding='utf-8')
        f.write(content)
        f.close()

