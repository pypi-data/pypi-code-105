#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astvariablenode.py                                                      #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementation for AST variable node used and returned by the parser"""

from .macal_expr import Expr
from .macal_astnode import AstNode
from .macal_parsernodes import ast_list_Index
from .macal_parsernodetypes import VARIABLE

class ast_Variable(AstNode):
    """AST Node: Variable"""
    def __init__(self, lex_token):
        """Initializes variable node type"""
        super().__init__(VARIABLE, lex_token)
        self.index       = []
        self.value       = None
        self.initialized = False
        self.ref         = False
        self.format      = False

    def set_value(self, value):
        """sets the value, and also sets the initialized flag"""
        self.initialized = True
        self.value = value

    def add_index(self, index: ast_list_Index):
        """add an index to the list of indexies"""
        self.index.append(index)

    def has_index(self):
        """Returns true if indexes exist on the list"""
        return len(self.index) > 0

    def is_initialized(self):
        """Returns true if this variable was initialized"""
        return self.initialized

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{}VARIABLE: {}".format(indent, self.name())
        if self.has_index():
            for i in self.index:
                tstr = "{} {}".format(tstr, i.print(""))
        if self.value is not None:
            tstr = "{} {}".format(tstr, self.value.print(self.value))
        return tstr