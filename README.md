# Netflix Shared House

This app is for updating the household in a Netflix family plan.

## Netflix Shared House Automation

This project automates the process of updating the primary location for a Netflix shared house account.

### Prerequisites

*   Python 3.9
*   Chrome WebDriver
*   IMAP access to your email account
*   `.env` file with the following variables:
    *   `EMAIL_ADDRESS`
    *   `PASSWORD`
    *   `IMAP_SERVER`
    *   `IMAP_PORT`
    *   `SEARCH_CRITERIA`

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

4.  Configure the `.env` file with your email credentials and IMAP settings.

### Usage

Run the `main.py` script:

```bash
python3 src/main.py
```

## Recommendations

- It is recommended to create a new mailbox at a free domain (e.g., Gmail, Yahoo) specifically for Netflix-related emails.
- Set a rule in your main mailbox to forward all emails from Netflix to this new mailbox. This helps in organizing and managing Netflix-related communications more efficiently.

### Docker

To build and run the application using Docker:

1.  Build the Docker image:

    ```bash
    docker build -t netflix-automation .
    ```

2.  Run the Docker container:

    ```bash
    docker run netflix-automation
    ```

### Notes

*   Make sure the Chrome WebDriver is compatible with your Chrome browser version.
*   Enable IMAP access in your email account settings.
