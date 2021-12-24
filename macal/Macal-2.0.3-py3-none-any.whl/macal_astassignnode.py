#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astassignnode.py                                                        #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementation for AST Assign node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodetypes import ASSIGN
from .macal_lextokentypes import NEW_ARRAY_INDEX
from .macal_astvariablenode import ast_Variable

class ast_Assign(AstNode):
    """AST Node: Assign"""
    def __init__(self, operand, tid: ast_Variable, expression):
        """Initializes assign node type"""
        super().__init__(ASSIGN, tid.token)
        self.operand = operand
        self.ident = tid
        self.expr = expression
        self.ref = False
        self.ref_token = None

    def print(self, indent):
        """Returns string representation of the node"""
        name = self.ident.name()
        if self.ref:
            name = "REF: {}".format(name)
        if self.ident.has_index():
            for idx in self.ident.index:
                if isinstance(idx.expr, ast_Variable):
                    name="{}[{}]".format(name, idx.expr.print(idx.expr))
                else:
                    left = idx.expr.left.value
                    if left == NEW_ARRAY_INDEX:
                        name = "new array index {}[]".format(name)
                    else:
                        name = "normal index {}[{}]".format(name, left)
        operand = self.operand[1]
        expr = self._print_expr(self.expr)
        return "{} ASSIGN {} {} {}".format(indent, name, operand, expr)