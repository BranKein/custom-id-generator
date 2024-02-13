import time
from datetime import datetime
import math


def get_max_bit(num_of_bits: int) -> int:
    return -1 ^ (-1 << num_of_bits)


def get_mask(num_of_bits, num_of_left):
    return (2 ** num_of_bits - 1) << num_of_left


def get_year(custom_id: int) -> int:
    return custom_id & get_mask(CustomIdGenerator.YEAR_BIT, CustomIdGenerator.YEAR_LEFT)


def get_chat_room(custom_id: int) -> int:
    return custom_id & get_mask(CustomIdGenerator.CHAT_ROOM_ID_BIT, CustomIdGenerator.CHAT_ROOM_LEFT)


def get_timestamp(custom_id: int) -> datetime:
    mask = get_mask(CustomIdGenerator.TIMESTAMP_ID_BIT, CustomIdGenerator.TIMESTAMP_LEFT)
    stmp = CustomIdGenerator.START_STMP + (custom_id & mask) >> CustomIdGenerator.TIMESTAMP_LEFT
    return datetime.fromtimestamp(float(stmp) / 1000.0)


class CustomIdGenerator:
    START_STMP = 1707828242000

    SIGN_BIT = 1
    YEAR_BIT = 14
    CHAT_ROOM_ID_BIT = 40
    TIMESTAMP_ID_BIT = 51
    DATACENTER_ID_BIT = 5
    SERVER_ID_BIT = 5
    SEQUENCE_BIT = 12

    SERVER_LEFT = SEQUENCE_BIT
    DATACENTER_LEFT = SERVER_LEFT + SERVER_ID_BIT
    TIMESTAMP_LEFT = DATACENTER_LEFT + DATACENTER_ID_BIT
    CHAT_ROOM_LEFT = TIMESTAMP_LEFT + TIMESTAMP_ID_BIT
    YEAR_LEFT = CHAT_ROOM_LEFT + CHAT_ROOM_ID_BIT

    last_stamp = -1
    sequence = 0

    def __init__(self, datacenter_id, server_id):
        if datacenter_id > get_max_bit(self.DATACENTER_ID_BIT) or datacenter_id < 0:
            raise ValueError("Datacenter ID cannot be greater than MAX_DATACENTER_ID or less than 0")
        if server_id > get_max_bit(self.SERVER_ID_BIT) or server_id < 0:
            raise ValueError("Server ID cannot be greater than SERVER_ID or less than 0")

        self.datacenter_id = datacenter_id
        self.server_id = server_id

    def get_new_id(self, chat_room_id) -> int:
        instance_id = self.get_temporary_id()
        return self.get_full_id(instance_id, chat_room_id)

    def get_full_id(self, temporary_id, chat_room_id) -> int:
        if chat_room_id > get_max_bit(self.CHAT_ROOM_ID_BIT) or chat_room_id < 0:
            raise ValueError("Chat room ID cannot be greater than MAX_CHAT_ROOM_ID or less than 0")
        id_datetime = get_timestamp(temporary_id)
        year = id_datetime.year

        return (year << self.YEAR_LEFT
                | chat_room_id << self.CHAT_ROOM_LEFT
                | temporary_id)

    def get_temporary_id(self) -> int:
        return ((self.get_curr_stmp() - self.START_STMP) << self.TIMESTAMP_LEFT
                | self.datacenter_id << self.DATACENTER_LEFT
                | self.server_id << self.SERVER_LEFT
                | self.sequence)

    def get_curr_stmp(self):
        curr_stmp = self.get_next_stmp()
        if curr_stmp < self.last_stamp:
            raise RuntimeError("Clock moved backwards")

        if curr_stmp == self.last_stamp:
            self.sequence = (self.sequence + 1) & get_max_bit(self.SEQUENCE_BIT)
            if self.sequence == 0:
                curr_stmp = self.get_next_stmp()
        else:
            self.sequence = 0

        self.last_stamp = curr_stmp

    def get_next_stmp(self):
        stmp = math.floor(time.time() * 1000)
        while stmp <= self.last_stamp:
            stmp = math.floor(time.time() * 1000)
        return stmp


__all__ = ['CustomIdGenerator']
