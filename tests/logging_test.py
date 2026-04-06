import importlib
import logs
from datetime import datetime
from unittest.mock import MagicMock


def test_logging(tmp_path, monkeypatch):
    # 1. Setup Environment
    monkeypatch.setenv("LOGS_DIRECTORY", str(tmp_path))
    importlib.reload(logs)

    # 2. Create Mock Agent
    mock_agent = MagicMock()
    mock_agent.name = "test_agent"
    mock_agent.toolsets = []
    mock_agent._instructions = "test"
    mock_agent.model.system = "test"
    mock_agent.model.model_name = "test"

    # 3. Use a dictionary that matches the expected output of dump_python
    # This avoids the "UserPrompt" vs "UserPromptNode" vs "TextPart" import headache
    messages = [
        {
            "role": "user",
            "content": "hi",
            "timestamp": datetime.now(),  # This fixes the 'strftime' error
        }
    ]

    # 4. Mock the TypeAdapter so it doesn't try to validate our manual dict
    # We want to test your logging logic, not Pydantic's internals
    monkeypatch.setattr("logs.ModelMessagesTypeAdapter.dump_python", lambda x: x)

    # 5. Run the function
    returned_path = logs.log_interaction_to_file(mock_agent, messages)

    # 6. Verify
    assert returned_path.exists()
    assert returned_path.parent == tmp_path
