"""Demonstrating scope in Python OOP."""

module_var = "module variable: module_var"


def module_fn() -> str:
    """Module level function."""
    return "module level function: module_fn()"


class SuperClass:
    """SuperClass with an assorted set of vars and methods."""

    super_class_var = "superclass class variable: SuperClass.super_class_var"
    __private_super_class_var = "private superclass class variable: SuperClass.__private_super_class_var"

    def __init__(self) -> None:
        """Initializer for SuperClass instances."""
        self.super_instance_var = (
            "private superclass instance variable: self.super_instance_var"
        )
        self.__private_super_class_instance_var = "private superclass instance variable: self.__private_super_class_instance_var"

    def super_class_method(self) -> str:
        """Super class method."""
        return "superclass method: self.super_class_method()"

    def __private_super_class_method(self) -> str:
        """Private super class method."""
        return "private super class method: self.__private_super_class_method"


class SubClass(SuperClass):
    """Subclass demonstrating what is accesible from a class method."""

    class_var = "class variable: SubClass.class_var (or self.class_var)"
    __private_class_var = "private class variable: SubClass.__private_class_var (or self.__private_class_var)"

    def __init__(self) -> None:
        """Initializer for SubClass instances."""
        super().__init__()
        self.instance_var = "instance variable: self.instance_var"
        self.__private_instance_var = (
            "private instance variable: variable.self.__private_instance_var"
        )

    def __private_method(self) -> str:
        """Private subclass method."""
        return "private method: self.__private_method()"

    def method2(self) -> str:
        """Regular subclass method."""
        return "Regular subclass method: method2"

    def method(self, method_param="method parameter: method_param") -> None:  # noqa: ANN001
        """Regular instance method illustrating what is accessible and what's not."""
        local_var = "method local var: local_var"

        # self, the method parameter, and method local vars are accessible
        print("Local")
        print("Access local, global, and built-in namespaces directly")
        print("local namespace:", list(locals().keys()))
        print(method_param)
        print(local_var)
        print()

        print("Global")
        print("global namespace:", list(globals().keys()))
        print(module_var)
        print(module_fn())
        print(SuperClass.super_class_var)
        print(SubClass.class_var)
        print(SubClass.__private_class_var)
        # print(SuperClass.__private_super_class_var) # SuperClass has no such attribute
        print()

        print("Access to instance and superclass namespaces through self")
        print("Instance namespace:", self.__dict__)
        print(self.instance_var)
        print(self.__private_instance_var)
        print(self.super_instance_var)
        print()

        print("Class namespace:", SubClass.__dict__)
        print(self.method2())
