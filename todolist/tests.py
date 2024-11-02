import re
import unittest
import json
import os
from django.test import TestCase

def write_to_file(file_name, data):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f)
    except TypeError as err:
        raise err
    except IOError as err:
        raise err

def read_from_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError as err:
        raise err
    except IOError as err:
        raise err

test_data = {
    "pk": 1,
    "title": "Task 1",
    "author": "test author",
    "published_data": "2022-01-01",
    "publisher": 2,
    "price": 100,
    "discounted_price": 50,
    "is_bestseller": False,
    "is_banned": True,
    "genres": [1],
}

class TestFileOperations(TestCase):
    def setUp(self):
        """Prepare test data and create the test file before each test."""
        self.test_file = 'data.json'
        write_to_file(self.test_file, test_data)

    def tearDown(self):
        """Remove the test file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read_file(self):
        """Test writing and reading valid data."""
        read_data = read_from_file(self.test_file)

        # Check that all fields match expected types
        self.assertEqual(read_data['pk'], test_data['pk'])
        self.assertIsInstance(read_data['title'], str)
        self.assertIsInstance(read_data['author'], str)
        self.assertIsInstance(read_data['published_data'], str)
        self.assertIsInstance(read_data['publisher'], int)
        self.assertIsInstance(read_data['price'], int)
        self.assertIsInstance(read_data['discounted_price'], int)
        self.assertIsInstance(read_data['is_bestseller'], bool)
        self.assertIsInstance(read_data['is_banned'], bool)
        self.assertIsInstance(read_data['genres'], list)

    def test_write_and_read_empty_file(self):
        """Test writing and reading an empty dictionary."""
        empty_file = 'empty_file.json'
        write_to_file(empty_file, {})

        read_data = read_from_file(empty_file)
        self.assertEqual(read_data, {})

        os.remove(empty_file)  # Clean up after test

    def test_read_nonexistent_file(self):
        """Test reading from a nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            read_from_file('nonexistent_file.json')

    def test_write_bad_data_into_file(self):
        """Test writing invalid data."""
        with self.assertRaises(TypeError):
            write_to_file(self.test_file, 1)

class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.cleaned_text = None

    def clean_text(self):
        # Удаляем небуквенные символы и приводим к нижнему регистру
        self.cleaned_text = re.sub(r'[^a-zA-Z\s]', '', self.text).lower()

    def remove_stop_words(self, stop_words):
        if self.cleaned_text is None:
            self.clean_text()

        words = self.cleaned_text.split()
        filtered_words = [word for word in words if word not in stop_words]
        self.cleaned_text = ' '.join(filtered_words)

class TestTextProcessor(unittest.TestCase):
    def test_clean_text_removes_non_alpha(self):
        """Test that non-alphabetic characters are removed."""
        text = 'Hello, World!'
        processor = TextProcessor(text)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, 'hello world')

    def test_clean_text_lowercase(self):
        """Test that text is converted to lowercase."""
        text = 'HeLLo WoRLD!'
        processor = TextProcessor(text)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, 'hello world')

    def test_clean_text_empty_string(self):
        """Test that cleaning an empty string returns an empty string."""
        text = ''
        processor = TextProcessor(text)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, '')

    def test_clean_text_with_numbers(self):
        """Test that numbers are removed from text."""
        text = '123 ABC!!!'
        processor = TextProcessor(text)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, 'abc')

    def test_remove_stop_words(self):
        """Test that stop words are removed correctly."""
        text = 'this is a test'
        stop_words = ['this', 'is']
        processor = TextProcessor(text)
        processor.clean_text()
        processor.remove_stop_words(stop_words)
        self.assertEqual(processor.cleaned_text, 'a test')

    def test_remove_stop_words_no_clean(self):
        """Test that stop words are removed if clean_text is not called first."""
        text = 'Hello, World!'
        stop_words = ['world']
        processor = TextProcessor(text)
        processor.remove_stop_words(stop_words)  # clean_text will be called inside
        self.assertEqual(processor.cleaned_text, 'hello')

    def test_remove_stop_words_no_stop_words(self):
        """Test that text remains unchanged if there are no stop words."""
        text = 'Hello, World!'
        stop_words = ['test']
        processor = TextProcessor(text)
        processor.clean_text()  # Must call clean_text first
        processor.remove_stop_words(stop_words)
        self.assertEqual(processor.cleaned_text, 'hello world')

