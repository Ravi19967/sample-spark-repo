import datetime
import unittest
from unittest.mock import MagicMock

import pandas as pd

from src.ETLInterface import ETLInterface
from src.main import Task1, Task2


class TestMain(unittest.TestCase):
    def test_interface_implementation(self):
        """
        Check if classes implement all abstract methods from ETLInterface
        """
        spark = MagicMock()
        try:
            Task1_instance = Task1(spark)
            Task2_instance = Task2(spark)
            assert isinstance(Task1_instance, ETLInterface) == True
            assert isinstance(Task2_instance, ETLInterface) == True
        except TypeError:
            assert False


if __name__ == "__main__":
    unittest.main()
