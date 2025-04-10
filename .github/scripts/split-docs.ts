import fs from 'fs/promises'
import path from 'path'

const inputFilePath = path.resolve('gh-pages-content/docs.txt')
const outputDir = path.resolve('gh-pages-content')
const pythonOutputFilePath = path.join(outputDir, 'docs.python.txt')
const typescriptOutputFilePath = path.join(outputDir, 'docs.typescript.txt')

// Regex to find the entire tabs block, allowing for extra whitespace
// Capture group 1: opening tag, group 2: inner content, group 3: closing tag
const tabsBlockRegex = /(\{%\s*tabs\s*%\})(.*?)(\{%\s*endtabs\s*%\})/gs
// Regex to find individual tabs within a block, allowing for extra whitespace
// Capture group 0: full tab, group 1: title, group 2: body
const tabRegex = /\{%\s*tab\s+title="([^"]+)"\s*%}(.*?)\{%\s*endtab\s*%}/gs

/**
 * Processes the documentation content to filter/extract tab blocks for a specific language.
 * - If exactly 1 tab matches, extracts its content.
 * - If >1 tabs match, keeps the {% tabs %} structure with only matching tabs.
 * - If 0 tabs match, keeps the original block.
 * @param content The original documentation content.
 * @param languageRegex A regex to match the desired language tab title (case-insensitive).
 * @returns The processed content.
 */
function processContentForLanguage(content: string, languageRegex: RegExp): string {
  return content.replace(tabsBlockRegex, (match, openTag, blockContent, closeTag) => {
    const matchingTabsFull: string[] = [] // Store the full text of matching tabs
    const matchingTabsBody: string[] = [] // Store the body content of matching tabs
    // Reset lastIndex before using exec in a loop
    tabRegex.lastIndex = 0
    let tabMatch
    while ((tabMatch = tabRegex.exec(blockContent)) !== null) {
      const fullTabMatch = tabMatch[0] // The entire {% tab ... %}...{% endtab %}
      const title = tabMatch[1].trim()
      const body = tabMatch[2] // The content within the tab

      if (languageRegex.test(title)) {
        matchingTabsFull.push(fullTabMatch)
        matchingTabsBody.push(body)
      }
    }

    // Decide what to return based on the number of matches
    if (matchingTabsFull.length === 1) {
      // Exactly one match: return only the body content, trimmed
      return matchingTabsBody[0].trim()
    }

    if (matchingTabsFull.length > 1) {
      // More than one match: reconstruct the tabs block with only matching tabs
      const newBlockContent = matchingTabsFull.join('\n')
      return `${openTag}\n${newBlockContent}\n${closeTag}`
    }

    // No matches: return the original block unchanged
    return match
  })
}

async function splitDocs() {
  console.log(`Reading input file: ${inputFilePath}`)
  let content: string
  try {
    content = await fs.readFile(inputFilePath, 'utf-8')
  } catch (error) {
    console.error(`Error reading input file ${inputFilePath}:`, error)
    process.exit(1)
  }

  console.log('Processing content for Python...')
  const pythonContent = processContentForLanguage(content, /^python/i)

  console.log('Processing content for TypeScript...')
  const typescriptContent = processContentForLanguage(content, /^(typescript|javascript)/i)

  try {
    console.log(`Writing Python docs to: ${pythonOutputFilePath}`)
    await fs.writeFile(pythonOutputFilePath, pythonContent)
    console.log(`Writing TypeScript docs to: ${typescriptOutputFilePath}`)
    await fs.writeFile(typescriptOutputFilePath, typescriptContent)
    console.log('Successfully created language-specific documentation files.')
  } catch (error) {
    console.error('Error writing output files:', error)
    process.exit(1)
  }
}

splitDocs()
