#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_parsernodes.py                                                          #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementations for AST nodes used and returned by the parser"""

from .macal_parsernodetypes import (BLOCK, INDEX, PARAMS, FOREACH, BREAK, HALT, RETURN)
from .macal_astnode import AstNode

class ast_Block(AstNode):
    """Node for a block of instructions can contain 0 or more instructions."""
    def __init__(self, lex_token):
        """Initializes block node type"""
        super().__init__(BLOCK, lex_token)
        self.closelex_token = None
        self.instruction_list = []

    def close(self, lex_token):
        """closes the node"""
        self.closelex_token = lex_token

    def add_instruction(self, instruction):
        """Adds an instruction to the list of instructions"""
        self.instruction_list.append(instruction)

    def count(self):
        """Returns the number of instructions in the list."""
        return len(self.instruction_list)

    def is_root(self):
        """Returns true if this is the root block, false if it is not."""
        return self.token is None

    def print(self, indent):
        """Returns string representation of the node"""
        old_indent = indent
        if not self.is_root():
            indent = "    {}".format(indent)
        tstr = ""
        for instr in self.instruction_list:
            tstr = "{}{}\n".format(tstr, instr.print(indent))
        if not self.is_root():
            tstr = "{{\n{}{}}}".format(tstr, old_indent)
        return tstr

class ast_list_Index(AstNode):
    """AST Node: Index"""
    def __init__(self, lex_token, expression, closelex_token):
        """Initializes index node type"""
        super().__init__(INDEX, lex_token)
        self.expr = expression
        self.closelex_token = closelex_token

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{} [".format(indent)
        if self.expr is not None:
            tstr = "{} {}".format(tstr, self.expr.print(self.expr))
        return "{} ]".format(tstr)

class ast_function_Param_list(AstNode):
    """AST Node: Parameter list"""
    def __init__(self, lex_token):
        """Initializes parameter list node type"""
        super().__init__(PARAMS, lex_token)
        self.closelex_token = None
        self.params = []

    def close(self, lex_token):
        """closes the node"""
        self.closelex_token = lex_token

    def add_parameter(self, expression):
        """adds a parameter to the list"""
        self.params.append(expression)
        
    def count(self):
        """returns the number of parameters on the list"""
        return len(self.params)

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{}(".format(indent)
        cnt = len(self.params)
        i = 0
        for expr in self.params:
            tstr = "{}{}".format(tstr, self._print_expr(expr))
            if i < cnt-1:
                tstr = "{}, ".format(tstr)
            i += 1
        tstr = "{})".format(tstr)
        return tstr
    
class ast_Break(AstNode):
    """AST Node: Break"""
    def __init__(self, lex_token):
        """Initializes break node type"""
        super().__init__(BREAK, lex_token)
    
    def print(self, indent):
        """Returns string representation of the node"""
        return "{}{}".format(indent, self.node_type)

class ast_Halt(AstNode):
    """AST Node: Halt"""
    def __init__(self, lex_token, expression):
        """Initializes halt node type"""
        super().__init__(HALT, lex_token)
        self.expr = expression

    def print(self, indent):
        """Returns string representation of the node"""
        return "{}HALT {}".format(indent, self._print_expr(self.expr))

class ast_Return(AstNode):
    """AST Node: Return"""
    def __init__(self, lex_token, expression):
        """Initializes return node type"""
        super().__init__(RETURN, lex_token)
        self.expr = expression

    def print(self, indent):
        """Returns string representation of the node"""
        return "{}RETURN {}".format(indent, self._print_expr(self.expr))

