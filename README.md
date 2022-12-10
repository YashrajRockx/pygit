# Simple implementation of Github API for python

## Usage

```python
import pygit

TOKEN = "Your token here"
USER = "yashrajrocx"          # Your username for the github account
REPO = "bombsquad_server"    # Repository Name
BRANCH = "main"              # Branch Name, default is `main`

# Create pygit object
git = pygit.Github(TOKEN, USER, REPO, BRANCH)

# READING FILE
# This will print the contents of the README file
# You can also read file inside folders, 
# just pass the path to the file
print(git.read("README.md"))

# DIRECTORY CONTENTS
# This will print the contents of the directory or 
# any specified folder if path is provided
print(git.listdir()))
>>> {"files": ["__init__.py", "README.md"], "directories": []}

# CREATING FILE
# This will create a file in testFolder
# and returns status code for the same
PATH = "testFolder/testFile.txt"
COMMIT = "Creating testFile"
DATA = "Hi, this is the content of file."
print(git.create(PATH, COMMIT, DATA))
>>> 201

# UPDATING FILE
# This will update a file in testFolder
# and returns status code for the same
PATH = "testFolder/testFile.txt"
COMMIT = "Updating testFile"
DATA = "Hi, this is the new content of file."
print(git.update(PATH, COMMIT, DATA))

# DELETING FILE
# This will delete a file in testFolder
# and returns status code for the same
PATH = "testFolder/testFile.txt"
COMMIT = "Updating testFile"
print(git.delete(PATH, COMMIT))
```
