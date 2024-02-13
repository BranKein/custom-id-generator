from abc import ABCMeta, abstractmethod
from custom_id import CustomIdGenerator


class DataAdder(metaclass=ABCMeta):
    @abstractmethod
    def get_new_id(self, chat_room_id) -> int:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class NumericDataAdder(DataAdder):
    def __init__(self):
        super().__init__()
        self.__name__ = 'Numeric Data Adder'

        self._index = 0

    def get_new_id(self, chat_room_id) -> int:
        new_id = self._index
        self._index += 1
        return new_id


class CustomIDDataAdder(DataAdder):
    def __init__(self, datacenter_id, server_id):
        super().__init__()
        self.__name__ = "Custom ID Data Adder"

        self.custom_id_generator = CustomIdGenerator(datacenter_id, server_id)

    def get_new_id(self, chat_room_id) -> int:
        return self.custom_id_generator.get_new_id(chat_room_id)


__all__ = ['DataAdder', 'CustomIDDataAdder', 'NumericDataAdder']
