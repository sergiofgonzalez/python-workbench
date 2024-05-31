"""
Python classes that represent symbolic Mathematical expressions.
"""

import math
from abc import ABC, abstractmethod

_well_known_function_bindings = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "sqrt": math.sqrt,
}


class Expression(ABC):
    """
    Base class for all symbolic expressions.
    """

    @abstractmethod
    def evaluate(self, **bindings):
        """
        Evaluate the expression given the variable bindings.

        Args:
            bindings: A dictionary of variable bindings, which can be passed in
                as `x=2`, y=3`.

        Returns:
            The numerical result of evaluating the expression.
        """
        pass

    @abstractmethod
    def expand(self):
        """
        Expand the expression.

        Returns:
            An expanded expression.
        """
        pass

    @abstractmethod
    def _python_expr(self):
        """
        Return the Python expression that can be used to evaluate the
        expression.

        Returns:
            str: The Python expression.
        """
        pass

    def python_function(self, **bindings):
        """
        Return the result of evaluating the expression, as an alternative to
        evaluate.

        Returns:
            float: The numerical result of evaluating the expression.
        """
        global_vars = {"math": math}
        return eval(self._python_expr(), global_vars, bindings)

    @staticmethod
    def _to_number_if_needed(arg):
        if isinstance(arg, (int, float)):
            return Number(arg)
        return arg

    def __neg__(self):
        return Negative(self)

    def __add__(self, other):
        return Sum(self, Expression._to_number_if_needed(other))

    def __sub__(self, other):
        return Difference(self, Expression._to_number_if_needed(other))

    def __mul__(self, other):
        return Product(self, Expression._to_number_if_needed(other))

    def __truediv__(self, other):
        return Quotient(self, Expression._to_number_if_needed(other))

    def __pow__(self, other):
        return Power(self, Expression._to_number_if_needed(other))

    def __radd__(self, other):
        return Sum(Expression._to_number_if_needed(other), self)

    def __rsub__(self, other):
        return Difference(Expression._to_number_if_needed(other), self)

    def __rmul__(self, other):
        return Product(Expression._to_number_if_needed(other), self)

    def __rtruediv__(self, other):
        return Quotient(Expression._to_number_if_needed(other), self)

    @abstractmethod
    def latex(self):
        """
        Return the raw LaTeX representation of the expression, which does not
        include the $ delimiters.

        Returns:
            str: The raw LaTeX representation of the expression.
        """
        pass

    def _repr_latex_(self):
        """
        Return the LaTeX representation of the expression so that it can be
        rendered in Jupyter notebooks.

        Returns:
            str: The LaTeX representation of the expression including the $
            delimiters.
        """
        return f"$ {self.latex()} $"

    @abstractmethod
    def derivative(self, variable: str):
        """
        Return the derivative of the expression with respect to the given
        variable.

        Args:
            variable: The variable with respect to which the derivative is
                computed.

        Returns:
            The derivative of the expression.
        """
        pass

    @abstractmethod
    def substitute(self, var, expression):
        """
        Substitute all occurrences of the variable with the given expression.

        Args:
            var: The variable to be substituted.
            expression: The expression to substitute the variable with.

        Returns:
            The expression with the variable substituted.
        """
        pass


class Variable(Expression):
    """
    Represents a single variable.
    """

    def __init__(self, name: str):
        self.name = name

    def evaluate(self, **bindings):
        try:
            return bindings[self.name]
        except KeyError as e:
            raise KeyError(f"Variable {self.name!r} not bound.")

    def _python_expr(self):
        return self.name

    def expand(self) -> Expression:
        return self

    def __str__(self):
        """User friendly representation of the variable."""
        return self.name

    def __repr__(self):
        """Developer friendly representation of the variable."""
        return f"Variable({self.name})"

    def latex(self):
        return self.name

    def derivative(self, variable):
        if variable.name == self.name:
            return Number(1)
        return Number(0)

    def substitute(self, var, expression):
        if var.name == self.name:
            return expression
        return self


class Number(Expression):
    """
    Represents a single number.
    """

    def __init__(self, value: int | float):
        self.value = value

    def evaluate(self, **bindings):
        return self.value

    def _python_expr(self):
        return str(self.value)

    def expand(self) -> Expression:
        return self

    def __str__(self):
        """User friendly representation of the number."""
        return str(self.value)

    def __repr__(self):
        """Developer friendly representation of the number."""
        return f"Number({self.value})"

    def latex(self):
        return str(self.value)

    def derivative(self, variable: str):
        return Number(0)

    def substitute(self, var, expression):
        return self


