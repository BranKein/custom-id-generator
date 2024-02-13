import struct
import time
from unittest import TestCase
from custom_id import CustomIdGenerator


class TestCustomIdGenerator(TestCase):
    def setUp(self):
        self.id_generator = CustomIdGenerator(12, 1)

    def test_get_temporary_id(self):
        start_ns_time = time.time_ns()
        temporary_id = self.id_generator.get_temporary_id()
        end_ns_time = time.time_ns()
        print("Time Taken is: " + str(end_ns_time - start_ns_time))
        print(bin(temporary_id))

    def test_get_temporary_id_100(self):
        start_ns_time = time.time_ns()
        for i in range(100):
            self.id_generator.get_temporary_id()
        end_ns_time = time.time_ns()
        print("Time Taken is: " + str(end_ns_time - start_ns_time))

    def test_get_new_id(self):
        new_id = self.id_generator.get_new_id(0)
        print(bin(new_id)[2:])

    def test_get_new_id_no_duplicate(self):
        id_list = []
        for i in range(10000):
            new_id = self.id_generator.get_new_id(0)
            if new_id in id_list:
                self.fail("duplicated id")
            id_list.append(new_id)

        self.fail()
