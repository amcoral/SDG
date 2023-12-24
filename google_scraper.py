def is_good_url(url: str) -> bool:
    bad_urls = ['https://www.globenewswire.com', "market", "research", "youtube"]
    matches = [match for match in bad_urls if match in url]
    return len(matches) == 0

def valid_url(url: str, domain: str) -> str:
  if 'https' in url:
    return url
  else:
    return "https://" + domain + url

def build_queries(queries):
  if len(queries) > 1:
    return "\n".join(queries)
  else:
    return queries[0]

def get_input(input_queries):
  queries = build_queries(input_queries)
  return {
    "queries": queries,
    "maxPagesPerQuery": 1,
    "resultsPerPage": 4,
    "mobileResults": False,
    "languageCode": "",
    "maxConcurrency": 10,
    "minConcurrency": 1,
    "saveHtml": False,
    "saveHtmlToKeyValueStore": False,
    "includeUnfilteredResults": False,
    "customDataFunction": """async ({ input, $, request, response, html }) => {
      return {
        pageTitle: $('title').text(),
      };
    };"""
  }

def transform_results(results):
    """Transform dataset results into url objects needed for next actor"""
    out = results
    clean_results = []
    for result in results:
      for r in result['organicResults']:
        if r and r["url"] and is_good_url(r["url"]):
          url = valid_url(r["url"], "google.com")
          clean_results.append(url)
    return clean_results

def run_google(client, queries):
  run_input = get_input(queries)
  run = client.actor("nFJndFXA5zjCTuudP").call(run_input=run_input, memory_mbytes=32768)
  dataset = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items()]
  return transform_results(dataset)
