import sys


class _const:

    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError(f"Can't rebind const({name})")
        self.__dict__[name] = value


sys.modules[__name__] = _const()
