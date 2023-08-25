# -*- coding: utf-8 -*-
import logging
from save_data import save_data_to_json
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

        # Get list of users
        users = client.get_users()
        save_data_to_json(users, "users.json")
        print("Users data saved successfully.")

        # Get list of posts with comments
        posts = client.get_posts_with_comments(page_size=10, page_limit=5)
        save_data_to_json(posts, "posts.json")
        print("Posts data saved successfully.")

    except error.UnknownApiProviderError as prov_err:
        logging.exception("Error connecting to the %s API", api_provider)
        print(f"Error connecting to the {api_provider} API:", str(prov_err))
    except error.InvalidTokenError as inv_token_err:
        logging.exception("Error connecting to the %s API", api_provider)
        print(f"Error connecting to the {api_provider} API:", str(inv_token_err))
    except error.MissingTokenError as miss_token_err:
        logging.exception("Error connecting to the %s API", api_provider)
        print(f"Error connecting to the {api_provider} API:", str(miss_token_err))
    except error.ServerDoesNotRespondError as resp_err:
        logging.exception("Error connecting to the %s API", api_provider)
        print(f"Error connecting to the {api_provider} API:", str(resp_err))


if __name__ == "__main__":
    main()
