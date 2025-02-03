# async-implementation-demo

This project demonstrates how to implement an async function to concurrently fetch data from multiple APIs, with proper error handling and timeout mechanisms. It can be deployed as an AWS Lambda function.

## Prerequisites

- Python 3.7+
- `aiohttp` library

## Installation

1. Ensure you have Python 3.7+ installed.
2. Install the required libraries using pip:

   ```sh
   pip install aiohttp

## Usage
1. Run the script:
    ```
    python async_api_client.py
    ```
2. Follow the prompts to provide URLs either from a file or via manual input.
3. The script will fetch data from the provided URLs concurrently and print the results.

## AWS Lambda Deployment
1. Package the script and its dependencies.
2. Deploy the package to AWS Lambda.
3. Trigger the Lambda function with an event containing the urls key and a list of URLs as its value.
## Example Event for AWS Lambda
```
{
  "urls": [
    "https://api.example.com/data1",
    "https://api.example.com/data2",
    "https://api.example.com/data3"
  ]
}
```
## Functions
    - fetch_data(session, url): Fetch data from a given URL with error handling and timeout mechanisms.
    - fetch_all_data(urls): Concurrently fetch data from multiple URLs.
    - lambda_handler(event, context): AWS Lambda handler function to fetch data from multiple URLs.
    - read_urls(): Read URLs from a file or manual input.

