# Netflix Shared House

This app is for updating the household in a Netflix family plan.

## Setup

1. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Recommendations

- It is recommended to create a new mailbox at a free domain (e.g., Gmail, Yahoo) specifically for Netflix-related emails.
- Set a rule in your main mailbox to forward all emails from Netflix to this new mailbox. This helps in organizing and managing Netflix-related communications more efficiently.

## Running with Docker

1. Build the Docker image:
    ```sh
    docker build -t netflix-shared-house .
    ```

2. Run the Docker container:
    ```sh
    docker run -d netflix-shared-house
    ```
