"""Utility functions for symbolic expressions."""

from symexpr.expressions import (
    Apply,
    Difference,
    Expression,
    Negative,
    Number,
    Power,
    Product,
    Quotient,
    Sum,
    Variable,
)


def distinct_variables(expr: Expression) -> set[str]:
    """
    Return the distinct variables in the expression.

    Args:
        expr (Expression):  The expression to find the distinct variables in.

    Returns
        set[str] The set of distinct variables in the expression.
    """
    # Leaves are either variables or numbers, so we can just return a set
    # in those cases.
    # Then, in the combinators, we can just use recursion to keep collecting the
    # variables.
    if isinstance(expr, Variable):
        return set(expr.name)
    elif isinstance(expr, Number):
        return set()
    elif isinstance(expr, Sum):
        return set().union(
            distinct_variables(expr.left), distinct_variables(expr.right)
        )
    elif isinstance(expr, Difference):
        return set().union(
            distinct_variables(expr.left), distinct_variables(expr.right)
        )
    elif isinstance(expr, Product):
        return set().union(
            distinct_variables(expr.left), distinct_variables(expr.right)
        )
    elif isinstance(expr, Quotient):
        return distinct_variables(expr.numerator).union(
            distinct_variables(expr.denominator)
        )
    elif isinstance(expr, Power):
        return distinct_variables(expr.base).union(
            distinct_variables(expr.exponent)
        )
    elif isinstance(expr, Negative):
        return distinct_variables(expr.expr)
    elif isinstance(expr, Apply):
        return distinct_variables(expr.argument)
    else:
        raise TypeError(f"Unknown expression type: {type(expr)}")
