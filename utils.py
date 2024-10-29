import re
from bs4 import BeautifulSoup
from googletrans import Translator
from datetime import datetime
import json
import os

# Function to remove HTML tags from a string
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Function to get Open Graph tags from a URL
def get_open_graph_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    og_tags = {}
    for tag in soup.find_all("meta"):
        if tag.get("property", "").startswith("og:"):
            og_tags[tag["property"][3:]] = tag["content"]
    return og_tags

# Function to translate text using googletrans
def translate_text(text, dest="pt"):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text

# Function to save last check dates to a file
def save_last_check_dates(last_check_dates, filename="last_check.json"):
    with open(filename, "w") as f:
        json.dump(last_check_dates, f)

# Function to load last check dates from a file
def load_last_check_dates(filename="last_check.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

# Function to save schedules to a file
def save_schedules(schedules, filename="schedules.json"):
    with open(filename, "w") as f:
        json.dump(schedules, f)

# Function to load schedules from a file
def load_schedules(filename="schedules.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

# Function to restore schedules from a file
def restore_schedules(scheduler, schedules):
    for job_id, job_data in schedules.items():
        try:
            if "run_date" in job_data:
                schedule_datetime = datetime.strptime(job_data["run_date"], "%Y-%m-%dT%H:%M:%S")
                scheduler.add_job(
                    post_to_linkedin,
                    "date",
                    run_date=schedule_datetime,
                    args=job_data["args"],
                    id=job_id,
                )
            else:
                logger.warning(f"Schedule {job_id} does not have 'run_date'.")
        except Exception as e:
            logger.error(f"Error restoring schedule {job_id}: {e}")
