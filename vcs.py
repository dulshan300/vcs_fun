import os
import hashlib
import pickle


def init_vcs():
    os.makedirs(".vcs_storage", exist_ok=True)
    print("VSC initialized.")


def snapshot(dir):
    snapshot_hash = hashlib.sha256()
    shanpshot_data = {"files": {}}

    for root, dirs, files in os.walk(dir):
        for file in files:
            if ".vcs_storage" in os.path.join(root, file):
                continue

            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                content = f.read()
                snapshot_hash.update(content)
                shanpshot_data["files"]["file_path"] = content

    hash_digest = snapshot_hash.hexdigest()
    shanpshot_data["file_list"] = list(shanpshot_data["files"].keys())

    with open(f".vcs_storage/{hash_digest}", "wb") as f:
        pickle.dump(shanpshot_data, f)

    print(f"Snapshot create with hash {hash_digest}")


if __name__ == "__main__":
    import sys

    command = sys.argv[1]
    if command == "init":
        init_vcs()
    elif command == "push":
        snapshot(".")
