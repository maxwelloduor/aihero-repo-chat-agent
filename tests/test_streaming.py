def test_stream_delta_logic():
    chunks = ["Hello", "Hello world", "Hello world again"]

    last_len = 0
    outputs = []

    for chunk in chunks:
        new_text = chunk[last_len:]
        last_len = len(chunk)
        outputs.append(new_text)

    assert outputs == ["Hello", " world", " again"]
