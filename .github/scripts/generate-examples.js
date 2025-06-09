/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2025, Victor Duarte (zvictor)
 */
import fs from 'fs/promises'
import path from 'path'

const REPOSITORY = 'https://github.com/zvictor/brainyflow'
const COOKBOOK_DIR = 'cookbook'
const OUTPUT_DIR = 'docs/cookbook' // Directory where generated files will be saved
const PYTHON_EXAMPLES_FILE = path.join(OUTPUT_DIR, 'python.md')
const TYPESCRIPT_EXAMPLES_FILE = path.join(OUTPUT_DIR, 'typescript.md')
const COMPLEXITY_SCALE = ['🥚', '🐣', '🐥', '🐓', '🦕', '🦖', '☄️', '🐭', '🐒', '🧠', '⚙️', '🤖', '👾', '🛸', '🌌']
const POINTS_SYSTEM = await fs.readFile(path.join(OUTPUT_DIR, 'points.md'), 'utf-8')

/**
 * Parses basic frontmatter to extract complexity and title.
 * @param {string} readmeContent - The full content of the README.md file.
 * @returns {{complexity: number|null, title: string|null, contentWithoutFrontmatter: string}}
 */
function parseFrontmatter(readmeContent) {
  let complexity = null
  let title = null
  let contentWithoutFrontmatter = readmeContent

  const fmMatch = readmeContent.match(/^---\s*\n([\s\S]*?)\n---\s*\n/)
  if (fmMatch && fmMatch[1]) {
    const fmContent = fmMatch[1]
    contentWithoutFrontmatter = readmeContent.substring(fmMatch[0].length) // Store content after frontmatter

    // Simple parsing for 'complexity'
    const complexityMatch = fmContent.match(/^\s*complexity:\s*([\d.]+)\s*$/m)
    if (complexityMatch && complexityMatch[1]) {
      const parsedComplexity = parseFloat(complexityMatch[1])
      if (!isNaN(parsedComplexity)) {
        complexity = parsedComplexity
      }
    }

    // Simple parsing for 'title' (optional, not used for project name in this version)
    const titleMatch = fmContent.match(/^\s*title:\s*(.+?)\s*$/m)
    if (titleMatch && titleMatch[1]) {
      title = titleMatch[1].trim()
    }
  }
  return { complexity, title, contentWithoutFrontmatter }
}

/**
 * Extracts project name and short description from README content.
 * @param {string} readmeContent - The content of the README.md file.
 * @param {string} defaultProjectName - Fallback project name if not found in README.
 * @returns {{projectName: string, shortDescription: string}}
 */
