def test_repository_automatically_creates_inbox(tmp_path):
    """Test that project repository maintains inbox project across instantiations."""
    # Arrange - Create initial repository and verify Inbox exists
    initial_repo = FileProjectRepository(tmp_path)
    initial_inbox = initial_repo.get_inbox()
    assert initial_inbox.name == "INBOX"
    assert initial_inbox.project_type == ProjectType.INBOX

    # Act - Create new repository instance pointing to same directory
    new_repo = FileProjectRepository(tmp_path)

    # Assert - New instance maintains same Inbox
    persisted_inbox = new_repo.get_inbox()
    assert persisted_inbox.id == initial_inbox.id
    assert persisted_inbox.project_type == ProjectType.INBOX
