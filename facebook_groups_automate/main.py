from config import FACEBOOK_EMAIL, FACEBOOK_PASSWORD, GROUPS
from facebook_poster import FacebookPoster
from utils import log, get_last_run, set_last_run, human_delay
import os

def process_groups(poster, groups, image_path=None):
    successful_posts = 0
    failed_posts = 0
    
    for group in groups:
        try:
            url = group["url"]
            message = group.get("message", "Automated post for training and placement updates.")
            
            log(f"\nProcessing group: {group.get('name', url)}")
            poster.post_to_group(url, message, image_path=image_path)
            successful_posts += 1
            
            # Add a longer delay between groups to appear more human-like
            human_delay(10, 15)
            
        except Exception as e:
            log(f"Failed to process group {group.get('name', url)}: {str(e)}")
            failed_posts += 1
            # If we encounter an error, wait longer before trying the next group
            human_delay(20, 30)
            continue
    
    return successful_posts, failed_posts

def main():
    # Check for last run
    last_run = get_last_run()
    if last_run:
        log(f"Last run was at: {last_run}")
    else:
        log("This is the first run.")

    # Check if flyer exists
    image_path = None
    if os.path.exists("WBL_Flyer.pdf"):
        image_path = os.path.abspath("WBL_Flyer.pdf")
        log(f"Found flyer at: {image_path}")
    else:
        log("No flyer found. Will post without image.")

    poster = None
    try:
        # Initialize the poster with headless=False for better visibility
        poster = FacebookPoster(FACEBOOK_EMAIL, FACEBOOK_PASSWORD, headless=False)
        
        # Login to Facebook
        poster.login()
        
        # Process all groups
        successful, failed = process_groups(poster, GROUPS, image_path)
        
        # Log summary
        log(f"\nAutomation Summary:")
        log(f"Successfully posted to {successful} groups")
        log(f"Failed to post to {failed} groups")
        
    except Exception as e:
        log(f"An error occurred during automation: {str(e)}")
    finally:
        if poster:
            poster.close()
        now = set_last_run()
        log(f"Updated last run to: {now}")

if __name__ == "__main__":
    main() 