import os
import hashlib
import pickle
import datetime

VCS_STORAGE = ".vcs_storage"
VCS_HISTRY = ".history"


def init_vcs():
    os.makedirs(VCS_STORAGE, exist_ok=True)
    # create the history file
    open(os.path.join(VCS_STORAGE, VCS_HISTRY), "a").close()
    print("VSC initialized.")


def snapshot(dir):

    import sys

    if len(sys.argv) < 3:
        print("comment required")
        return

    comment = sys.argv[2]

    snapshot_hash = hashlib.sha256()
    snapshot_data = {"files": {}, "comment": comment}

    for root, dirs, files in os.walk(dir, topdown=True):
        # escap vcs storage files
        if root.find(VCS_STORAGE) != -1:
            continue

        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                content = f.read()
                snapshot_hash.update(content)
                snapshot_data["files"][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_data["file_list"] = list(snapshot_data["files"].keys())

    with open(os.path.join(VCS_STORAGE, hash_digest), "wb") as f:
        pickle.dump(snapshot_data, f)

    # update history

    meta = {
        "time": datetime.datetime.now(datetime.timezone.utc).timestamp(),
        "hash": hash_digest,
        "comment": comment,
    }

    history_path = os.path.join(VCS_STORAGE, VCS_HISTRY)

    history_list = {}
    if os.path.exists(history_path) and os.path.getsize(history_path) > 0:
        with open(history_path, "rb") as f:
            history_list = pickle.load(f)

    # need to check if history list has the hash digits
    if hash_digest in history_list:
        print("nothing to push")
    else:
        history_list[hash_digest] = meta
        with open(history_path, "wb") as f:
            pickle.dump(history_list, f)

        print(f"Snapshot create with hash {hash_digest }")


def revert_to_snapshot(hash_digits):
    snapshot_path = os.path.join(VCS_STORAGE, hash_digits)
    # check if the file exist
    if not os.path.exists(snapshot_path):
        print("Snapshot does not exist")
        return

    with open(snapshot_path, "rb") as f:
        snapshot_data = pickle.load(f)

    for file_path, content in snapshot_data["files"].items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)

    # check new files added
    current_files = set()
    for root, dir, files in os.walk(".", topdown=True):
        if root.find(VCS_STORAGE) != -1:
            continue
        for file in files:
            current_files.add(os.path.join(root, file))

    snapshot_files = set(snapshot_data["file_list"])
    files_to_delete = current_files - snapshot_files

    for file_path in files_to_delete:
        os.remove(file_path)
        print(f"Remove {file_path}")

    print(f"Reverted to snapshot {hash_digits}")


def log():
    import json

    history_path = os.path.join(VCS_STORAGE, VCS_HISTRY)
    history_list = {}
    if os.path.exists(history_path) and os.path.getsize(history_path) > 0:
        with open(history_path, "rb") as f:
            history_list = pickle.load(f)

    for hash, item in history_list.items():
        timestamp = datetime.datetime.fromtimestamp(item["time"]).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
        print(f"commit {item['hash']}")
        print(f"Date:   {timestamp}")
        print()
        print(f"    {item['comment']}")
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("command required")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_vcs()
    elif command == "snapshot":
        snapshot(".")
    elif command == "revert":
        if len(sys.argv) >= 3:
            hash_digits = sys.argv[2]
            revert_to_snapshot(hash_digits)
        else:
            print("hash digits required")
    elif command == "log":
        log()
