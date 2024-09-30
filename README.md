# Tweet Stats

This project analyzes tweets to extract insights such as the most active tweeting day, the maximum number of tweets by a single user, and popular hashtags. 

It can retrieve data directly from the Twitter API based on a specified number of days (example of implementation) or analyze a pre-existing dataset.

## Project Structure


``` bash
TweetStats
├── Dockerfile
├── README.md
├── data
│   ├── processed
│   │   ├── general_analysis_results.csv
│   │   └── user_specific_analysis_results.csv
│   └── raw
│       └── tweets.json
├── k8s
│   └── deployment.yaml
├── requirements.txt
└── src
    ├── analysis.py
    ├── data.py
    ├── get_data.py
    ├── main.py
    └── processing.py
```

## Requirements

- Python 3.11
- Docker (optional)
- Kubernetes (optional for deployment)
- Access to Twitter API credentials (optional for example)

## Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/derezendemagalhaes/TweetStats.git
cd TweetStats
```


2. **Environment Variables (Optional):**

In the `.env` file fill in the values with your Twitter API credentials.


3. **Install Dependencies:**

It's recommended to use a virtual environment, create a it by running:
```bash
python3.11 -m venv venv
```

Activate the Virtual Environment:

- On Windows, activate the virtual environment by running:
    ```bash
    venv\Scripts\activate
    ```
- On macOS and Linux, use:
    ```bash
    source venv/bin/activate
    ```
Once the virtual environment is activated, you can install your project dependencies (e.g., from a requirements.txt file) using pip:
```bash
pip install -r requirements.txt
```


## Running the Application

You can run the application in two modes:

1. **Default Mode:**

    Analyzes the data from `data/raw/tweets.json`.

    ```bash
    python src/main.py
    ```

2. **Default Mode (Makefile):**

    Alternatively run this mode using the Makefile to both install the virtual environment and run the script:
    ```bash
    brew install make
    make run
    ```

3. **Get data Mode (example):**

    Fetches recent tweets based on the specified number of days using the `--get-data` argument.
    ```bash
    python src/main.py --get-data <number of days>
    ```

## Docker Usage

To build and run the application using Docker:

```bash
docker build -t tweet-stats . docker run tweet-stats
```

## Deployment

The application can be deployed using Kubernetes:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl create job --from=cronjob/tweet-stats-cronjob tweet-stats-manual-$(date +%Y%m%d%H%M%S)
```

The cron job is scheduled to run every Monday at 8:00 AM.

## Continuous Integration

Check the `.gitlab-ci.yml` file for CI configurations including build, test, and deploy stages.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your proposed changes.
