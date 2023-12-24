def format_urls(urls):
  input_urls = []
  for url in urls:
    input_urls.append({"url": url})
  return input_urls

# Prepare the Actor input
def get_input(input_urls):
  urls = format_urls(input_urls)
  run_input = {
      "articleUrls": urls,
      "onlyNewArticles": False,
      "onlyNewArticlesPerDomain": False,
      "onlyInsideArticles": False,
      "enqueueFromArticles": False,
      "crawlWholeSubdomain": False,
      "onlySubdomainArticles": True,
      "scanSitemaps": False,
      "saveSnapshots": False,
      "useGoogleBotHeaders": False,
      "minWords": 0,
      "mustHaveDate": False,
      "proxyConfiguration": { "useApifyProxy": True },
      "useBrowser": False
  }
  return run_input

def run_article(client, urls):
  run_input = get_input(urls)
  run = client.actor("hy5TYiCBwQ9o8uRKG").call(run_input=run_input, memory_mbytes=32768)
  dataset = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items() if "text" in i]
  dataset = [i["text"].split("\n") for i in client.dataset(run["defaultDatasetId"]).iterate_items() if len(i["text"]) > 30]
  dataset = [i for sublist in dataset for i in sublist]
  dataset = [i for i in dataset if len(i) > 30]
  return dataset
