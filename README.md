# Archive Manager

Archive Manager is a Python tool designed to help users interact with and manage large archives of files efficiently. 
Whether you need to sort files, find duplicates, perform equality checks, or remove unnecessary files, this tool 
provides the necessary functionalities to streamline your file management tasks.

Core concepts and explanation:
- Archyves are wrappers for built in generators that enable the user to loop through directories revursively.
- To represent each item that the archyve finds, we have Entry objects - these are wrappers for Path objects that enable some useful features like hashing, sorting etc.

## Features

- **Sorting:** Organize your files based on various criteria such as file type, size, date modified, etc.
- **Duplicate Finding:** Identify and manage duplicate files to free up storage space.
- **Equality Checking:** Compare files to ensure they are identical or different.
- **Removal Tools:** Safely remove unwanted files from your archives.

## Installation
```bash
pip install archyve
```
   

## Examples

Below are some examples of how to use archyve.

1. Find duplicates in a large library of images:
   
   ```python
   from archyve import Archyve, Entry
   
   # Create an archyve
   archyve: Archyve = Archyve(r"<put your path(s) here>")

   # Get a list of all the duplicate images and videos
   archyve = archyve.images + archyve.videos
   duplicate_lists: list[list[Entry]] = archyve.duplicates()
   
   # Sort the duplicates by age
   for i in range(len(duplicate_lists)):
       duplicate_lists[i] = sorted(duplicate_lists[i], key=lambda e: e.created)
   
   # Delete the ones that are not the oldest
   delete: list[list[Entry]] = [duplicate_list[1:] for duplicate_list in duplicate_lists]
   for entry_list in delete:
       archyve.delete(entry_list)
   ```

2. Get a list of all non-text files recursively in a given directory:
   
   ```python
   from archyve import Archyve, EntryType
   
   # Create an archyve
   archyve: Archyve = Archyve(r"p1", r"p2")
   
   # Filter the archyve entries on whatever you need
   archyve = archyve.filter(lambda e: not e.is_type(EntryType.TEXT))
   
   # Loop through the archyve and print the entries
   for entry in archyve:
      print(entry)
   ```