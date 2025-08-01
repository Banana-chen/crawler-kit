from enum import Enum
from os import getenv


class Topic(str, Enum):
    Test = "test"
    Pchome = "pchome"

    def __str__(self):
        return f"projects/{getenv('PROJECT_ID')}/topics/{self.value}"
