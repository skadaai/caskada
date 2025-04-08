import fs from 'fs/promises'
import path from 'path'

const inputFilePath = path.resolve('gh-pages-content/docs.txt')
const outputDir = path.resolve('gh-pages-content')
const pythonOutputFilePath = path.join(outputDir, 'docs.python.txt')
const typescriptOutputFilePath = path.join(outputDir, 'docs.typescript.txt')

// Regex to find the entire tabs block, allowing for extra whitespace
const tabsBlockRegex = /\{%\s*tabs\s*%}(.*?)\{%\s*endtabs\s*%}/gs
// Regex to find individual tabs within a block, allowing for extra whitespace
const tabRegex = /\{%\s*tab\s+title="([^"]+)"\s*%}(.*?)\{%\s*endtab\s*%}/gs

/**
 * Processes the documentation content to extract code blocks for a specific language.
 * @param content The original documentation content.
 * @param languageRegex A regex to match the desired language tab title (case-insensitive).
 * @returns The processed content with only the specified language's tab content remaining where applicable.
 */
function processContentForLanguage(content: string, languageRegex: RegExp): string {
  return content.replace(tabsBlockRegex, (match, blockContent) => {
    let languageTabContent = ''
    let foundLanguage = false
    // Reset lastIndex before using exec in a loop
    tabRegex.lastIndex = 0
    let tabMatch
    while ((tabMatch = tabRegex.exec(blockContent)) !== null) {
      const title = tabMatch[1].trim()
      const tabBody = tabMatch[2] // Keep leading/trailing whitespace within the tab body
      if (languageRegex.test(title)) {
        languageTabContent = tabBody
        foundLanguage = true
        break // Found the desired language tab
      }
    }
    // If the language tab was found, return its content (trimmed), otherwise return the original block
    return foundLanguage ? languageTabContent.trim() : match
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
  const typescriptContent = processContentForLanguage(content, /^typescript/i)

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
