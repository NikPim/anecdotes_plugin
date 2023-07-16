import logging
from config import read_config
from dummy_api_client import DummyAPIClient
from save_data import save_data_to_json


def main():
    config = read_config()
    token = config.get("API", "token")

    service_url = "https://dummyapi.io/data/v1/"
    access_token = token

    # Configure logging
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    try:
        #Create client instance and check the connection to the API
        client = DummyAPIClient(service_url, access_token)
        print("Connection to the API established successfully.")

        try:
            # Get list of users
            users = client.get_users()
            save_data_to_json(users, "users.json")
            print("Users data saved successfully.")
        except Exception as err:
            logging.exception("Error fetching users")
            print("Error fetching users:", str(err))

        try:
            # Get list of posts with comments
            posts = client.get_posts_with_comments(page_size=10, page_limit=5)
            save_data_to_json(posts, "posts.json")
            print("Posts data saved successfully.")
        except Exception as err:
            logging.exception("Error fetching posts")
            print("Error fetching posts:", str(err))

    except Exception as err:
        logging.exception("Error connecting to the API")
        print("Error connecting to the API:", str(err))

if __name__ == "__main__":
    main()
