# Singleton pattern

Illustrates how to implement the **Singleton** pattern in Python

## A reminder on `==` and `is`

`is` compares whether two objects are the same object (identity test). By contrast, `==` compares whether two objects have the same value.

For example, when checking an object against `None` you should use `is`, because `None` is a singleton object and you'd like to check if the memory address of your object and the memory address of `None` is the same.

> `is` should be used when you need to check if the memory address of two objects are the same. In particular, any comparison with `None` should be using `None`.

> `==` should be used when you need to check that the value of two objects are the same, even if they have different memory addresses.

You can override the `==` behavior in your classes by implementing the `__eq__()` magic method. If you don't implement the `__eq__()` method in your custom classes, `==` will fall back to `is`.