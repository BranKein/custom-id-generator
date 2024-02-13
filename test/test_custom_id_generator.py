from unittest import TestCase
from data_adder.custom_id_generator import CustomIdGenerator


class TestCustomIDDataAdder(TestCase):
    def setUp(self):
        self.id_generator = CustomIdGenerator()

    def test_get_new_id(self):
        id_list = []
        for i in range(10000):
            new_id = self.id_generator.get_new_id(0)
            if new_id in id_list:
                self.fail("duplicated id")
            id_list.append(new_id)

        self.fail()
