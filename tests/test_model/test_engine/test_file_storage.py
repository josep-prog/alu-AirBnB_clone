#!/usr/bin/python3
"""
Unit tests for FileStorage class
"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.model = BaseModel()
        self.storage.new(self.model)

    def test_all(self):
        """Test all() method"""
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)
        self.assertGreaterEqual(len(objects), 1)

    # Add more test methods...


if __name__ == '__main__':
    unittest.main()
