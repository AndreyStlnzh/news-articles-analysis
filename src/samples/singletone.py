class Singletone(object):
    _object = None

    def __new__(cls, *args, **kwargs):
        if cls._object is None:
            cls._object = super(Singletone, cls).__new__(cls)
            cls._object._init(*args, **kwargs)
        return cls._object

    def _init(self) -> None:
        super().__init__()


def main():
    pass


if __name__ == "__main__":
    main()
