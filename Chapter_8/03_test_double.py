from unittest.mock import Mock

# Create a mock object that records calls and can return preset values
mock_repo = Mock()
# Configure the response we want
mock_repo.get.return_value = some_task
# Call will return some_task
mock_repo.get(123)
# Verify the call happened exactly once
mock_repo.get.assert_called_once()

# Mocks track all interaction details
# Shows what arguments were passed
print(mock_repo.get.call_args)
# Shows how many times it was called
print(mock_repo.get.call_count)
