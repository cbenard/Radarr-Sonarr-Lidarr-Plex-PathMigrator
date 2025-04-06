from settings import database_dict
import sqlite3

# Normalize the paths: replace backslashes with forward slashes
for db, path_dict in database_dict.items():
    new_dict = {}
    for new_path, old_paths in path_dict.items():
        new_old_paths = [path.replace("\\", "/") for path in old_paths]
        new_dict[new_path] = new_old_paths
    database_dict[db] = new_dict

# Define a function that replaces the old path with the new path
def update_path(old_path, old_to_new_paths):
    # Replace backslashes in the old path with forward slashes
    old_path = old_path.replace('\\', '/')
    print(f"Old path: {old_path}")  # Print the old path
    for new_path, old_paths in old_to_new_paths.items():
        for old_path_key in old_paths:
            if old_path_key in old_path:
                # Replace the old path with the new path
                updated_path = old_path.replace(old_path_key, new_path)
                # Print the updated path
                print(f"New path: {updated_path}")
                return updated_path
    # If the old path is not in the current path, return the original path
    return old_path

# Define a function that updates a specific column in a specific table
def update_table(sqlfile, table, column, old_to_new_paths):
    # Create a cursor object
    cursor = sqlfile.cursor()
    # Execute a SQL query that selects all data from the specified column of the specified table
    cursor.execute(f"SELECT {column} FROM {table}")
    # Fetch all rows returned by the query
    data = cursor.fetchall()
    # Iterate over each row
    for row in data:
        # Get the old path from the first element of the row
        oldPath = row[0]
        # Get the new path by calling the update_path function with the old path
        newPath = update_path(oldPath, old_to_new_paths)
        # If the new path is different from the old path
        if newPath != oldPath:
            # Print the new path
            print(newPath)
            # Execute a SQL query that updates the specified column of the specified table with the new path
            cursor.execute(f'UPDATE {table} SET {column} = ? WHERE {column} = ?', (newPath, oldPath))
            # Commit the changes to the database
            sqlfile.commit()

# Iterate over the dictionary of databases
for database, old_to_new_paths in database_dict.items():
    # Connect to the SQLite database file
    sqlfile = sqlite3.connect(database)
    # Call the update_table function with different table and column names based on the database
    if database == "radarr.db":
        update_table(sqlfile, 'Collections', 'RootFolderPath', old_to_new_paths)
        update_table(sqlfile, 'Movies', 'Path', old_to_new_paths)
        update_table(sqlfile, 'RootFolders', 'Path', old_to_new_paths)
    elif database == "sonarr.db":
        update_table(sqlfile, 'RootFolders', 'Path', old_to_new_paths)
        update_table(sqlfile, 'Series', 'Path', old_to_new_paths)
        update_table(sqlfile, 'EpisodeFiles', 'RelativePath', old_to_new_paths)
        update_table(sqlfile, 'ExtraFiles', 'RelativePath', old_to_new_paths)
        update_table(sqlfile, 'SubtitleFiles', 'RelativePath', old_to_new_paths)
    # Close the database connection after all updates are done
    sqlfile.close()

