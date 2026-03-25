import io
import zipfile
import requests
import frontmatter


def read_repo_data(
    repo_owner,
    repo_name,
    branch="main",
    include_extensions=(".md", ".mdx"),
    include_paths=None,          # e.g. ["_questions/"]
    exclude_hidden=True,
    timeout=30
):
    """
    Download and parse markdown files from a GitHub repository.

    Args:
        repo_owner (str): GitHub username or org
        repo_name (str): Repository name
        branch (str): Branch name (default: main)
        include_extensions (tuple): File extensions to include
        include_paths (list or None): Only include files containing these paths
        exclude_hidden (bool): Skip hidden/system directories
        timeout (int): HTTP timeout

    Returns:
        List[dict]: Cleaned documents ready for downstream processing
    """

    prefix = "https://codeload.github.com"
    url = f"{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/{branch}"

    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename
        filename_lower = filename.lower()

        # 1. Extension filter
        if not filename_lower.endswith(include_extensions):
            continue

        # 2. Skip hidden/system dirs
        if exclude_hidden and any(part.startswith('.') for part in filename.split('/')):
            continue

        # 3. Path filtering (important for FAQ repo)
        if include_paths:
            if not any(p in filename_lower for p in include_paths):
                continue

        try:
            with zf.open(file_info) as f_in:
                content = f_in.read().decode("utf-8", errors="ignore")

                post = frontmatter.loads(content)
                data = post.to_dict()

                # Skip empty or useless docs
                if not data and not content.strip():
                    continue

                # --- Normalize structure (IMPORTANT for AI later) ---
                document = {
                    "id": data.get("id"),
                    "title": data.get("title") or data.get("question"),
                    "content": data.get("content", content),
                    "metadata": {
                        k: v for k, v in data.items()
                        if k not in ["content", "title", "question"]
                    },
                    "source": filename
                }

                repository_data.append(document)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    zf.close()
    return repository_data