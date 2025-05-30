import fs from 'fs/promises'
import path from 'path'

const REPOSITORY = 'https://github.com/zvictor/brainyflow'
const COOKBOOK_DIR = 'cookbook'
const OUTPUT_DIR = 'docs/cookbook' // Directory where generated files will be saved
const PYTHON_EXAMPLES_FILE = path.join(OUTPUT_DIR, 'python.md')
const TYPESCRIPT_EXAMPLES_FILE = path.join(OUTPUT_DIR, 'typescript.md')

/**
 * Extracts project name and short description from README content.
 * @param {string} readmeContent - The content of the README.md file.
 * @param {string} defaultProjectName - Fallback project name if not found in README.
 * @returns {{projectName: string, shortDescription: string}}
 */
function extractProjectDetails(readmeContent, defaultProjectName) {
  let projectName = defaultProjectName
  let shortDescription = `Details are no available for ${defaultProjectName}.` // Default description

  const lines = readmeContent.split('\n')

  // Extract Project Name from the first H1 heading
  const firstH1Index = lines.findIndex((line) => line.startsWith('# '))
  if (firstH1Index !== -1) {
    projectName = lines[firstH1Index].substring(2).trim()
    // Update default description if project name is found
    shortDescription = `Details are no available for ${projectName}.`

    // Extract Short Description (first paragraph of text after H1)
    let descriptionLines = []
    for (let i = firstH1Index + 1; i < lines.length; i++) {
      const line = lines[i].trim()

      if (line === '') {
        // An empty line signifies the end of a paragraph
        if (descriptionLines.length > 0)
          break // End of description paragraph
        else continue // Skip leading empty lines after H1
      }

      // Stop if it's a new heading, code block, list, or horizontal rule
      if (
        line.startsWith('#') ||
        line.startsWith('```') ||
        line.startsWith('- ') ||
        line.startsWith('* ') ||
        /^\d+\.\s/.test(line) ||
        line.startsWith('---') ||
        line.startsWith('***') ||
        line.startsWith('___')
      ) {
        if (descriptionLines.length > 0)
          break // End of description if it has started
        else {
          // If description hasn't started, these elements mean no paragraph description
          descriptionLines = [] // Clear any potential stray lines
          break
        }
      }
      descriptionLines.push(line)

      // Check if the *next* line signifies a break, to capture multi-line paragraphs correctly.
      const nextLine = lines[i + 1] ? lines[i + 1].trim() : undefined
      if (
        nextLine === undefined ||
        nextLine === '' ||
        nextLine.startsWith('#') ||
        nextLine.startsWith('```') ||
        nextLine.startsWith('- ') ||
        nextLine.startsWith('* ') ||
        /^\d+\.\s/.test(nextLine) ||
        nextLine.startsWith('---')
      ) {
        break // End of paragraph
      }
    }

    if (descriptionLines.length > 0) {
      shortDescription = descriptionLines.join(' ').trim()
      // Truncate if too long for a summary
      if (shortDescription.length > 400) {
        shortDescription = shortDescription.substring(0, 397) + '...'
      }
    }
  }
  return { projectName, shortDescription }
}

/**
 * Generates the Markdown content for a list of projects.
 * @param {string} title - The title for the Markdown page (e.g., "Python Examples").
 * @param {Array<{name: string, description: string, readmeContent: string, dirName: string}>} projects - Array of project objects.
 * @returns {string} - The generated Markdown content.
 */
function generateMarkdown(title, projects) {
  let markdown = `---\ntitle: ${title}\nmachine-display: false\n---\n\n`
  markdown += `# ${title}\n\n`
  markdown += `All projects listed below can be found in our [cookbook directory](${path.join(REPOSITORY, 'tree/main', COOKBOOK_DIR)}).\n\n`
  if (projects.length === 0) {
    markdown += 'No examples found for this category yet.\n'
    return markdown
  }

  projects.forEach((project) => {
    // Escape HTML special characters in project name and description for the summary
    const escapedName = project.name.replace(/</g, '&lt;').replace(/>/g, '&gt;')
    const escapedDescription = project.description.replace(/</g, '&lt;').replace(/>/g, '&gt;')

    markdown += `## ${escapedName} ([${project.dirName}](${path.join(REPOSITORY, 'tree/main', COOKBOOK_DIR, project.dirName)}))\n`
    markdown += escapedDescription
    markdown += `<details>\n`
    markdown += `<summary><strong>Details</strong></summary>\n\n`
    markdown += `\n`
    markdown += `${project.readmeContent}\n\n`
    markdown += `</details>\n\n`
  })
  return markdown
}

/**
 * Main function to generate example pages.
 */
async function main() {
  try {
    await fs.mkdir(OUTPUT_DIR, { recursive: true }) // Ensure output directory exists

    const pythonProjects = []
    const typescriptProjects = []

    const entries = await fs.readdir(COOKBOOK_DIR, { withFileTypes: true })
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const projectDir = path.join(COOKBOOK_DIR, entry.name)
        const readmePath = path.join(projectDir, 'README.md')
        console.log(`\n${entry.name}:`)

        try {
          // Check if README.md exists and is readable
          await fs.access(readmePath, fs.constants.R_OK)
          const readmeContent = await fs.readFile(readmePath, 'utf-8')

          const { projectName, shortDescription } = extractProjectDetails(readmeContent, entry.name)
          console.log(`\t${projectName}`)
          console.log(`\t>> ${shortDescription}`)

          const projectData = {
            name: projectName,
            description: shortDescription,
            readmeContent: readmeContent,
            dirName: entry.name, // Original directory name for context
          }

          if (entry.name.startsWith('python-')) {
            pythonProjects.push(projectData)
          } else if (entry.name.startsWith('typescript-')) {
            typescriptProjects.push(projectData)
          }
          // Other directories are ignored unless they match the naming convention
        } catch (readmeError) {
          // README.md doesn't exist, is not readable, or other error during processing
          if (readmeError.code === 'ENOENT') {
            console.warn(`Skipping ${projectDir}: README.md not found.`)
          } else {
            console.warn(`Skipping ${projectDir}: Error processing README.md - ${readmeError.message}`)
          }
        }
      }
    }

    // Sort projects alphabetically by dirName for consistent ordering
    pythonProjects.sort((a, b) => a.dirName.localeCompare(b.dirName))
    typescriptProjects.sort((a, b) => a.dirName.localeCompare(b.dirName))

    const pythonMarkdown = generateMarkdown('Python Examples', pythonProjects)
    const typescriptMarkdown = generateMarkdown('TypeScript Examples', typescriptProjects)

    await fs.writeFile(PYTHON_EXAMPLES_FILE, pythonMarkdown)
    console.log(`Successfully generated ${PYTHON_EXAMPLES_FILE}`)
    await fs.writeFile(TYPESCRIPT_EXAMPLES_FILE, typescriptMarkdown)
    console.log(`Successfully generated ${TYPESCRIPT_EXAMPLES_FILE}`)
  } catch (error) {
    console.error('Error generating example pages:', error)
    process.exit(1) // Exit with error code
  }
}

main()
