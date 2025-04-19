---
title: 'Web Search'
machine-display: false
---

# Web Search

{% hint style="warning" %}

**BrainyFlow does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

We recommend some implementations of commonly used web search tools.

| **API**                           | **Free Tier**                                       | **Pricing Model**                                   | **Docs**                                                                                   |
| --------------------------------- | --------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Google Custom Search JSON API** | 100 queries/day free                                | $5 per 1000 queries.                                | [Link](https://developers.google.com/custom-search/v1/overview)                            |
| **Bing Web Search API**           | 1,000 queries/month                                 | $15–$25 per 1,000 queries.                          | [Link](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) |
| **DuckDuckGo Instant Answer**     | Completely free (Instant Answers only, **no URLs**) | No paid plans; usage unlimited, but data is limited | [Link](https://duckduckgo.com/api)                                                         |
| **Brave Search API**              | 2,000 queries/month free                            | $3 per 1k queries for Base, $5 per 1k for Pro       | [Link](https://brave.com/search/api/)                                                      |
| **SerpApi**                       | 100 searches/month free                             | Start at $75/month for 5,000 searches               | [Link](https://serpapi.com/)                                                               |
| **RapidAPI**                      | Many options                                        | Many options                                        | [Link](https://rapidapi.com/search?term=search&sortBy=ByRelevance)                         |

## Example Code

### 1. Google Custom Search JSON API

{% tabs %}
{% tab title="Python" %}

```python
import requests
import os

API_KEY = os.environ.get("GOOGLE_API_KEY") # Use environment variables
CX_ID = os.environ.get("GOOGLE_CX_ID")     # Use environment variables
query = "example"

url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": API_KEY,
    "cx": CX_ID,
    "q": query
}

if not API_KEY or not CX_ID:
    print("Error: Please set GOOGLE_API_KEY and GOOGLE_CX_ID environment variables.")
else:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        results = response.json()
        print(results)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google search results: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function searchGoogle(query: string): Promise<any> {
  const apiKey = process.env.GOOGLE_API_KEY // Use environment variables
  const cxId = process.env.GOOGLE_CX_ID // Use environment variables

  if (!apiKey || !cxId) {
    console.error('Error: Please set GOOGLE_API_KEY and GOOGLE_CX_ID environment variables.')
    return null
  }

  const url = new URL('https://www.googleapis.com/customsearch/v1')
  url.searchParams.append('key', apiKey)
  url.searchParams.append('cx', cxId)
  url.searchParams.append('q', query)

  try {
    const response = await fetch(url.toString())
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const results = await response.json()
    console.log(results)
    return results
  } catch (error) {
    console.error('Error fetching Google search results:', error)
    return null
  }
}

// Example usage:
// searchGoogle("example");
```

{% endtab %}
{% endtabs %}

### 2. Bing Web Search API

{% tabs %}
{% tab title="Python" %}

```python
import requests
import os

SUBSCRIPTION_KEY = os.environ.get("BING_API_KEY") # Use environment variables
query = "example"

url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
params = {"q": query}

if not SUBSCRIPTION_KEY:
    print("Error: Please set BING_API_KEY environment variable.")
else:
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        print(results)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bing search results: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function searchBing(query: string): Promise<any> {
  const subscriptionKey = process.env.BING_API_KEY // Use environment variables

  if (!subscriptionKey) {
    console.error('Error: Please set BING_API_KEY environment variable.')
    return null
  }

  const url = new URL('https://api.bing.microsoft.com/v7.0/search')
  url.searchParams.append('q', query)

  const headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
  }

  try {
    const response = await fetch(url.toString(), { headers })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const results = await response.json()
    console.log(results)
    return results
  } catch (error) {
    console.error('Error fetching Bing search results:', error)
    return null
  }
}

// Example usage:
// searchBing("example");
```

{% endtab %}
{% endtabs %}

### 3. DuckDuckGo Instant Answer

{% tabs %}
{% tab title="Python" %}

```python
import requests

query = "example"
url = "https://api.duckduckgo.com/"
params = {
    "q": query,
    "format": "json",
    "no_html": 1 # Often useful to remove HTML tags
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()
    print(results)
except requests.exceptions.RequestException as e:
    print(f"Error fetching DuckDuckGo results: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function searchDuckDuckGo(query: string): Promise<any> {
  const url = new URL('https://api.duckduckgo.com/')
  url.searchParams.append('q', query)
  url.searchParams.append('format', 'json')
  url.searchParams.append('no_html', '1') // Often useful

  try {
    const response = await fetch(url.toString())
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const results = await response.json()
    console.log(results)
    return results
  } catch (error) {
    console.error('Error fetching DuckDuckGo results:', error)
    return null
  }
}

// Example usage:
// searchDuckDuckGo("example");
```

{% endtab %}
{% endtabs %}

### 4. Brave Search API

{% tabs %}
{% tab title="Python" %}

```python
import requests
import os

SUBSCRIPTION_TOKEN = os.environ.get("BRAVE_API_TOKEN") # Use environment variables
query = "example"

url = "https://api.search.brave.com/res/v1/web/search"
headers = {
    "X-Subscription-Token": SUBSCRIPTION_TOKEN,
    "Accept": "application/json" # Good practice
}
params = {
    "q": query
}

if not SUBSCRIPTION_TOKEN:
    print("Error: Please set BRAVE_API_TOKEN environment variable.")
else:
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        print(results)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Brave search results: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function searchBrave(query: string): Promise<any> {
  const subscriptionToken = process.env.BRAVE_API_TOKEN // Use environment variables

  if (!subscriptionToken) {
    console.error('Error: Please set BRAVE_API_TOKEN environment variable.')
    return null
  }

  const url = new URL('https://api.search.brave.com/res/v1/web/search')
  url.searchParams.append('q', query)

  const headers = {
    'X-Subscription-Token': subscriptionToken,
    Accept: 'application/json', // Good practice
  }

  try {
    const response = await fetch(url.toString(), { headers })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const results = await response.json()
    console.log(results)
    return results
  } catch (error) {
    console.error('Error fetching Brave search results:', error)
    return null
  }
}

// Example usage:
// searchBrave("example");
```

{% endtab %}
{% endtabs %}

### 5. SerpApi

{% tabs %}
{% tab title="Python" %}

```python
import requests
import os

API_KEY = os.environ.get("SERPAPI_KEY") # Use environment variables
query = "example"

url = "https://serpapi.com/search"
params = {
    "engine": "google", # Or other engines like 'bing', 'duckduckgo'
    "q": query,
    "api_key": API_KEY
}

if not API_KEY:
    print("Error: Please set SERPAPI_KEY environment variable.")
else:
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        print(results)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SerpApi results: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function searchSerpApi(query: string, engine: string = 'google'): Promise<any> {
  const apiKey = process.env.SERPAPI_KEY // Use environment variables

  if (!apiKey) {
    console.error('Error: Please set SERPAPI_KEY environment variable.')
    return null
  }

  const url = new URL('https://serpapi.com/search')
  url.searchParams.append('engine', engine)
  url.searchParams.append('q', query)
  url.searchParams.append('api_key', apiKey)

  try {
    const response = await fetch(url.toString())
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const results = await response.json()
    console.log(results)
    return results
  } catch (error) {
    console.error('Error fetching SerpApi results:', error)
    return null
  }
}

// Example usage:
// searchSerpApi("example");
// searchSerpApi("example", "bing");
```

{% endtab %}
{% endtabs %}
