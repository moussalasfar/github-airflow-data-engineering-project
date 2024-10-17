# Data Pipeline Project using Apache Airflow, AWS, and GitHub API

## Project Overview

This project involves building an automated data pipeline to extract, process, and store data from GitHub using Apache Airflow and AWS services. The pipeline extracts repository metadata for multiple users and stores it securely in an AWS S3 bucket.

## Technologies Used

- **GitHub API**: To extract repository metadata.
- **Apache Airflow**: For orchestrating and automating workflows.
- **AWS S3**: For storing the extracted data securely.
- **EC2 (Ubuntu)**: For running the Apache Airflow instance.

## Project Components

1. **GitHub API Integration**:
   - Utilized GitHub API to extract data such as commits, issues, and stars for profiles like `moussalasfar` and others.
   - Used secure access through GitHub tokens for authentication.

2. **Apache Airflow**:
   - Set up on an EC2 instance (Ubuntu) to manage the scheduling and execution of tasks.
   - Tasks include:
     - Extracting data from the GitHub API.
     - Processing the extracted data.
     - Uploading data to AWS S3.

3. **AWS S3 for Data Storage**:
   - Extracted data is stored in an S3 bucket named `moussa-airflow-bucket` in JSON format.
   - Configured IAM permissions (`s3:PutObject` and `s3:HeadObject`) to ensure secure access to the bucket.

## contact
For any questions or informations:
- **linkedin**:<a href="www.linkedin.com/in/moussa-lasfar-423793196" target="_blank">Moussa Lasfar</a><br>
- **Email**:`moussalasfar2000@gmail.com`
