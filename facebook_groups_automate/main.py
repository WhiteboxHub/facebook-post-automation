from config import FACEBOOK_EMAIL, FACEBOOK_PASSWORD, GROUPS
from facebook_poster import FacebookPoster
from utils import log, get_last_run, set_last_run

def main():
    last_run = get_last_run()
    if last_run:
        log(f"Last run was at: {last_run}")
    else:
        log("This is the first run.")

    poster = FacebookPoster(FACEBOOK_EMAIL, FACEBOOK_PASSWORD)
    try:
        poster.login()
        for group in GROUPS:
            url = group["url"]
            image_path = group.get("image_path")
            message = group.get("message", "Automated post for training and placement updates.")
            poster.post_to_group(url, message, image_path=image_path)
    finally:
        poster.close()
        now = set_last_run()
        log(f"Updated last run to: {now}")

if __name__ == "__main__":
    main() 