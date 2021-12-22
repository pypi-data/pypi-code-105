import libcst
from libcst.codemod import VisitorBasedCodemodCommand

FUNC_TO_COMPARISON = {
    "assert_eq": libcst.Equal,
    "assert_is": libcst.Is,
    "assert_is_not": libcst.IsNot,
    "assert_in": libcst.In,
    "assert_not_in": libcst.NotIn,
    "assert_gt": libcst.GreaterThan,
    "assert_ge": libcst.GreaterThanEqual,
    "assert_lt": libcst.LessThan,
    "assert_le": libcst.LessThanEqual,
    "assert_ne": libcst.NotEqual,
}


class AssertsCommand(VisitorBasedCodemodCommand):

    DESCRIPTION: str = "Migrate away from qcore.asserts."

    def leave_Expr(
        self, original_node: libcst.Expr, updated_node: libcst.Expr
    ) -> libcst.CSTNode:
        call = updated_node.value
        if not isinstance(call, libcst.Call):
            return updated_node
        name = libcst.helpers.get_full_name_for_node(call)
        if name not in FUNC_TO_COMPARISON:
            return updated_node
        if len(call.args) != 2:
            return updated_node
        if any(arg.keyword is not None for arg in call.args):
            return updated_node
        test = libcst.Comparison(
            left=call.args[0].value,
            comparisons=[libcst.ComparisonTarget(FUNC_TO_COMPARISON[name](), call.args[1].value)]
        )
        assert_statement = libcst.Assert(test=test)
        return assert_statement
