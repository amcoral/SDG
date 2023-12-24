def is_good_url(url: str) -> bool:
    bad_urls = ['https://www.globenewswire.com', "market", "research", "youtube"]
    matches = [match for match in bad_urls if match in url]
    return len(matches) == 0

def valid_url(url: str, domain: str) -> str:
  if 'https' in url:
    return url
  else:
    return "https://" + domain + url

def get_input(query, num_articles):
  run_input = {
      "query": query,
      "language": "US:en",
      "maxItems": num_articles,
      "extractImages": True,
      "proxyConfiguration": { "useApifyProxy": True },
  }
  return run_input

def run_news(client, query, num_articles):
  run_input = get_input(query, num_articles)
  run = client.actor("eWUEW5YpCaCBAa0Zs").call(run_input=run_input, memory_mbytes=32768)
  urls = []
  dataset = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items()]
  for d in dataset:
    if d and d["link"] and is_good_url(d["link"]):
      urls.append(valid_url(d["link"], "google.com"))
  return urls
