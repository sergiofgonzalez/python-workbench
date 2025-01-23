# Proxy pattern using object composition

The *subject* will be a simple `StackCalculator` class. The class provides methods for multiplication and division. We will want to *proxy* the instances of this class to enhance it by providing a different behavior for division, to return a "NaN" instead of raising an error when dividing by zero.

In practice, the example creates a `SafeCalculator` class that proxies the `divide()` method on the `StackCalculator` class to intercept the *divide by zero* situation.
