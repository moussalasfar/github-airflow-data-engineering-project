import requests
import pandas as pd
import os

def run_github_etl():

    usernames = ['moussalasfar']  # Add more usernames as needed
    token = '' # your token

    headers = {'Authorization': f'token {token}'}
    
    # new data
    new_repos = []
    
    # Read existing repository IDs if the CSV exists
    existing_ids = set()
    if os.path.exists('repositories.csv'):
        existing_df = pd.read_csv('repositories.csv')
        existing_ids = set(existing_df['id'].astype(str))  # Ensure IDs are strings for comparison

    # Loop through each username
    for username in usernames:
        url = f'https://api.github.com/users/{username}/repos'
        
        # Fetch repositories from GitHub for the current user
        response = requests.get(url, headers=headers)
        repos = response.json()
        
        # Process each repository
        for repo in repos:
            repo_id = repo['id']
            # Check for duplication
            if str(repo_id) not in existing_ids:  # Compare as strings
                new_repo = {
                    'id': repo_id,
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'html_url': repo['html_url'],
                    'private': repo['private'],
                    'description': repo.get('description', ''),  # Handle missing descriptions
                    'created_at': repo['created_at'],
                    'stargazers_count': repo['stargazers_count']
                }
                new_repos.append(new_repo)

    # If there are new repositories, append to CSV
    if new_repos:
        new_df = pd.DataFrame(new_repos)
        new_df.to_csv('s3://moussa-airflow-bucket/repositories.csv', mode='a', header=not os.path.exists('repositories.csv'), index=False)


