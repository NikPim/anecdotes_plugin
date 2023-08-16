# -*- coding: utf-8 -*-
import logging
from save_data import save_data_to_json
from client_factory import APIClientFactory


def main():
    # Configure logging
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    try:
        # Create client instance and check the connection to the API
        api_provider = "Dummy"
        client = APIClientFactory.create_client(api_provider)
        print(f"Connection to {api_provider} API established successfully")

        try:
            # Get list of users
            users = client.get_users()
            save_data_to_json(users, "users.json")
            print("Users data saved successfully.")
        except Exception as err:
            logging.exception(f"Error fetching users from {api_provider}")
            print(f"Error fetching users from {api_provider}:", str(err))

        try:
            # Get list of posts with comments
            posts = client.get_posts_with_comments(page_size=10, page_limit=5)
            save_data_to_json(posts, "posts.json")
            print("Posts data saved successfully.")
        except Exception as err:
            logging.exception(f"Error fetching posts from {api_provider}")
            print(f"Error fetching posts from {api_provider}:", str(err))

    except Exception as err:
        logging.exception(f"Error connecting to the {api_provider} API")
        print(f"Error connecting to the {api_provider} API:", str(err))


if __name__ == "__main__":
    main()
