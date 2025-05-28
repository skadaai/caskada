import fs from 'fs'
import path from 'path'

/**
 * Extracts changelog text for a specific version from CHANGELOG.md
 * @param {string} packageDir - Directory containing the package and CHANGELOG.md
 * @param {string} versionString - The version to extract changelog for (e.g., "1.2.3")
 * @returns {string} - The changelog text for the specified version.
 */
function getChangelogForVersion(packageDir, versionString) {
  const changelogPath = path.join(packageDir, 'CHANGELOG.md')
  if (!fs.existsSync(changelogPath)) {
    console.warn(`Changelog file not found: ${changelogPath}`)
    return `Released version ${versionString}` // Fallback
  }

  const changelogContent = fs.readFileSync(changelogPath, 'utf8')
  const lines = changelogContent.split('\n')
  let capturing = false
  const capturedLines = []

  // Regex to match version headers like "## 1.2.3" or "## [1.2.3]"
  // Changesets usually outputs "## 1.2.3"
  const escapedVersionString = versionString.replace(/\./g, '\\.')
  const versionHeaderRegex = new RegExp(`^##\\s+(\\[${escapedVersionString}\\]|${escapedVersionString})`)

  for (const line of lines) {
    if (versionHeaderRegex.test(line)) {
      capturing = true
      // We don't include the "## 1.2.3" line itself; changelog entries are under it.
      continue
    }

    if (capturing) {
      // Stop if we hit the next version's header (another "## ...")
      if (line.match(/^##\s+/)) {
        break
      }
      capturedLines.push(line)
    }
  }

  const result = capturedLines.join('\n').trim()
  // Provide a fallback if no specific entries were found under the version header
  return result || `Updates for v${versionString}`
}

// CLI usage: node .github/scripts/extract-changelog-text.js <packageDir> <versionString>
// Example: node .github/scripts/extract-changelog-text.js python 1.0.1
if (import.meta.url.startsWith('file:') && process.argv[1] === import.meta.url.substring(7)) {
  const packageDir = process.argv[2]
  const versionString = process.argv[3]

  if (!packageDir || !versionString) {
    console.error('Usage: node .github/scripts/extract-changelog-text.js <packageDir> <versionString>')
    process.exit(1)
  }

  const changelogText = getChangelogForVersion(packageDir, versionString)
  process.stdout.write(changelogText) // Output raw text directly
}