class Negative(Expression):
    """
    Represents the negative of an expression.
    """

    def __init__(self, expr: Expression):
        self.expr = expr

    def evaluate(self, **bindings):
        return -1 * self.expr.evaluate(**bindings)

    def expand(self):
        return Negative(self.expr.expand())

    def _python_expr(self):
        return f"-({self.expr._python_expr()})"

    def __str__(self):
        """User friendly representation of the negative."""
        return f"-{self.expr}"

    def __repr__(self):
        """Developer friendly representation of the negative."""
        return f"Negative({repr(self.expr)})"

    def latex(self):
        return f"-{self.expr.latex()}"

    def derivative(self, variable: str):
        return Negative(self.expr.derivative(variable))

    def substitute(self, var, expression):
        return Negative(self.expr.substitute(var, expression))


class Sum(Expression):
    """
    Represents the sum of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, **bindings):
        return self.left.evaluate(**bindings) + self.right.evaluate(**bindings)

    def _python_expr(self):
        return f"({self.left._python_expr()}) + ({self.right._python_expr()})"

    def expand(self):
        return Sum(self.left.expand(), self.right.expand())

    def __str__(self):
        """User friendly representation of the sum."""
        return f"{self.left} + {self.right}"

    def __repr__(self):
        """Developer friendly representation of the sum."""
        return f"Sum({repr(self.left)}, {repr(self.right)})"

    def latex(self):
        return f"{self.left.latex()} + {self.right.latex()}"

    def derivative(self, variable: str):
        return Sum(
            self.left.derivative(variable), self.right.derivative(variable)
        )

    def substitute(self, var, new):
        return Sum(
            self.left.substitute(var, new), self.right.substitute(var, new)
        )


class Difference(Expression):
    """
    Represents the difference of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, **bindings):
        return self.left.evaluate(**bindings) - self.right.evaluate(**bindings)

    def expand(self):
        return Difference(self.left.expand(), self.right.expand())

    def _python_expr(self):
        return f"({self.left._python_expr()}) - ({self.right._python_expr()})"

    def __str__(self):
        """User friendly representation of the difference."""
        return f"{self.left} - {self.right}"

    def __repr__(self):
        """Developer friendly representation of the difference."""
        return f"Difference({repr(self.left)}, {repr(self.right)})"

    def latex(self):
        return f"{self.left.latex()} - {self.right.latex()}"

    def derivative(self, variable: str):
        return Difference(
            self.left.derivative(variable), self.right.derivative(variable)
        )

    def substitute(self, var, new):
        return Difference(
            self.left.substitute(var, new), self.right.substitute(var, new)
        )


