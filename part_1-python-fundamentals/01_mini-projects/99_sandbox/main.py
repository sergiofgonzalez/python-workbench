class Task:
    def __new__(cls, *args):
        print(f">>> in __new__")
        obj = object.__new__(cls)
        print(f">>> in __new__: instance 0x{id(obj):x} allocated")
        return obj

    def __init__(self, title):
        print(f">>> in __init__ for instance 0x{id(self):x}")
        self.title = title

    def __del__(self):
        print(f">> in __del__ for instance 0x{id(self):x}")


task = Task("homework")
del task # force destruction

