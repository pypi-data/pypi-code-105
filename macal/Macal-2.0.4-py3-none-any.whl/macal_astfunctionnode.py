#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astfunctionnode.py                                                  #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementation for AST Function node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodes import ast_Block, ast_function_Param_list
from .macal_parsernodetypes import FUNCTION
from .macal_astvariablenode import ast_Variable
from .macal_lextoken import Token

class ast_Function_definition(AstNode):
    """AST Node: Function"""
    def __init__(self, tid: ast_Variable, opLex: Token, params: ast_function_Param_list,
                 block: ast_Block):
        """Initializes function definition node type"""
        super().__init__(FUNCTION, tid.token)
        self.operand = opLex
        self.ident = tid
        self.params = params
        self.block = block
        self.isextern = False
        self.extern_call = None

    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()

    def print(self, indent):
        """Returns string representation of the node"""
        myname = self.name()
        myparams = self.params.print("")
        myblock = self.block.print(indent)
        return "{}FUNCTION {} {} {}".format(indent, myname, myparams, myblock)