class Product(Expression):
    """
    Represents the product of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, **bindings):
        return self.left.evaluate(**bindings) * self.right.evaluate(**bindings)

    def _python_expr(self):
        return f"({self.left._python_expr()}) * ({self.right._python_expr()})"

    def expand(self) -> Expression:
        expanded_left = self.left.expand()
        expanded_right = self.right.expand()
        # (a + b) * c = a * c + b * c
        if isinstance(expanded_left, Sum):
            return Sum(
                Product(expanded_left.left, expanded_right).expand(),
                Product(expanded_left.right, expanded_right).expand(),
            )
        # a * (b + c) = a * b + a * c
        elif isinstance(expanded_right, Sum):
            return Sum(
                Product(expanded_left, expanded_right.left).expand(),
                Product(expanded_left, expanded_right.right).expand(),
            )
        # a * b
        else:
            return Product(expanded_left, expanded_right)

    def __str__(self):
        """User friendly representation of the product."""
        return f"{self.left} * {self.right}"

    def __repr__(self):
        """Developer friendly representation of the product."""
        return f"Product({repr(self.left)}, {repr(self.right)})"

    def latex(self):
        return f"{self.left.latex()} \\cdot {self.right.latex()}"

    def derivative(self, variable):
        if isinstance(self.left, Number):
            return Product(self.left, self.right.derivative(variable))
        elif isinstance(self.right, Number):
            return Product(self.right, self.left.derivative(variable))
        elif isinstance(self.left, Variable) and self.left.name != variable.name:
            return Product(self.left, self.right.derivative(variable))
        elif isinstance(self.right, Variable) and self.right.name != variable.name:
            return Product(self.right, self.left.derivative(variable))
        else:
            return Sum(
                Product(self.left.derivative(variable), self.right),
                Product(self.left, self.right.derivative(variable)),
            )

    def substitute(self, var, new):
        return Product(
            self.left.substitute(var, new), self.right.substitute(var, new)
        )


class Quotient(Expression):
    """
    Represents the quotient of a numerator and a denominator.
    """

    def __init__(self, numerator: Expression, denominator: Expression):
        self.numerator = numerator
        self.denominator = denominator

    def evaluate(self, **bindings):
        return self.numerator.evaluate(**bindings) / self.denominator.evaluate(
            **bindings
        )

    def expand(self):
        return Quotient(self.numerator.expand(), self.denominator.expand())

    def _python_expr(self):
        return f"({self.numerator._python_expr()}) / ({self.denominator._python_expr()})"

    def __str__(self):
        """User friendly representation of the quotient."""
        return f"{self.numerator} / {self.denominator}"

    def __repr__(self):
        """Developer friendly representation of the quotient."""
        return f"Quotient({repr(self.numerator)}, {repr(self.denominator)})"

    def latex(self):
        return (
            f"\\frac{{{self.numerator.latex()}}}{{{self.denominator.latex()}}}"
        )

    def derivative(self, variable: str):
        return Product(
            self.numerator, Quotient(Number(1), self.denominator)
        ).derivative(variable)

    def substitute(self, var, new):
        return Quotient(
            self.numerator.substitute(var, new),
            self.denominator.substitute(var, new),
        )

class Power(Expression):
    """
    Represents the power of a base and an exponent.
    """

    def __init__(self, base: Expression, exponent: Expression):
        self.base = base
        self.exponent = exponent

    def evaluate(self, **bindings):
        return self.base.evaluate(**bindings) ** self.exponent.evaluate(
            **bindings
        )

    def _python_expr(self):
        return (
            f"({self.base._python_expr()}) ** ({self.exponent._python_expr()})"
        )

    def expand(self):
        return Power(self.base.expand(), self.exponent.expand())

    def __str__(self):
        """User friendly representation of the power."""
        return f"{self.base}^{self.exponent}"

    def __repr__(self):
        """Developer friendly representation of the power."""
        return f"Power({repr(self.base)}, {repr(self.exponent)})"

    def latex(self):
        return f"{self.base.latex()}^{{{self.exponent.latex()}}}"

    def derivative(self, variable: str):
        if isinstance(self.exponent, Number):
            power_rule = Product(
                Number(self.exponent.value),
                Power(self.base, Number(self.exponent.value - 1)),
            )
            return Product(power_rule, self.base.derivative(variable))
        elif isinstance(self.base, Number):
            exponential_rule = Product(
                Apply(Function("ln"), Number(self.base.value)),
            )
            return Product(exponential_rule, self.exponent.derivative(variable))
        else:
            raise NotImplementedError(
                "Can't calculate derivative of {str(self)}"
            )

    def substitute(self, var, new):
        return self

class Function:
    """
    Represents a named function. Note that this class is not part of the
    hierarchy of Expressions, as it doesn't require to evaluate or anything like
    that.

    It is used to type the first argument of an Apply expression.
    """

    def __init__(self, name: str):
        if name not in _well_known_function_bindings:
            raise ValueError(f"Unknown function {name!r}")
        self.name = name

    def __str__(self):
        """User friendly representation of the function."""
        return self.name

    def __repr__(self):
        """Developer friendly representation of the function."""
        return f"Function({repr(self.name)})"

    def latex(self):
        if self.name != "sqrt":
            return f"{self.name}"
        return "\\sqrt"


class Apply(Expression):
    """
    Represents the application of a function to an argument.
    """

    def __init__(self, function: Function, argument: Expression):
        self.function = function
        self.argument = argument

    def evaluate(self, **bindings):
        return _well_known_function_bindings[self.function.name](
            self.argument.evaluate(**bindings)
        )

    def _python_expr(self):
        return f"math.{self.function.name}({self.argument._python_expr()})"

    def expand(self):
        return Apply(self.function, self.argument.expand())

    def __str__(self):
        """User friendly representation of the application."""
        return f"{self.function}({self.argument})"

    def __repr__(self):
        """Developer friendly representation of the application."""
        return f"Apply({repr(self.function)}, {repr(self.argument)})"

    def latex(self):
        return f"{self.function.latex()}({{{self.argument.latex()}}})"

    def derivative(self, variable: str):
        if self.function.name in _well_known_derivatives:
            return Product(
                self.argument.derivative(variable),
                _well_known_derivatives[self.function.name].substitute(
                    _var, self.argument
                ),
            )
        raise NotImplementedError(
            f"Derivative of {self.function.name!r} not implemented."
        )

    def substitute(self, var, new):
        return Apply(self.function, self.argument.substitute(var, new))


_var = Variable("placeholder variable for derivatives")
_well_known_derivatives = {
    "sin": Apply(Function("cos"), _var),
    "cos": Negative(Apply(Function("sin"), _var)),
    "ln": Quotient(Number(1), _var),
    "sqrt": Quotient(Number(1), Product(Number(2), Apply(Function("sqrt"), _var))),
}
