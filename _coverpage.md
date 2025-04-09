<p align="center">
  <img id="logo" width="320px" src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/logo-dark.png" alt="brainyflow's logo" />
<p>

<h1 style="max-width: 700px; margin: auto;">More AI, with less coding! 🚀</h1>
<h2>Let Agents build Agents with zero bloat, zero dependencies, zero vendor lock-in 😮</h2>

<!-- <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/divider.png" alt="divider" width="100%" style="max-width: 920px"> -->

<nav align="center">
  <a href="https://brainy.gitbook.io/flow/introduction/getting_started">Getting started 🐣</a>
  <a href="https://brainy.gitbook.io/flow/introduction/installation">Installation 🚜</a>
  <a href="https://github.com/zvictor/brainyflow/tree/master/cookbook">Examples 🌈 </a>
  <a href="https://pypi.org/project/brainyflow">PyPI <img src="https://iconduck.com/vectors/vctrahatphfa/media/svg/download" width="17" height="17" alt="Python Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <a href="https://www.npmjs.com/package/brainyflow">NPM <img src="https://iconduck.com/vectors/vctrk180y7wy/media/svg/download" width="17" height="17" alt="Typescript Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <a href="https://github.com/zvictor/brainyflow">Github <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.svg" width="17" height="17" alt="Github Logo" style="vertical-align: sub; margin: 0 2px;"></a>
  <!-- Dropdown container -->
  <div id="docs-dropdown-container">
    <!-- Trigger link -->
    <a href="/docs.txt" class="docs-dropdown-trigger">docs.txt 📜</a>
    <!-- Dropdown content -->
    <div class="dropdown-content">
      <a href="/docs.python.txt"> <!-- Python Link -->
        <img class="dropdown-icon" src="https://iconduck.com/vectors/vctrahatphfa/media/svg/download" width="17" height="17" alt="Python Logo">docs.<em>python</em>.txt
      </a>
      <a href="/docs.typescript.txt"> <!-- Typescript Link -->
        <img class="dropdown-icon" src="https://iconduck.com/vectors/vctrk180y7wy/media/svg/download" width="17" height="17" alt="Typescript Logo">docs.<em>typescript</em>.txt
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

    /* Show dropdown on hover of CONTAINER */
    #docs-dropdown-container:hover .dropdown-content {
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
  <p class="horizontal">
  <p style="font-size: 1.2em; font-weight: bolder; margin: 10px 0">WTF is <em>brainyFlow</em> ?</p>
    It's a 🤯 65-line only minimalist AI framework.<br />
    It provides a simple interface for building Agents that reduces complexity and turns LLMs much more powerful!
  <p>
  <!-- <div class="vertical">
  </div> -->
</div>
