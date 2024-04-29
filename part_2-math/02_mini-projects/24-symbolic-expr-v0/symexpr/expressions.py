"""
Python classes that represent symbolic Mathematical expressions.
"""


class Expression:
    """
    Base class for all symbolic expressions.
    """
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


class Variable(Expression):
    """
    Represents a single variable.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        """User friendly representation of the variable."""
        return self.name

    def __repr__(self):
        """Developer friendly representation of the variable."""
        return f"Variable({self.name})"


class Number(Expression):
    """
    Represents a single number.
    """

    def __init__(self, value: int | float):
        self.value = value

    def __str__(self):
        """User friendly representation of the number."""
        return str(self.value)

    def __repr__(self):
        """Developer friendly representation of the number."""
        return f"Number({self.value})"


class Negative(Expression):
    """
    Represents the negative of an expression.
    """

    def __init__(self, expr: Expression):
        self.expr = expr

    def __str__(self):
        """User friendly representation of the negative."""
        return f"-{self.expr}"

    def __repr__(self):
        """Developer friendly representation of the negative."""
        return f"Negative({repr(self.expr)})"


class Sum(Expression):
    """
    Represents the sum of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self):
        """User friendly representation of the sum."""
        return f"{self.left} + {self.right}"

    def __repr__(self):
        """Developer friendly representation of the sum."""
        return f"Sum({repr(self.left)}, {repr(self.right)})"


class Difference(Expression):
    """
    Represents the difference of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self):
        """User friendly representation of the difference."""
        return f"{self.left} - {self.right}"

    def __repr__(self):
        """Developer friendly representation of the difference."""
        return f"Difference({repr(self.left)}, {repr(self.right)})"


class Product(Expression):
    """
    Represents the product of two expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self):
        """User friendly representation of the product."""
        return f"{self.left} * {self.right}"

    def __repr__(self):
        """Developer friendly representation of the product."""
        return f"Product({repr(self.left)}, {repr(self.right)})"


class Quotient(Expression):
    """
    Represents the quotient of a numerator and a denominator.
    """

    def __init__(self, numerator: Expression, denominator: Expression):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        """User friendly representation of the quotient."""
        return f"{self.numerator} / {self.denominator}"

    def __repr__(self):
        """Developer friendly representation of the quotient."""
        return f"Quotient({repr(self.numerator)}, {repr(self.denominator)})"


class Power(Expression):
    """
    Represents the power of a base and an exponent.
    """

    def __init__(self, base: Expression, exponent: Expression):
        self.base = base
        self.exponent = exponent

    def __str__(self):
        """User friendly representation of the power."""
        return f"{self.base}^{self.exponent}"

    def __repr__(self):
        """Developer friendly representation of the power."""
        return f"Power({repr(self.base)}, {repr(self.exponent)})"


class Function(Expression):
    """
    Represents a named function.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        """User friendly representation of the function."""
        return self.name

    def __repr__(self):
        """Developer friendly representation of the function."""
        return f"Function({repr(self.name)})"


class Apply(Expression):
    """
    Represents the application of a function to an argument.
    """

    def __init__(self, function: Function, argument: Expression):
        self.function = function
        self.argument = argument

    def __str__(self):
        """User friendly representation of the application."""
        return f"{self.function}({self.argument})"

    def __repr__(self):
        """Developer friendly representation of the application."""
        return f"Apply({repr(self.function)}, {repr(self.argument)})"
