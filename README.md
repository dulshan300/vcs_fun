# Simple Python Version Control System (VCS)

This is a minimal version control system written in Python for educational purposes. It simulates some of the basic functionality of Git, such as initializing a repository, committing snapshots with comments, reverting to previous states, and viewing a log of changes.

## Features

- Initialize a simple VCS repository
- Create snapshots (commits) of your working directory
- Revert to any previous snapshot
- View commit history with timestamps and comments

## Getting Started

### Requirements

- Python 3.x

### Setup

Simply run the script using Python. No installation or external dependencies required.

## Commands

### `init`

Initializes the VCS repository in the current directory.

```bash
python vcs.py init
````

Creates a hidden folder named `.vcs_storage` to store version history and snapshot data.

---

### `snapshot <comment>`

Creates a snapshot (commit) of the current directory, excluding the VCS storage itself.

```bash
python vcs.py snapshot "Initial commit"
```

* Stores file content and a comment.
* Each snapshot is hashed using SHA-256.
* Automatically updates the history file.

---

### `revert <hash>`

Reverts the working directory to a previous snapshot using the snapshot's hash.

```bash
python vcs.py revert <snapshot_hash>
```

* Files not present in the snapshot will be deleted.
* Files in the snapshot will be restored.

---

### `log`

Displays the commit history, including hash, date, and comment.

```bash
python vcs.py log
```

---

## Notes

* All data is stored in `.vcs_storage/`, including snapshots and commit history (`.history`).
* This is a simplified tool for learning purposes and not meant for production use.
* Binary file content is stored using Python's `pickle` module.

## License

This project is for educational use only and does not include any licensing or warranties.


