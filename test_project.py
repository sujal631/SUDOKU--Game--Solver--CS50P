import pytest
import os
import csv
import tempfile
from project import validate_name, format_time, write_to_csv, write_csv_header, append_to_csv, sort_rankings, rewrite_csv
from unittest.mock import patch
from operator import itemgetter


class MockBoard:
    """
    Class to represent a MockBoard for testing purposes.
    """

    def __init__(self, difficulty, wrong_inputs):
        """
        Initialize the MockBoard with a difficulty level and number of wrong inputs.
        """
        self.difficulty = difficulty
        self.wrong_inputs = wrong_inputs

    def calculate_score(self):
        """
        Calculate the score for the mock board. Always returns 110 for testing purposes.
        """
        return 110


@pytest.fixture
def temp_file():
    """
    Pytest fixture to create a temporary file for testing purposes.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield os.path.join(temp_dir, 'test.csv')


def test_validate_name():
    """
    Test function for validate_name. Checks validation of various usernames.
    """
    assert validate_name("JoshiDai") == True  # Valid name
    assert validate_name("Leo") == False  # Too short
    assert validate_name("Zoe##") == False  # Invalid characters
    assert validate_name("Leo1234") == True  # Valid name with numbers


def test_format_time():
    """
    Test function for format_time. Checks formatting of various time values.
    """
    assert format_time(125) == '2:5'
    assert format_time(159) == '2:39'
    assert format_time(3600) == '60:0'


def test_write_to_csv(temp_file):
    """
    Test function for write_to_csv. Checks if data is written correctly to the CSV file.
    """
    with patch('project.RANKING_FILE', new=temp_file):
        write_csv_header(temp_file)
        mock_board = MockBoard('MEDIUM', 0)
        write_to_csv('Sujal', mock_board, 159)
        with open(temp_file, 'r') as file:
            lines = file.readlines()
            assert lines[1].strip() == ',Sujal,MEDIUM,2:39,0,110'


def test_write_csv_header(temp_file):
    """
    Test function for write_csv_header. Checks if the header is correctly written to the CSV file.
    """
    write_csv_header(temp_file)
    with open(temp_file, 'r') as file:
        assert file.readline().strip(
        ) == 'Rank,Username,Difficulty,Time Taken,Wrong Inputs,Total Score'


def test_append_to_csv(temp_file):
    """
    Test function for append_to_csv. Checks if a new line is correctly appended to the CSV file.
    """
    write_csv_header(temp_file)
    append_to_csv(temp_file, {'Rank': '1', 'Username': 'TestUser', 'Difficulty': 'Easy',
                  'Time Taken': '5:0', 'Wrong Inputs': '0', 'Total Score': '100'})
    with open(temp_file, 'r') as file:
        lines = file.readlines()
        # Check if the appended line is correct
        assert lines[1].strip() == '1,TestUser,Easy,5:0,0,100'


def test_sort_rankings(temp_file):
    """
    Test function for sort_rankings. Checks if the rankings are correctly sorted by total score.
    """
    with patch('project.RANKING_FILE', new=temp_file):
        write_csv_header(temp_file)
        # Append some lines to the CSV file
        append_to_csv(temp_file, {'Rank': '2', 'Username': 'TestUser1', 'Difficulty': 'Easy',
                      'Time Taken': '5:0', 'Wrong Inputs': '0', 'Total Score': '100'})
        append_to_csv(temp_file, {'Rank': '1', 'Username': 'TestUser2', 'Difficulty': 'Hard',
                      'Time Taken': '10:0', 'Wrong Inputs': '0', 'Total Score': '200'})
        append_to_csv(temp_file, {'Rank': '3', 'Username': 'TestUser3', 'Difficulty': 'Medium',
                      'Time Taken': '7:30', 'Wrong Inputs': '1', 'Total Score': '150'})
        # Sort the rankings
        sort_rankings()

        with open(temp_file, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        assert sorted(data, key=itemgetter(
            'Total Score'), reverse=True) == data


def test_rewrite_csv(temp_file):
    """
    Test function for rewrite_csv. Checks if the CSV file is correctly overwritten with new data.
    """
    with patch('project.RANKING_FILE', new=temp_file):
        test_data = [
            {'Rank': '2', 'Username': 'TestUser1', 'Difficulty': 'Easy',
                'Time Taken': '5:0', 'Wrong Inputs': '0', 'Total Score': '100'},
            {'Rank': '1', 'Username': 'TestUser2', 'Difficulty': 'Hard',
                'Time Taken': '10:0', 'Wrong Inputs': '0', 'Total Score': '200'},
            {'Rank': '3', 'Username': 'TestUser3', 'Difficulty': 'Medium',
                'Time Taken': '7:30', 'Wrong Inputs': '1', 'Total Score': '150'}
        ]
        # Rewrite the CSV file with new
        rewrite_csv(test_data)

        with open(temp_file, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        assert data == test_data
