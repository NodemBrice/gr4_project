import os
from backend import notes
import pytest

@pytest.fixture
def temp_store(tmp_path):
    original = notes.DATA_FILE
    notes.DATA_FILE = tmp_path / "notes.json"
    yield
    notes.DATA_FILE = original  # Restore

def test_notes_crud(temp_store):
    # Start empty
    assert notes.get_all_notes() == []
    
    n = notes.add_note("t1", "c1")
    assert n.id == 1
    assert notes.get_note(1).title == "t1"
    
    n2 = notes.add_note("t2", "c2")
    assert n2.id == 2
    
    updated = notes.update_note(1, "tt", "cc")
    assert updated and updated.title == "tt"
    
    assert notes.delete_note(1) is True
    assert notes.get_note(1) is None
    
    # Edge: update non-existent
    assert notes.update_note(999, "x", "y") is None
    
    # Edge: delete non-existent
    assert notes.delete_note(999) is False