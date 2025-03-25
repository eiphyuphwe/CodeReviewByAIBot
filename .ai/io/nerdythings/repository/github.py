# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

import requests
from repository.repository import Repository, RepositoryError

class GitHub(Repository):

    def __init__(self, token, repo_owner, repo_name, pull_number):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.pull_number = pull_number
        self.__header_accept_json = { "Authorization": f"Bearer {token}" }
        self.__header_authorization = { "Accept": "application/vnd.github+json" }
        self.__url_add_comment = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/comments"
        self.__url_add_issue = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pull_number}/comments"
        self.__url_get_diff = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}"

    def post_comment_to_line(self, text, commit_id, file_path, line):
        headers = self.__header_accept_json | self.__header_authorization
        body = {
            "body": text,
            "commit_id": commit_id,
            "path" : file_path,
            "position" : line,
            "side" : "RIGHT"
        }
        response = requests.post(self.__url_add_comment, json = body, headers = headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise RepositoryError(f"Error with line comment {response.status_code} : {response.text}")

    def post_comment_general(self, text):
        headers = self.__header_accept_json | self.__header_authorization
        body = {
            "body": text
        }
        response = requests.post(self.__url_add_issue, json = body, headers = headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise RepositoryError(f"Error with general comment {response.status_code} : {response.text}")

    def get_diff_from_github(self):
        headers = self.__header_accept_json | self.__header_authorization
        response = requests.get(self.__url_get_diff, headers=headers, params={"Accept": "application/vnd.github.v3.diff"})
        if response.status_code == 200:
            return response.text
        else:
            raise RepositoryError(f"Error getting diff from GitHub {response.status_code} : {response.text}")

    def get_line_number_from_diff(self, file_path, original_line_number):
                diff = self.get_diff_from_github()

                file_diff_start = diff.find(f"--- a/{file_path}")
                if file_diff_start == -1:
                    return None
                file_diff = diff[file_diff_start:]
                file_diff_end = file_diff.find("diff --git")
                if file_diff_end != -1:
                    file_diff = file_diff[:file_diff_end]

                lines = file_diff.splitlines()
                current_line_number = 0
                for line in lines:
                    if line.startswith("@@"):
                        match = re.search(r"-(\d+),(\d+) \+(\d+),(\d+)", line)
                        if match:
                            current_line_number = int(match.group(3))
                    elif line.startswith("+"):
                        if original_line_number == current_line_number:
                            return current_line_number
                        current_line_number += 1
                    elif line.startswith("-"):
                        pass
                    else:
                        if original_line_number == current_line_number:
                            return current_line_number
                        current_line_number += 1
                return None