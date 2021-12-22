import re
import libcst
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor


class TesthelperCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Fixes test helper imports."

    def leave_Attribute(
        self, original_node: libcst.Attribute, updated_node: libcst.Attribute
    ) -> libcst.CSTNode:
        name = libcst.helpers.get_full_name_for_node(updated_node)
        if name is None:
            return updated_node
        match = re.match(r"^a\.([a-z_\.]+)\.tests\.([a-zA-Z_\d]+)$", name)
        if match:
            module_name = match.group(1)
            function_name = match.group(2)
            AddImportsVisitor.add_needed_import(
                self.context, f"a.{module_name}.tests", function_name
            )
            return libcst.Name(value=function_name)
        return updated_node
