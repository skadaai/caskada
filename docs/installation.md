---
machine-display: false
---

# Installation

Caskada is currently available for both Python and TypeScript.

{% tabs %}
{% tab title="Python" %}
You can install the Python package using pip:

```bash
pip install caskada
```

{% endtab %}

{% tab title="TypeScript" %}
You can install the TypeScript package using pnpm (or npm/yarn):

```bash
pnpm add caskada
# or
npm install caskada
# or
yarn add caskada
```

{% endtab %}

{% tab title="JavaScript (Browser)" %}
You can import the JavaScript file directly in the browser using a `<script>` tag:

```html
<script type="module">
  import * as caskada from 'https://unpkg.com/caskada@latest/dist/caskada.js'

  new caskada.Node(...)
</script>
```

or

```html
<script type="module" src="https://unpkg.com/caskada@latest/dist/caskada.js"></script>
<script>
  new globalThis.caskada.Node(...)
</script>
```

{% endtab %}
{% endtabs %}

## Alternative: Copy the Source Code

Since Caskada is lightweight and dependency-free, you can also install it by simply copying the source code file directly into your project:

{% tabs %}
{% tab title="Python" %}
Copy [`python/caskada.py`](https://github.com/skadaai/caskada/blob/main/python/caskada.py)
{% endtab %}

{% tab title="TypeScript" %}
Copy [`typescript/caskada.ts`](https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts)
{% endtab %}
{% endtabs %}

## Next Steps

Once you have Caskada installed, check out the [Getting Started](./getting_started.md) guide to build your first flow, or explore the [Core Abstractions](./core_abstraction/node.md) to understand the framework's fundamental concepts.
