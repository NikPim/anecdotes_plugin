# -*- coding: utf-8 -*-
import logging
from saving_data import JsonFileSaver
from client_factory import APIClientFactory
import error_classes as error


def main() -> None:
    # Configure logging
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    try:
        # Create client instance and check the connection to the API
        api_provider = "Dummy"
        client = APIClientFactory.create_client(api_provider)
        print(f"Connection to the {api_provider} API established successfully")

        json_saver = JsonFileSaver()

        # Get list of users
        users = client.get_users()
        json_saver.save(users, "users.json")
        print("Users data saved successfully.")

        # Get list of posts with comments
        posts = client.get_posts_with_comments(page_size=10, page_limit=5)
        json_saver.save(posts, "posts.json")
        print("Posts data saved successfully.")

    except (
        error.UnknownApiProviderError,
        error.InvalidTokenError,
        error.MissingTokenError,
        error.ServerDoesNotRespondError,
    ) as err:
        logging.exception("Error connecting to the %s API", api_provider)
        print(f"Error connecting to the {api_provider} API:", str(err))


if __name__ == "__main__":
    main()
