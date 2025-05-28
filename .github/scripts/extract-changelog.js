import fs from 'fs'
import path from 'path'

/**
 * Extracts changelog information from changeset files
 * @param {string} packageDir - Directory containing the package (e.g., 'python', 'typescript')
 * @param {string} packageName - Name of the package
 * @returns {Object} - { version, changelog, hasChanges }
 */
export function extractChangelog(packageDir, packageName) {
  try {
    // Read version from package.json if it exists (for both packages after changeset processing)
    const packageJsonPath = path.join(packageDir, 'package.json')
    let version = null

    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'))
      version = packageJson.version
    } else if (packageDir === 'python') {
      // For Python, extract from setup.py
      const setupPyPath = path.join(packageDir, 'setup.py')
      if (fs.existsSync(setupPyPath)) {
        const setupContent = fs.readFileSync(setupPyPath, 'utf8')
        const versionMatch = setupContent.match(/version=['"]([^'"]+)['"]/)
        if (versionMatch) {
          version = versionMatch[1]
        }
      }
    }

    if (!version) {
      return { version: null, changelog: '', hasChanges: false }
    }

    // Look for CHANGELOG.md
    const changelogPath = path.join(packageDir, 'CHANGELOG.md')
    let changelog = ''

    if (fs.existsSync(changelogPath)) {
      const changelogContent = fs.readFileSync(changelogPath, 'utf8')

      // Extract the latest version's changelog
      const lines = changelogContent.split('\n')
      let capturing = false
      let capturedLines = []

      for (const line of lines) {
        // Check if this line starts a version section
        if (line.match(/^##\s+/)) {
          if (capturing) {
            // We've hit the next version, stop capturing
            break
          }
          // Check if this is our version
          if (line.includes(version)) {
            capturing = true
            continue // Skip the version header line
          }
        } else if (capturing) {
          // If we hit another ## or ### heading that's not a patch/minor section, we might be done
          if (line.match(/^##[^#]/)) {
            break
          }
          capturedLines.push(line)
        }
      }

      changelog = capturedLines.join('\n').trim()
    }

    // If no changelog found, create a basic one
    if (!changelog) {
      changelog = `Release ${version}`
    }

    return {
      version,
      changelog,
      hasChanges: true,
    }
  } catch (error) {
    console.error('Error extracting changelog:', error)
    return { version: null, changelog: '', hasChanges: false }
  }
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const packageDir = process.argv[2]
  const packageName = process.argv[3]

  if (!packageDir || !packageName) {
    console.error('Usage: node extract-changelog.js <packageDir> <packageName>')
    process.exit(1)
  }

  const result = extractChangelog(packageDir, packageName)
  console.log(JSON.stringify(result, null, 2))
}
