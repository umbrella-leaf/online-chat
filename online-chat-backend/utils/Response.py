class Response:
    def __init__(self, status, data, message):
        self.status = status
        self.data = data
        self.message = message

    def to_dict(self):
        return self.__dict__


class Success(Response):
    def __init__(self, data=None, message=None):
        status = 200
        super().__init__(status, data, message)


class Warn(Response):
    def __init__(self, data=None, message=None):
        status = 300
        super().__init__(status, data, message)


class Error(Response):
    error = None

    def __init__(self, data=None, message=None):
        status = 400
        super().__init__(status, data, message)


Error.error = Error(message='连接错误！')


if __name__ == '__main__':
    print(Error.error.to_dict())
