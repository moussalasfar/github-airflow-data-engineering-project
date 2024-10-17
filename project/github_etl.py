import requests
import pandas as pd
import os
import boto3
from botocore.exceptions import NoCredentialsError

def run_github_etl():
    usernames = ['moussalasfar']  # Add more usernames as needed
    token = ''  # Your token

    headers = {'Authorization': f'token {token}'}
    
    # Prepare for new data
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

        # Data Transformations
        # 1. Rename columns if necessary
        new_df.rename(columns={
            'id': 'repository_id',
            'name': 'repository_name',
            'full_name': 'repository_full_name',
            'html_url': 'repository_url',
            'private': 'is_private',
            'description': 'repo_description',
            'created_at': 'created_date',
            'stargazers_count': 'stars'
        }, inplace=True)

        # 2. Convert 'created_date' to datetime
        new_df['created_date'] = pd.to_datetime(new_df['created_date'])

        # 3. Filter out any repositories that are private
        new_df = new_df[new_df['is_private'] == False]

        # Save the transformed DataFrame to CSV
        new_df.to_csv('repositories.csv', mode='a', header=not os.path.exists('repositories.csv'), index=False)

        # Upload the CSV file to S3
        s3_bucket = 'moussa-airflow-bucket'
        s3_key = 'repositories.csv'
        
        s3_client = boto3.client('s3')

        try:
            s3_client.upload_file('repositories.csv', s3_bucket, s3_key)
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")


