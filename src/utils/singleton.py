from functools import wraps


def singleton(cls):
    """
    装饰器实现
    :param cls:
    :return:
    """
    instances = dict()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        index = (tuple([id(arg) for arg in args]), tuple(kwargs.items()))

        try:
            return instances[index]
        except KeyError:
            return instances.setdefault(index, cls(*args, **kwargs))

    return wrapper


class SingletonMetaClass(type):
    """
    元类实现
    """
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._inst[cls]
