import json
import base64
import requests


class Github:
    def __init__(self, token: str, user: str, repo: str, branch: str = "main") -> None:
        """Simple github interaction for python

        Args:
            token: Github token string
            user: Username of the account
            repo: Repository name
            branch: Branch name, the default will be `main`
        """

        self.user = user
        self.repo = repo
        self.token = token
        self.branch = branch

    def _sha(self, path: str = "") -> str:
        """Helper method for updating files"""

        response = requests.get(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            headers={"accept": "application/vnd.github+json"},
            auth=(self.user, self.TOKEN),
        )
        return response.json()["sha"]

    def _parse_data(self, data):
        if isinstance(data, (tuple, list, dict)):
            return json.dumps(data, escape_forward_slashes=False).encode()
        else:
            return str(data)

    def read(self, path: str = "") -> str:
        """Method for reading anyfile from repo

        Args:
            path: Path of the file to be read

        Returns:
            str: Contents of the file
        """

        response = requests.get(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            headers={"accept": "application/vnd.github+json"},
            auth=(self.user, self.TOKEN),
        )

        return base64.b64decode(response.json()["content"]).decode()

    def listdir(self, path: str = "") -> dict:
        """Method to get all files and directories of a specific folder

        Args:
            path: Path to the folder

        Returns:
            dict: All files and directories arranged in `{"files": [], "directories": []}` format
        """

        dumb = {"files": [], "directories": []}
        response = requests.get(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            headers={"accept": "application/vnd.github+json"},
            auth=(self.user, self.TOKEN),
        ).json()

        for i in response:
            if i["type"] == "dir":
                dumb["directories"].append(i["name"])
            elif i["type"] == "file":
                dumb["files"].append(i["name"])

        return dumb

    def update(self, path: str, commit: str, data) -> int:
        """Method to update a file of a specific directory

        Args:
            path: The path to the file to be updated
            commit: Commit message to commit
            data: New data to be updated

        Returns:
            int: Status code of the operation
        """

        response = requests.put(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            auth=(self.user, self.TOKEN),
            json={
                "branch": self.branch,
                "message": commit,
                "sha": self._sha(path),
                "content": base64.b64encode(self._parse_data(data)).decode(),
            },
        )
        return response.status_code

    def create(self, path: str, commit: str, data) -> int:
        """Method to create a new file

        Args:
            path: Path where the new file will be created
            commit: Commit message to commit
            data: New data to be updated

        Returns:
            int: Status code of the operation
        """

        response = requests.put(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            auth=(self.user, self.TOKEN),
            json={
                "branch": self.branch,
                "message": commit,
                "content": base64.b64encode(self._parse_data(data)).decode(),
            },
        )
        return response.status_code

    def delete(self, path: str, commit: str) -> int:
        """Method to create a new file

        Args:
            path: Path where the new file will be created
            commit: Commit message to commit
            data: New data to be updated

        Returns:
            int: Status code of the operation
        """

        response = requests.delete(
            f"https://api.github.com/repos/{self.user}/{self.repo}/contents/{path}",
            auth=(self.user, self.TOKEN),
            json={"branch": self.branch, "message": commit, "sha": self._sha(path)},
        )
        return response.status_code
