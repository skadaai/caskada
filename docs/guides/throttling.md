# Rate Limiting and Throttling

Effective rate limiting is crucial when working with external APIs and services. This guide covers patterns for implementing throttling in BrainyFlow applications.

This is particularly important when:

1. Calling external APIs with rate limits
2. Managing expensive operations (like LLM calls)
3. Preventing system overload from too many parallel requests

## Concurrency Control Patterns

### 1. Using Semaphores (Python)

```python
import asyncio

class LimitedParallelExec(Node):
    def __init__(self, concurrency=3):
        self.semaphore = asyncio.Semaphore(concurrency)

    async def exec(self, items):
        async def limited_process(item):
            async with self.semaphore:
                return await self.process_item(item)

        tasks = [limited_process(item) for item in items]
        return await asyncio.gather(*tasks)

    async def process_item(self, item):
        # Process a single item
        pass
```

### 2. Using p-limit (TypeScript)

```typescript
import pLimit from 'p-limit'

class LimitedParallelExec extends Node {
  constructor(private concurrency = 3) {
    super()
  }

  async exec(items) {
    const limit = pLimit(this.concurrency)
    return Promise.all(items.map((item) => limit(() => this.processItem(item))))
  }

  async processItem(item) {
    // Process a single item
  }
}
```

## Rate Limiting with Window Limits

{% tabs %}
{% tab title="Python" %}

```python
from ratelimit import limits, sleep_and_retry

# 30 calls per minute
@sleep_and_retry
@limits(calls=30, period=60)
def call_api():
    # Your API call here
    pass
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { RateLimiter } from 'limiter'

// 30 calls per minute
const limiter = new RateLimiter({ tokensPerInterval: 30, interval: 'minute' })

async function callApi() {
  await limiter.removeTokens(1)
  // Your API call here
}
```

{% endtab %}
{% endtabs %}

## Throttler Utility

{% tabs %}
{% tab title="Python" %}

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5)
)
def call_api_with_retry():
    # Your API call here
    pass
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import pRetry from 'p-retry'

async function callApiWithRetry() {
  return pRetry(
    async () => {
      // Your API call here
    },
    {
      retries: 5,
      minTimeout: 4000,
      maxTimeout: 10000,
    },
  )
}
```

{% endtab %}
{% endtabs %}

## Advanced Throttling Patterns

### 1. Token Bucket Rate Limiter

{% tabs %}
{% tab title="Python" %}

```python
from pyrate_limiter import Duration, Rate, Limiter

# 10 requests per minute
rate = Rate(10, Duration.MINUTE)
limiter = Limiter(rate)

@limiter.ratelimit("api_calls")
async def call_api():
    # Your API call here
    pass
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { TokenBucket } from 'limiter'

// 10 requests per minute
const limiter = new TokenBucket({
  bucketSize: 10,
  tokensPerInterval: 10,
  interval: 'minute',
})

async function callApi() {
  await limiter.removeTokens(1)
  // Your API call here
}
```

{% endtab %}
{% endtabs %}

### 2. Sliding Window Rate Limiter

{% tabs %}
{% tab title="Python" %}

```python
from slidingwindow import SlidingWindowRateLimiter

limiter = SlidingWindowRateLimiter(
    max_requests=100,
    window_size=60  # 60 seconds
)

async def call_api():
    if not limiter.allow_request():
        await asyncio.sleep(limiter.time_to_next_request()) #  or raise RateLimitExceeded()
    # Your API call here
    return "API response"
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class SlidingWindowRateLimiter {
  private requests: number[] = []

  constructor(
    private maxRequests: number,
    private windowSize: number,
  ) {}

  allowRequest(): boolean {
    const now = Date.now()
    // Remove expired requests
    this.requests = this.requests.filter((time) => now - time < this.windowSize * 1000)
    // Check if we can allow another request
    return this.requests.length < this.maxRequests
  }

  timeToNextRequest(): number {
    const now = Date.now()
    this.requests = this.requests.filter((time) => now - time < this.windowSize * 1000)
    if (this.requests.length < this.maxRequests) return 0
    const oldest = this.requests[0]
    return Math.ceil((oldest + this.windowSize * 1000 - now) / 1000)
  }
}

// Usage:
const limiter = new SlidingWindowRateLimiter(100, 60) // 100 requests per 60 seconds

async function callApi() {
  if (!limiter.allowRequest()) {
    await new Promise((resolve) => setTimeout(resolve, limiter.timeToNextRequest() * 1000))
  }
  // Your API call here
  return 'API response'
}
```

{% endtab %}
{% endtabs %}

## Best Practices

1. **Monitor API Responses**: Watch for 429 (Too Many Requests) responses and adjust your rate limiting accordingly
2. **Implement Retry Logic**: When hitting rate limits, implement exponential backoff for retries
3. **Distribute Load**: If possible, spread requests across multiple API keys or endpoints
4. **Cache Responses**: Cache frequent identical requests to reduce API calls
5. **Batch Requests**: Combine multiple requests into single API calls when possible

## Integration with BrainyFlow

### Throttled LLM Node

{% tabs %}
{% tab title="Python" %}

```python
class ThrottledLLMNode(Node):
    def __init__(self, max_retries=3, calls_per_minute=30):
        super().__init__(max_retries=max_retries)
        self.limiter = Limiter(Rate(calls_per_minute, Duration.MINUTE))

    async def exec(self, prompt):
        @self.limiter.ratelimit('llm_calls')
        async def limited_llm_call(text):
            return await call_llm(text)

        return await limited_llm_call(prompt)

    async def exec_fallback(self, prompt, error):
        # Handle rate limit errors specially
        if "rate limit" in str(error).lower():
            # Wait longer before retrying
            await asyncio.sleep(60)
            return await self.exec(prompt)
        # For other errors, fall back to a simple response
        return "I'm having trouble processing your request right now."
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node, NodeError } from 'brainyflow'
import { RateLimiter } from 'limiter'

class ThrottledLLMNode extends Node {
  private limiter: RateLimiter

  constructor(
    private maxRetries = 3,
    callsPerMinute = 30,
  ) {
    super({ maxRetries })
    this.limiter = new RateLimiter({ tokensPerInterval: callsPerMinute, interval: 'minute' })
  }

  async exec(prompt: string): Promise<string> {
    // Wait for token before proceeding
    await this.limiter.removeTokens(1)
    return await callLLM(prompt)
  }

  async execFallback(prompt: string, error: NodeError): Promise<string> {
    // Handle rate limit errors specially
    if (error.message.toLowerCase().includes('rate limit')) {
      // Wait longer before retrying
      await new Promise((resolve) => setTimeout(resolve, 60000))
      return this.exec(prompt)
    }
    // For other errors, fall back to a simple response
    return "I'm having trouble processing your request right now."
  }
}
```

{% endtab %}
{% endtabs %}

## Linking to Related Concepts

For batch processing patterns, see [Flow](../core_abstraction/flow.md).
