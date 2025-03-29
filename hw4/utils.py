import os

def create_artifacts_dir(dirname: str) -> str:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(cur_dir, "artifacts", dirname)
    os.makedirs(artifacts_dir, exist_ok=True)

    return artifacts_dir
