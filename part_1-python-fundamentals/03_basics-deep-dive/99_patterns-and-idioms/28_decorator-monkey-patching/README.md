# Decorator: using monkey patching for the implementation

In the example, we decorate the `StackCalculator` class that only features the `divive()` and `multiply()` operations with a new method `add()`. Also, the `divide()` method is intercepted to return `"NaN"` instead of raising an exception when a division by zero is attempted.