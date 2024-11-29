# tests/interfaces/view_models/test_base.py
import dataclasses
import pytest
from todo_app.interfaces.view_models.base import ErrorViewModel, OperationResult


def test_error_view_model_creation():
    """Test creating an error view model."""
    error = ErrorViewModel(message="Test error", code="TEST_ERROR")
    assert error.message == "Test error"
    assert error.code == "TEST_ERROR"


def test_error_view_model_immutability():
    """Test that error view model is immutable."""
    error = ErrorViewModel(message="Test error", code="TEST_ERROR")
    with pytest.raises(dataclasses.FrozenInstanceError):
        error.message = "New message"


def test_operation_result_success():
    """Test creating a successful operation result."""
    data = {"key": "value"}
    result = OperationResult.succeed(data)

    assert result.is_success
    assert result.success == data
    with pytest.raises(ValueError):
        _ = result.error


def test_operation_result_failure():
    """Test creating a failed operation result."""
    error = ErrorViewModel(message="Failed", code="ERROR")
    result = OperationResult.fail(error.message, error.code)

    assert not result.is_success
    assert result.error.message == "Failed"
    assert result.error.code == "ERROR"
    with pytest.raises(ValueError):
        _ = result.success


def test_operation_result_invalid_creation():
    """Test that OperationResult cannot be created with both success and error."""
    with pytest.raises(ValueError):
        OperationResult(
            success={"key": "value"}, error=ErrorViewModel(message="Failed", code="ERROR")
        )


def test_operation_result_invalid_empty_creation():
    """Test that OperationResult cannot be created without success or error."""
    with pytest.raises(ValueError):
        OperationResult()
