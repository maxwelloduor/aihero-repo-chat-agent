import ingest


def test_filter():
    doc = {"filename": "data-engineering-faq.md"}
    assert "data-engineering" in doc["filename"]


def test_index_creation():
    index = ingest.index_data(
        repo_owner="DataTalksClub", repo_name="faq", filter=lambda d: True
    )
    assert index is not None
