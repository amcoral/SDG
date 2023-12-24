from apify_client import ApifyClient
from google_news import run_news
from smart_article import run_article
from openai_chat import get_overview
from sdg_data import GOALS
from os import getenv
from dotenv import load_dotenv

load_dotenv()
# Initialize the ApifyClient with your API token
client = ApifyClient(getenv("APIFY_TOKEN"), max_retries=1)

def filter_text(text):
  has_contact = "contact us" in text.lower()
  has_buy = "buy now" in text.lower()
  has_author = "written by" in text.lower()
  return has_contact or has_buy or has_author

def clean_out_text(out_text):
  clean_text = []
  for text in out_text:
    if not filter_text(text):
      clean_text.append(text)
  return clean_text

def get_query(company, keyword_search):
  search_keys = " ".join(keyword_search)
  return f"{search_keys} \"{company}\""

def run(goal_idx, company):
  keywords = GOALS[goal_idx]["keyword_search"]
  query = get_query(company, keywords)
  urls = run_news(client, query, 20)
  out_text = clean_out_text(run_article(client, urls))
  response = get_overview(goal_idx, company)
  return response
