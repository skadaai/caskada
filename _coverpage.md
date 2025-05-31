<p align="center">
  <img id="logo" width="320px" src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/logo-dark.png" alt="brainyflow's logo" />
<p>

<h1 style="max-width: 700px; margin: auto;">More AI, with less coding! 🚀</h1>
<h2>Build Powerful AI Agents with Minimal Code, Maximum Freedom.</h2>
<p>Zero bloat, dependencies, or vendor lock-in.</p>

<!-- <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/divider.png" alt="divider" width="100%" style="max-width: 920px"> -->

<nav align="center">
  <a href="https://brainy.gitbook.io/flow/introduction/getting_started">Get Started Now ✨ 🐣</a>
  <a href="https://github.com/zvictor/brainyflow/tree/master/cookbook">Examples 🌈 </a>
  <a href="https://pypi.org/project/brainyflow">PyPI <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="17" height="17" alt="Python Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <a href="https://www.npmjs.com/package/brainyflow">NPM <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="17" height="17" alt="Typescript Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <a href="https://discord.gg/N9mVvxRXyH">Chat <img src="https://cdn.prod.website-files.com/6257adef93867e50d84d30e2/66e3d80db9971f10a9757c99_Symbol.svg" width="17" height="17" alt="Discord Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <a href="https://github.com/zvictor/brainyflow">Github <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.svg" width="17" height="17" alt="Github Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <!-- Dropdown container -->
  <div id="docs-dropdown-container">
    <!-- Trigger link -->
    <a href="/docs.txt" class="docs-dropdown-trigger" tabindex="0">docs.txt 📜</a>
    <!-- Dropdown content -->
    <div class="dropdown-content">
      <a href="/docs.python.txt"> <!-- Python Link -->
        <img class="dropdown-icon" src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="17" height="17" alt="Python Logo">docs.<em>python</em>.txt
      </a>
      <a href="/docs.typescript.txt"> <!-- Typescript Link -->
        <img class="dropdown-icon" src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="17" height="17" alt="Typescript Logo">docs.<em>typescript</em>.txt
      </a>
      <a href="/docs.txt"> <!-- All Docs Link -->
        📜 docs.txt (<em>all</em>)
      </a>
    </div>
  </div>
  <style>
    /* Dropdown Container - Styled to fit nav layout */
    #docs-dropdown-container {
      position: relative; /* Needed for absolute positioning of content */
      display: inline-block; /* Fit in with other nav links */
      margin: 5px; /* Match other nav links */
    }

    /* Dropdown Trigger Link - Styling only */
    .docs-dropdown-trigger {
      display: inline-block; /* Needed for padding/border */
      background-color: var(--theme-color);
      padding: 7px 12px;
      border-radius: 10px;
      color: white;
      text-decoration: none;
      font-weight: bold;
      cursor: pointer;
    }

    /* Show dropdown on hover (desktop) OR when container has focus (click/tap) */
    #docs-dropdown-container:hover .dropdown-content,
    #docs-dropdown-container:focus-within .dropdown-content {
      display: block !important;
    }

    /* Dropdown Content Box */
    .dropdown-content {
      display: none;
      position: absolute;
      background-color: rgba(var(--cover-navigation-background-color), 0.9);
      min-width: 180px;
      box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.3);
      z-index: 10;
      border-radius: 5px;
      padding: 10px;
      top: 100%; /* Default position below */
      left: 50%;
      transform: translateX(-50%);
      /* margin-top: 5px; */ /* Removed to prevent gap */
    }

    /* Links within the dropdown */
    .dropdown-content a {
      color: white;
      padding: 10px 15px;
      text-decoration: none;
      display: block;
      white-space: nowrap;
      background-color: transparent;
      border-radius: 0;
      font-weight: bold; /* Ensure bold */
      cursor: pointer;
    }

    /* Dropdown link icons */
    .dropdown-icon {
      vertical-align: sub;
      margin-right: 8px;
    }

    /* Hover effect for dropdown links - subtle brightness change */
    .dropdown-content a:hover {
      filter: brightness(125%); /* Slightly lighter on hover */
    }

    /* Arrow connector */
    .dropdown-content {
      border: 1px solid var(--theme-color);
    }

    .dropdown-content::after {
      content: "";
      position: absolute;
      bottom: 100%; /* Position arrow at the top of the dropdown */
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: transparent transparent var(--theme-color) transparent; /* Pointing down */
    }
    /* Class to flip position and arrow */
    /* Class to flip position and arrow */
    .dropdown-content.above {
      top: auto;
      bottom: 100%;
      /* margin-bottom: 5px; */ /* Removed to prevent gap */
    }
    .dropdown-content.above::after {
      top: 100%; /* Position arrow at the bottom */
      bottom: auto;
      border-color: var(--theme-color) transparent transparent transparent; /* Pointing up */
    }

      /* Mobile Vertical Layout */
    @media screen and (max-width: 768px) {
      nav {
        display: flex;
        flex-direction: column;
        align-items: center; /* Center items vertically */
        text-align: center; /* Center inline-block children */
      }
      /* Adjust nav links specifically for mobile */
      nav > a { /* Target only standard links for block display */
        display: block; /* Make each link take full width */
        margin: 8px 0; /* Add vertical spacing */
        width: 80%; /* Control width */
        max-width: 250px; /* Max width */
        /* text-align: center; */ /* Centering handled by parent nav */
      }
      /* Keep dropdown container inline-block for hover, centered by parent */
      nav > #docs-dropdown-container {
        display: inline-block; /* Keep inline-block for hover */
        margin: 8px 0; /* Add vertical spacing */
        /* width: 80%; */ /* Let it size naturally */
        max-width: 250px; /* Max width */
        text-align: center; /* Center text within links */
      }

      /* Adjust dropdown positioning for vertical layout */
      #docs-dropdown-container:hover .dropdown-content {
          left: 50%; /* Re-center dropdown relative to the now block-level container */
          transform: translateX(-50%);
          min-width: 160px; /* Adjust width as needed */
      }
       .dropdown-content::after {
          left: 50%; /* Re-center arrow */
          margin-left: -5px;
      }
       .dropdown-content.above::after {
          left: 50%; /* Re-center arrow */
          margin-left: -5px;
      }
    }

  </style>
