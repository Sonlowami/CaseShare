import pytest
from unittest import mock
from datetime import datetime
from models.base_model import BaseModel

@pytest.fixture
def base_model():
    return BaseModel()

@mock.patch('models.db')
def test_save_success(mock_db, base_model):
    # Mock the necessary dependencies
    mock_session = mock_db.session
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    # Call the save() function
    result = base_model.save()

    # Assert that the necessary methods were called
    mock_session.add.assert_called_once_with(base_model)
    mock_session.commit.assert_called_once()

    # Assert the result
    assert result is True

@mock.patch('models.db')
def test_save_failure(mock_db, base_model):
    # Mock the necessary dependencies
    mock_session = mock_db.session
    mock_session.add.return_value = None
    mock_session.commit.side_effect = Exception('Database error')

    # Call the save() function
    result = base_model.save()

    # Assert that the necessary methods were called
    mock_session.add.assert_called_once_with(base_model)
    mock_session.commit.assert_called_once()

    # Assert the result
    assert result is False