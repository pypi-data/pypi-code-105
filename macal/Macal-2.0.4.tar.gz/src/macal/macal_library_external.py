#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_external.py                                                     #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 External Library Imports module                                                       #
# Consolidates many modules so that for library development you only have to import this module.  #
#                                                                                                 #
###################################################################################################

"""library development imports module"""

from .macal_library           import PLibrary
from .macal_interpreterconsts import FuncArg
from .macal_scope             import PScope
from .macal_function          import PFunction

from .macal_parsernodetypes   import VARIABLE
from .macal_variable_types    import ANY, ARRAY, BOOL, FLOAT, INT, PARAMS, RECORD, STRING
from .macal_keywords          import NIL

__all__ = ['PLibrary', 'FuncArg', 'PScope', 'PFunction', 'VARIABLE', 'ANY', 'ARRAY', 'BOOL', 
		   'FLOAT', 'INT', 'PARAMS', 'RECORD', 'STRING', 'NIL']

