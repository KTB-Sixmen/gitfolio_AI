from github import Github
from app.config import settings

def fetch_github_info(username: str):
    g = Github(settings.github_token)
    user = g.get_user(username)
    repos = user.get_repos()
    return user, repos
    