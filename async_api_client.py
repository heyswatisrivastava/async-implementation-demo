

"""
This script demonstrates how to implement an async function to concurrently fetch data from multiple APIs,
with proper error handling and timeout mechanisms. It can be deployed as an AWS Lambda function.

Steps to run this script:
1. Ensure you have Python 3.7+ installed.
2. Install the required libraries using pip:
   pip install aiohttp
3. Run the script:
   python <script_name>.py
4. Follow the prompts to provide URLs either from a file or via manual input.
5. The script will fetch data from the provided URLs concurrently and print the results.

For AWS Lambda deployment:
1. Package the script and its dependencies.
2. Deploy the package to AWS Lambda.
3. Trigger the Lambda function with an event containing the 'urls' key and a list of URLs as its value.
"""

import aiohttp
import asyncio
import json


# Define the async function to fetch data from multiple APIs
async def fetch_data(session, url):
    """
    Fetch data from a given URL with error handling and timeout mechanisms.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The URL to fetch data from.

    Returns:
        dict or None: The JSON response from the URL, or None if an error occurred.
    """
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Request to {url} failed: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"Request to {url} timed out")
        return None


# Define the main async function to concurrently fetch data from multiple APIs
async def fetch_all_data(urls):
    """
    Concurrently fetch data from multiple URLs.

    Args:
        urls (list): A list of URLs to fetch data from.

    Returns:
        list: A list of JSON responses from the URLs.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        return await asyncio.gather(*tasks)


# AWS Lambda handler function
def lambda_handler(event, context):
    """
    AWS Lambda handler function to fetch data from multiple URLs.

    Args:
        event (dict): The event data containing the 'urls' key.
        context (object): The context object (not used).

    Returns:
        dict: The response containing the status code and the fetched data.
    """
    urls = event.get("urls", [])
    if not urls:
        return {"statusCode": 400, "body": json.dumps("No URLs provided")}

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all_data(urls))

    return {"statusCode": 200, "body": json.dumps(results)}


# Read URLs from a file or input
def read_urls():
    """
    Read URLs from a file or manual input.

    Returns:
        list: A list of URLs.
    """
    choice = input("Read URLs from (f)ile or (i)nput? ").strip().lower()
    if choice == "f":
        file_path = input("Enter the file path: ").strip()
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    elif choice == "i":
        urls = []
        print("Enter URLs (type 'done' to finish):")
        while True:
            url = input().strip()
            if url.lower() == "done":
                break
            urls.append(url)
    else:
        print("Invalid choice. Exiting with default added URLs.")
        # Add default URLs here
        # urls = []
        urls = [
            "https://api.example.com/data1",
            "https://api.example.com/data2",
            "https://api.example.com/data3",
        ]
    return urls


if __name__ == "__main__":
    urls = read_urls()
    if urls:
        event = {"urls": urls}
        context = {}
        print(lambda_handler(event, context))
    else:
        print("No URLs provided.")