</nav>

<!-- <style>
  .vertical {
    display: flex;
    text-align: center;
    flex-direction: column;
    display: none;
  }

  @media screen and (max-width: 1024px) {
    .vertical {
      display: initial;
    }

    .horizontal {
      display: none;
    }
  }
</style> -->

<div class="glass">
  <p style="font-size: 1.2em; font-weight: bolder; margin: 10px 0">What is <em>BrainyFlow</em>?</p>
  <p>
    BrainyFlow is a <strong>radically minimalist AI framework</strong> (just 300 lines in Python!) enabling <em>Agentic Coding</em> through powerful, intuitive graph abstractions.<br />Build complex AI systems with unparalleled simplicity and freedom.
  </p>
  <strong>Key Features:</strong>
  <ul>
    <li><strong>Brain-Easy 🧠</strong>: Intuitive for humans and AI assistants.</li>
    <li><strong>Minimalist ✨</strong>: Core logic in just 300 lines.</li>
    <li><strong>Freedom 🔓</strong>: Zero bloat, dependencies, or vendor lock-in.</li>
    <li><strong>Composable 🧩</strong>: Build complex systems from simple parts.</li>
    <li><strong>Powerful 🦾</strong>: Supports Agents, Workflows, RAG, and more.</li>
    <li><strong>Agentic-Coding 🤖</strong>: Designed for AI-assisted development.</li>
    <li><strong>Universal 🌈</strong>: Works with any LLM provider.</li>
    <li><strong>Polyglot 🌍</strong>: Python & TypeScript supported.</li>
  </ul>
  <p>See how simple it is? Check out the <a href="https://brainy.gitbook.io/flow/introduction/getting_started">Getting Started</a> guide or dive into <a href="https://brainy.gitbook.io/flow/guides/agentic_coding">Agentic Coding</a>!</p></div>
</div>
