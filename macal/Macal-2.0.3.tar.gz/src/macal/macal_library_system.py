#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_system.py                                                       #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 System Library                                                                        #
#                                                                                                 #
###################################################################################################

"""System library implementation"""

from .macal_library_external import *

class LibrarySystem(PLibrary):
    def __init__(self):
        super().__init__("system")
        self.RegisterFunction("console",          [FuncArg("arg", PARAMS)], self.Console)
        self.RegisterFunction("record_has_field", [FuncArg("rec", RECORD), FuncArg("fieldname", STRING)], self.RecordHasField)
        self.RegisterFunction("type",             [FuncArg("_var", VARIABLE)], self.Type)
        self.RegisterFunction("isString",         [FuncArg("_var", VARIABLE)], self.IsString)
        self.RegisterFunction("isInt",            [FuncArg("_var", VARIABLE)], self.IsInt)
        self.RegisterFunction("isFloat",          [FuncArg("_var", VARIABLE)], self.IsFloat)
        self.RegisterFunction("isBool",           [FuncArg("_var", VARIABLE)], self.IsBool)
        self.RegisterFunction("isRecord",         [FuncArg("_var", VARIABLE)], self.IsRecord)
        self.RegisterFunction("isArray",          [FuncArg("_var", VARIABLE)], self.IsArray)

    def Console(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        out_str = ""
        # Since the param is type any and we can have any number of them we just iterate over them.
        if len(params) > 0:
            if params[0].format:
                self.console_fmt(params)
                return
            for param in params:
                out_str = f"{out_str}{param.get_value()}"
            print(out_str)
        else:
            print()

    def console_fmt(self, args):
        fmt  = args[0].get_value()
        args = args[1:]
        if len(args) != fmt.count("{}"):
            raise Exception("Number of arguments mismatch with format string.")
        argv = []
        for arg in args:
            argv.append(arg.get_value())
        print(fmt.format(*argv))

    def RecordHasField(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        fieldname = self.GetParamValue(params, "fieldname")
        record = self.GetParamValue(params, "rec")
        result =  fieldname in record
        scope.SetReturnValue(result, BOOL)

    def Type(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type()
        scope.SetReturnValue(result, STRING)

    def IsString(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == STRING
        scope.SetReturnValue(result, BOOL)

    def IsInt(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == INT
        scope.SetReturnValue(result, BOOL)

    def IsFloat(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == FLOAT
        scope.SetReturnValue(result, BOOL)

    def IsBool(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == BOOL
        scope.SetReturnValue(result, BOOL)

    def IsRecord(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == RECORD
        scope.SetReturnValue(result, BOOL)

    def IsArray(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var, index = self.GetVariableFromParam(params, scope, "_var")
        if len(index) > 0:
            result = PScope.get_value_type(self.GetIndexedVariableValue(var, index))
        else:
            result = var.get_type() == ARRAY
        scope.SetReturnValue(result, BOOL)
    