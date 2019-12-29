import logging

from day02_program_alarm import tests as day02tests
from day05_sunny_with_a_change_of_asteroids import tests as day05tests


intcode_logger = logging.getLogger("intcode")
intcode_logger.setLevel(logging.INFO)

if __name__ == "__main__":
    print("day02:")
    day02tests()
    print("day05:")
    day05tests()