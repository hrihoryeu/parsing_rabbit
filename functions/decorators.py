def begin_finish(func):
    def wrapper():
        print(f' [x] method(function) {func.__name__} starts...')
        func()
        print(f' [x] method(function) {func.__name__} finished')
    return wrapper()
