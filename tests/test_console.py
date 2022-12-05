#!/usr/bin/python3
"""
This module carries out test on the console.py module
using the unittest module
"""
from unittest import TestCase, mock
from console import HBNBCommand
from io import StringIO
import json
import os

class TestHBNBCommand_create(TestCase):
    """
    Test the create command on console.py
    """
    def setUp(self):
        self.sys_output = mock.patch('sys.stdout', new=StringIO())
        self.out = self.sys_output.start()

    def test_create_with_no_class(self):
        """
        Testing the create command with no class name
        """
        HBNBCommand().onecmd("create")
        output_string = "** class name missing **"
        self.assertEqual(output_string, self.out.getvalue().strip())

    def test_create_with_no_args(self):
        """
        Testing the create command with no args
        """
        data = None
        initial_length = 0
        if os.path.exists('file.json'):
            with open("file.json") as f:
                data = json.load(f)
            initial_length = len(data)
        HBNBCommand().onecmd("create State")
        with open("file.json") as f:
            data = json.load(f)
        self.assertEqual(len(data), initial_length + 1)
        test_key = f"State.{self.out.getvalue().strip()}"
        self.assertIsNotNone(data.get(test_key))

    def test_create_with_correct_args(self):
        """
        Testing create with the correct argument
        """
        data = None
        initial_length = 0
        if os.path.exists("file.json"):
            with open("file.json") as f:
                data = json.load(f)
            initial_length = len(data)
        HBNBCommand().onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
        with open("file.json") as f:
            data = json.load(f)
        self.assertEqual(len(data), initial_length + 1)
        test_key = f"Place.{self.out.getvalue().strip()}"
        self.assertIsNotNone(data.get(test_key))
        test_value = data.get(test_key)
        self.assertEqual(test_value.get("city_id"), "0001")
        self.assertEqual(test_value.get("user_id"), "0001")
        self.assertEqual(test_value.get("name"), "My little house")
        self.assertEqual(test_value.get("number_rooms"), 4)
        self.assertEqual(test_value.get("number_bathrooms"), 2)
        self.assertEqual(test_value.get("max_guest"), 10)
        self.assertEqual(test_value.get("price_by_night"), 300)
        self.assertEqual(test_value.get("latitude"), 37.773972)
        self.assertEqual(test_value.get("longitude"), -122.431297)

    def test_create_with_wrong_args(self):
        """
        Testing create with improperly formatted args
        """
        data = None
        initial_length = 0
        if os.path.exists("file.json"):
            with open("file.json") as f:
                data = json.load(f)
            initial_length = len(data)

        HBNBCommand().onecmd('create State name="San Francisco"')
        state_id = self.out.getvalue().strip()
        self.out.truncate(0)
        self.out.seek(0)
        HBNBCommand().onecmd("create Place name='My_House'")
        place_id = self.out.getvalue().strip()
        self.out.truncate(0)
        self.out.seek(0)
        HBNBCommand().onecmd("create Place price = 434")
        place_id2 = self.out.getvalue().strip()

        with open("file.json") as f:
            data = json.load(f)
        self.assertEqual(len(data), initial_length + 3)
        test_state_key = f"State.{state_id}"
        test_place_key = f"Place.{place_id}"
        test_place2_key = f"Place.{place_id2}"
        test_state_value = data.get(test_state_key)
        test_place_value = data.get(test_place_key)
        test_place2_value = data.get(test_place2_key)
        self.assertIsNotNone(test_state_value)
        self.assertIsNone(test_state_value.get("name"))
        self.assertIsNotNone(test_place_value)
        self.assertIsNone(test_place_value.get("name"))
        self.assertIsNotNone(test_place2_value)
        self.assertIsNone(test_place_value.get("price"))
        
