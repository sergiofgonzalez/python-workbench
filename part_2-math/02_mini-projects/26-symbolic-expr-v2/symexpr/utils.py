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


def contains(expression: Expression, variable: Variable):
    """
    Return True if the expression contains the variable.

    Args:
        expression (Expression): The expression to check.
        variable (Variable): The variable to check for.

    Returns:
        bool: True if the expression contains the variable, False otherwise.
    """
    if isinstance(expression, Variable):
        return expression.name == variable.name
    elif isinstance(expression, Number):
        return False
    elif isinstance(expression, Sum):
        return contains(expression.left, variable) or contains(
            expression.right, variable
        )
    elif isinstance(expression, Difference):
        return contains(expression.left, variable) or contains(
            expression.right, variable
        )
    elif isinstance(expression, Product):
        return contains(expression.left, variable) or contains(
            expression.right, variable
        )
    elif isinstance(expression, Quotient):
        return contains(expression.numerator, variable) or contains(
            expression.denominator, variable
        )
    elif isinstance(expression, Power):
        return contains(expression.base, variable) or contains(
            expression.exponent, variable
        )
    elif isinstance(expression, Negative):
        return contains(expression.expr, variable)
    elif isinstance(expression, Apply):
        return contains(expression.argument, variable)
    else:
        raise TypeError(f"Unknown expression type: {type(expression)}")


def distinct_functions(expr: Expression) -> set[str]:
    """
    Return the distinct functions in the expression.

    Args:
        expr (Expression):  The expression to find the distinct functions in.

    Returns
        set[str] The set of distinct functions in the expression.
    """
    if isinstance(expr, Apply):
        return set([expr.function.name]).union(
            distinct_functions(expr.argument)
        )
    elif isinstance(expr, Number):
        return set()
    elif isinstance(expr, Sum):
        return set().union(
            distinct_functions(expr.left), distinct_functions(expr.right)
        )
    elif isinstance(expr, Difference):
        return set().union(
            distinct_functions(expr.left), distinct_functions(expr.right)
        )
    elif isinstance(expr, Product):
        return set().union(
            distinct_functions(expr.left), distinct_functions(expr.right)
        )
    elif isinstance(expr, Quotient):
        return distinct_functions(expr.numerator).union(
            distinct_functions(expr.denominator)
        )
    elif isinstance(expr, Power):
        return distinct_functions(expr.base).union(
            distinct_functions(expr.exponent)
        )
    elif isinstance(expr, Negative):
        return distinct_functions(expr.expr)
    elif isinstance(expr, Variable):
        return set()
    else:
        raise TypeError(f"Unknown expression type: {type(expr)}")

def contains_sum(expr: Expression) -> bool:
    """
    Return True if the expression contains a sum.

    Args:
        expr (Expression): The expression to check.

    Returns:
        bool: True if the expression contains a sum, False otherwise.
    """
    if isinstance(expr, Sum):
        return True
    elif isinstance(expr, Difference):
        return contains_sum(expr.left) or contains_sum(expr.right)
    elif isinstance(expr, Product):
        return contains_sum(expr.left) or contains_sum(expr.right)
    elif isinstance(expr, Quotient):
        return contains_sum(expr.numerator) or contains_sum(expr.denominator)
    elif isinstance(expr, Power):
        return contains_sum(expr.base) or contains_sum(expr.exponent)
    elif isinstance(expr, Negative):
        return contains_sum(expr.expr)
    elif isinstance(expr, Apply):
        return contains_sum(expr.argument)
    else:
        return False