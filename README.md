# Path Updater for Radarr, Sonarr, Lidarr, and Plex Databases

This Python script is designed to help you update paths in Radarr, Sonarr, Lidarr, and Plex SQLite databases. This can be especially useful
when moving your media files from Windows to Linux without breaking your database links. The script handles the databases for Radarr,
Sonarr, Lidarr, and Plex separately.

## How it Works

The script connects to your SQLite databases and replaces old media paths with new ones. This operation is performed on several tables in the databases where paths are stored, ensuring all links in the database point to the correct location after moving your media files.

## Setup

Copy or rename `settings.example.py` to `settings.py`

Modify `settings.py` to define your database names, and the corresponding old and new paths in the `database_dict` dictionary in the script. The structure of the dictionary is as follows:

```
database_dict = {
    "database_name_1": {
        "new_path_1": ["old_path_1", "old_path_2", "..."],
        "new_path_2": ["old_path_3", "old_path_4", "..."],
        ...
    },
    "database_name_2": {
        "new_path_1": ["old_path_1", "old_path_2", "..."],
        ...
    },
    ...
}
```

**Note** - Paths should be entered in the format that your operating system uses. However, the script will normalize all paths to use forward slashes (/) for consistency.

## Running the Script

Run the script from a directory containing `.db files` with Python:

```
python3 movarr.py
```

As the script runs, it will print out old paths and their corresponding new paths. If a new path is not the same as the old path, it will update the old path to the new path in the database and print the new path.

## Warnings

1. **This script directly updates your SQLite databases. It is highly recommended that you back up your databases before running this script.**

2. **Ensure that your new paths correctly point to the new locations of your media files before running the script.**
