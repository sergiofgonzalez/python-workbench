"""
App entry point showing how to use symexpr package.
"""

import math

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
from symexpr.utils import (
    contains,
    contains_sum,
    distinct_functions,
    distinct_variables,
)

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

    # Evaluate an expression
    print("Evaluating an expression...")

    expr = Variable("x")
    print(expr.evaluate(x=2))

    expr = Number("7")
    print(expr.evaluate(x=2))

    expr = Product(Variable("x"), Variable("y"))
    print(expr.evaluate(x=2, y=5))

    expr = Apply(Function("sin"), Variable("x"))
    print(expr.evaluate(x=0))
    print(expr.evaluate(x=math.pi / 2))

    expr = Product(
        Sum(Product(Number(3), Power(Variable("x"), Number(2))), Variable("x")),
        Apply(Function("sin"), Variable("x")),
    )
    print(expr.evaluate(x=5))

    # Expand an expression

    ## Expanding a product (a + b)(y + z) should be ay + az + by + bz
    Y = Variable("y")
    Z = Variable("z")
    A = Variable("a")
    B = Variable("b")
    expr = Product(Sum(A, B), Sum(Y, Z))
    print(expr.expand())

    ## (3x^2 + x) sin(x) should be 3x^2 sin(x) + x sin(x)
    expr = Product(
        Sum(Product(Number(3), Power(Variable("x"), Number(2))), Variable("x")),
        Apply(Function("sin"), Variable("x")),
    )
    print(expr.expand())

    # Checking equality
    print("Checking equality...")
    expr1 = Variable("x")
    expr2 = Variable("x")
    print(expr1 == expr2)

    # Checking if an expression contains a variable
    print("Checking if an expression contains a variable...")
    expr = Number(2) * Variable("x") + Number(3)
    print(contains(expr, Variable("x")))

    expr = Number(3) + Number(2) * Variable("x")
    print(contains(expr, Variable("x")))

    expr = (Number(2) + Variable("y")) / Number(3)
    print(contains(expr, Variable("x")))

    # Obtaining distinct functions
    print("Obtaining distinct functions...")
    expr = Apply(Function("sin"), Variable("x"))
    print(distinct_functions(expr))

    expr = Apply(Function("sin"), Variable("x")) + Product(
        Apply(Function("sin"), Variable("x")),
        Apply(Function("cos"), Variable("x")),
    )
    print(distinct_functions(expr))

    expr = Apply(Function("sin"), Apply(Function("log"), Variable("x")))
    print(distinct_functions(expr))

    # Contains sum
    print("Checking if an expression contains a sum...")
    expr = Number(2) + Number(3)
    print(contains_sum(expr))

    expr = Product(
        Product(
            Product(Number(3), Power(Variable("x"), Number(2))), Variable("x")
        ),
        Apply(Function("sin"), Variable("x")),
    )
    print(contains_sum(expr))

    # python_function/_python_expr to evaluate an expression
    x = Variable("x")
    print(x._python_expr())
    print(x.python_function(x=2))
    print(x.python_function(x=55))

    i = Number(5)
    print(i._python_expr())
    print(i.python_function())

    expr = Negative(x)
    print(expr.python_function(x=55))

    expr = Sum(x, Number(3))
    print(expr.python_function(x=55))

    expr = Difference(x, Number(3))
    print(expr.python_function(x=55))

    expr = Product(x, Number(3))
    print(expr.python_function(x=5))

    expr = Quotient(x, Number(3))
    print(expr.python_function(x=15))

    expr = Power(x, Number(3))
    print(expr.python_function(x=2))

    expr = Apply(Function("sqrt"), x)
    print(expr.python_function(x=25))

    # Derivatives
    print("\nDerivatives...")

    expr = Number(5)
    print(expr.derivative(Variable("x")))

    expr = Variable("x")
    print(expr.derivative(Variable("x")))

    expr = Variable("a")
    print(expr.derivative(Variable("x")))

    # (x + c + 1)' = 1
    expr = Sum(Variable("x"), Sum(Variable("c"), Number(1)))
    print(expr.derivative(Variable("x")))

    # (c * x)' = c
    expr = Product(Variable("c"), Variable("x"))
    print(expr.derivative(Variable("x")))

    # (x^2)' = 2x
    expr = Power(Variable("x"), Number(2))
    print(expr.derivative(Variable("x")))

    # sin(x)' = cos(x)
    expr = Apply(Function("sin"), Variable("x"))
    print(expr.derivative(Variable("x")))

    # sin(x^2)' = 2x cos(x^2)
    expr = Apply(Function("sin"), Power(Variable("x"), Number(2)))
    print(expr.derivative(Variable("x")))

    # ((3x^2 + x) sin(x))' = 3x^2 cos(x) + 6x sin(x) + sin(x)
    expr = Product(
        Sum(
            Product(Number(3), Power(Variable("x"), Number(2))),
            Variable("x"),
        ),
        Apply(Function("sin"), Variable("x")),
    )
    print(expr.derivative(Variable("x")))

    # Exercise: simplifying the derivative of a product c * f(x)

    # case 1: c * x
    expr = Product(Variable("c"), Variable("x"))
    print(expr.derivative(Variable("x")))

    # case 2: x * c
    expr = Product(Variable("x"), Variable("c"))
    print(expr.derivative(Variable("x")))

    # case 2: 5 * x
    expr = Product(Number(5), Variable("x"))
    print(expr.derivative(Variable("x")))

    # case 3: x * 5
    expr = Product(Variable("x"), Number(5))
    print(expr.derivative(Variable("x")))


    # Exercise: supporting derivatives of square roots
    expr = Apply(Function("sqrt"), Variable("x"))
    print(expr.derivative(Variable("x")))