function extractProjectDetails(readmeContent, defaultProjectName) {
  let projectName = defaultProjectName
  let shortDescription = `Details are not available for ${defaultProjectName}.` // Default description

  const lines = readmeContent.split('\n')

  // Extract Project Name from the first H1 heading
  const firstH1Index = lines.findIndex((line) => line.startsWith('# '))
  if (firstH1Index !== -1) {
    projectName = lines[firstH1Index].substring(2).trim()
    // Update default description if project name is found
    shortDescription = `Details are not available for ${projectName}.`

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
 * @param {string} pageTitle - The title for the Markdown page (e.g., "Python Examples").
 * @param {Array<{name: string, description: string, readmeContent: string, dirName: string, complexity: number|null}>} projects - Array of project objects.
 * @returns {string} - The generated Markdown content.
 */
function generateMarkdown(pageTitle, projects) {
  const maxComplexity = Math.max(...projects.map((x) => x.complexity))
  const minComplexity = Math.min(...projects.map((x) => x.complexity))

  let markdown = `---\ntitle: '${pageTitle.replace(/'/g, "\\'")}'\nmachine-display: false\n---\n\n`
  markdown += `# ${pageTitle}\n\n`
  markdown += `All projects listed below can be found in our [cookbook directory](${REPOSITORY}/${path.join('tree/main', COOKBOOK_DIR)}).\n`
  markdown += `\nThey have been sorted by [complexity points](#the-complexity-points-system) - _which are represented by the scale ${COMPLEXITY_SCALE.join('→')}_ - to help you easily find projects that suit your skills.\n\n`
  if (projects.length === 0) {
    markdown += 'No examples found for this category yet.\n'
    return markdown
  }

  projects.forEach((project) => {
    // Escape HTML special characters in project name and description for the summary
    const escapedName = project.name.replace(/</g, '&lt;').replace(/>/g, '&gt;')
    const escapedDescription = project.description.replace(/</g, '&lt;').replace(/>/g, '&gt;')
    const ratio = (project.complexity - minComplexity) / (maxComplexity - minComplexity)
    let normalizedIndex = Math.round(ratio * (COMPLEXITY_SCALE.length - 1))
    // Clamp the index to be safe
    normalizedIndex = Math.max(0, Math.min(normalizedIndex, Math.min(projects.length, COMPLEXITY_SCALE.length - 1)))

    markdown += `## ${escapedName} ([${project.dirName}](${REPOSITORY}/${path.join('tree/main', COOKBOOK_DIR, project.dirName)}))\n`
    markdown += `Complexity Points: ${project.complexity}\n└${COMPLEXITY_SCALE[normalizedIndex].repeat(normalizedIndex + 1)}\n\n`
    markdown += escapedDescription
    markdown += `<details>\n`
    markdown += `<summary><strong>Details</strong></summary>\n\n`
    markdown += `\n`
    markdown += `${project.readmeContent}\n\n`
    markdown += `</details>\n\n`
  })

  markdown += `![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)\n`
  markdown += `# The Complexity Points System\n`
  markdown += `All listed projects had their calculation automatically calculated.\nClick \`Details\` below for more information in the points system.\n`
  markdown += `<details>\n<summary><strong>Details</strong></summary>\n\n`
  markdown += `\n`
  markdown += POINTS_SYSTEM
  markdown += `</details>\n\n`
  return markdown
}

/**
 * Main function to generate example pages.
 */
async function main() {
  try {
    await fs.mkdir(OUTPUT_DIR, { recursive: true })

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
          const fullReadmeContent = await fs.readFile(readmePath, 'utf-8')

          const { complexity, contentWithoutFrontmatter } = parseFrontmatter(fullReadmeContent)
          const { projectName, shortDescription } = extractProjectDetails(contentWithoutFrontmatter, entry.name)
          console.log(`\t${projectName}`, complexity ? `[complexity:${complexity}]` : '')
          console.log(`\t>> ${shortDescription}`)

          const projectData = {
            name: projectName,
            description: shortDescription,
            readmeContent: contentWithoutFrontmatter, // Store the "clean" README for the details view
            dirName: entry.name,
            complexity,
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

    // Sort projects: first by complexity (nulls/undefined last), then by dirName
    const compareProjects = (a, b) => {
      const complexityA = a.complexity === null ? Number.MAX_SAFE_INTEGER : a.complexity
      const complexityB = b.complexity === null ? Number.MAX_SAFE_INTEGER : b.complexity

      if (complexityA !== complexityB) {
        return complexityA - complexityB
      }
      return a.dirName.localeCompare(b.dirName)
    }

    pythonProjects.sort(compareProjects)
    typescriptProjects.sort(compareProjects)

    const pythonMarkdown = generateMarkdown('Python Examples', pythonProjects)
    const typescriptMarkdown = generateMarkdown('TypeScript Examples', typescriptProjects)
    const cookbookMarkdown = generateMarkdown('Cookbook', [...typescriptProjects, ...pythonProjects].sort(compareProjects))

    await fs.writeFile(PYTHON_EXAMPLES_FILE, pythonMarkdown)
    console.log(`\n\nSuccessfully generated ${PYTHON_EXAMPLES_FILE}`)
    await fs.writeFile(TYPESCRIPT_EXAMPLES_FILE, typescriptMarkdown)
    console.log(`Successfully generated ${TYPESCRIPT_EXAMPLES_FILE}`)
    await fs.writeFile(path.join(COOKBOOK_DIR, 'README.md'), cookbookMarkdown)
    console.log(`Successfully generated ${path.join(COOKBOOK_DIR, 'README.md')}`)
  } catch (error) {
    console.error('Error generating example pages:', error)
    process.exit(1)
  }
}

main()
