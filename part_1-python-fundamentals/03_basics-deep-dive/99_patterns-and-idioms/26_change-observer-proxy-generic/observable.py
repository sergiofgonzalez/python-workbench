"""Implementation of the Change Observer pattern in Python."""


class UninitializedAccessAttemptError(Exception):
    """Raised when attempting to access an attribute before initialization completed."""


class Observable:
    """Class that proxies access to an object attributes."""

    def __init__(self, target_object, observer) -> None:
        """Initialize an Observable instance."""
        super().__setattr__("_initialized", False)
        super().__setattr__("_target_object", target_object)
        super().__setattr__("_observer", observer)
        super().__setattr__("_initialized", True)

    def __setattr__(self, name: str, value: any):
        """Proxies access the setter of the property."""
        if not hasattr(self, "_initialized") or not self._initialized:
            return
        if hasattr(self._target_object, name):
            if value != self._target_object.__getattribute__(name):
                prev = self._target_object.__getattribute__(name)
                self._target_object.__setattr__(name, value)
                self._observer(name, prev, value)
        else:
            print(f"Intercepted write attempt to {name}: not defined on target")
            self.__setattr__(name, value)

    def __getattribute__(self, name: str) -> any:
        """Delegate to the underlying target for getters."""
        if not hasattr(super(), "_initialized") or not self._initialized:
            msg = f"Attempt to read {name} attribute"
            raise UninitializedAccessAttemptError(msg)
        if hasattr(self._target_object, name):
            return self._target_object.__getattribute__(name)
        print(f"Intercepted read attempt on {name}: not defined on target")
        return self.__getattribute__(name)


def create_observable(target_obj, observer) -> Observable:
    """Return a Change Observer object for the given target obj."""
    return Observable(target_obj, observer)
