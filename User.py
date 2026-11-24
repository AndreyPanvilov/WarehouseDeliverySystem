class User:
    def __init__(self, user_id: int, address_x: int, address_y: int):
        self.__user_id = user_id
        self.__address_x = address_x
        self.__address_y = address_y

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def address_x(self) -> int:
        return self.__address_x

    @property
    def address_y(self) -> int:
        return self.__address_y

    def __str__(self) -> str:
        return f"User(id={self.__user_id}, address=({self.__address_x}, {self.__address_y}))"