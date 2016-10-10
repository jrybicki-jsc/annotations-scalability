
class executor:
    def __enter__(self):
        def empty_function(annotation):
            pass
        return (empty_function,) * 3

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


