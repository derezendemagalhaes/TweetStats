import argparse
import logging

from data import load_data, get_tweets
from processing import preprocess_data
from analysis import analyze_data

logging.basicConfig(level=logging.INFO)


def main(args):
    """
    Main function to orchestrate the fetching, processing, and analyzing of tweet data.

    Args:
        args (argparse.Namespace): Command-line arguments parsed by argparse.
            - args.get_data (int, optional): Specifies the number of days to fetch tweets from. If provided,
              tweets from the last `args.get_data` days are fetched and processed. Otherwise, tweets from
              a default JSON file are processed.

    Side Effects:
        - Gets tweets and saves them to 'tweets_api.json' if `args.get_data` is provided.
        - Reads from either 'tweets_api.json' or a default file based on the presence of `args.get_data`.
        - Processes and analyzes the tweet data.
        - Saves the analysis results to CSV files.
        - Logs the completion of data fetching, processing, and analysis steps.
    """
    if args.get_data is not None:
        days = args.get_data
        get_tweets(days)
        logging.info(f"Data for the last {days} days fetched and saved to 'tweets_api.json'.")
        tweets = load_data('tweets_api.json')
    else:
        tweets = load_data('data/raw/tweets.json')

    processed_tweets = preprocess_data(tweets)
    general_results, user_results = analyze_data(processed_tweets)

    output_dir = 'data/processed'
    logging.info("Starting to save analysis results.")
    general_results.to_csv(f'{output_dir}/general_analysis_results.csv', index=False)
    logging.info(f"General results saved to {output_dir}/general_analysis_results.csv.")
    user_results.to_csv(f'{output_dir}/user_specific_analysis_results.csv')
    logging.info(f"User-specific results saved to {output_dir}/user_specific_analysis_results.csv.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tweet Stats")
    parser.add_argument('--get-data', type=int, help='Get data from the last n days', nargs='?', const=7)
    args = parser.parse_args()
    main(args)
