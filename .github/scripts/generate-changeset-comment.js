import { humanId } from 'human-id'

function getNewChangesetTemplate(packageName, title) {
  return encodeURIComponent(`---
"${packageName}": patch
---

${title}
`)
}

export function generateChangesetComment(context, packageType) {
  const packageName = packageType.toLocaleLowerCase()
  const directory = packageName
  const isTypescript = packageName === 'typescript'
  const icon = isTypescript
    ? '<img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="28" height="28" alt="Typescript Logo" />'
    : '<img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="28" height="28" alt="Python Logo" />'

  const changesetUrl = `${context.payload.pull_request.head.repo.html_url}/new/${
    context.payload.pull_request.head.ref
  }?filename=${directory}/.changeset/${humanId({
    separator: '-',
    capitalize: false,
  })}.md&value=${getNewChangesetTemplate(packageName, context.payload.pull_request.title)}`

  return `## Missing ${packageType} Changeset ${icon}
  
  Changes to the ${packageType} package were detected, but no changeset was found.
  Merging this PR will not cause a version bump for the ${packageType} package.
  
  If these changes should not result in a new version, you're good to go. **If these changes should result in a version bump, you need to add a changeset.**

  [Click here to learn what changesets are, and how to add one](https://github.com/changesets/changesets/blob/main/docs/adding-a-changeset.md).

  [Click here if you're a maintainer who wants to add a changeset to this PR](${changesetUrl})
  
  Alternatively, you can add a changeset by running:
  \`\`\`
  cd ${directory}
  pnpm changeset
  \`\`\`
  
  This will help document your changes and ensure proper versioning.`
}
