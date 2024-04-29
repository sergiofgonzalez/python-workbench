"""
App entry point showing how to use symexpr package.
"""

from symexpr.expressions import (
    Apply,
    Difference,
    Expression,
    Function,
    Negative,
    Number,
    Power,
    Product,
    Quotient,
    Sum,
    Variable,
)
from symexpr.utils import distinct_variables

if __name__ == "__main__":
    # Create symbolic expressions
    print("Creating symbolic expressions...")
    print(repr(Number(2) * Variable("x")))
    print(repr(Number(2) * Variable("x") + Number(3)))
    print(repr(2 * Variable("x") + 3))

    # Getting distinct variables from an expression
    print("Getting distinct variables from an expression...")
    expr = Number(2) * Variable("x") + Number(3)
    print(distinct_variables(expr))
    expr = Sum(
        Product(Variable("y"), Variable("z")),
        Power(Variable("x"), Variable("z")),
    )
    print(distinct_variables(expr))

    expr = Negative(Apply(Function("sin"), Product(Number(2), Variable("x"))))
    print(distinct_variables(expr))

    # 2xy^3
    expr = Product(
        Number(2), Product(Variable("x"), Power(Variable("y"), Number(3)))
    )
    print(distinct_variables(expr))
