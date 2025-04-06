#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define file paths relative to the repository root
OUTPUT_FILE="gh-pages-content/docs.txt"
SUMMARY_FILE="docs/SUMMARY.md"
DOCS_DIR="docs"

# Ensure the output directory exists (it's created in the workflow step before this script runs)
# mkdir -p "$(dirname "$OUTPUT_FILE")" # This is handled by the workflow step

# Clear the output file if it exists, or create it if it doesn't
> "$OUTPUT_FILE"

echo "Starting documentation concatenation..."
echo "Output file: $OUTPUT_FILE"
echo "Summary file: $SUMMARY_FILE"
echo "Docs directory: $DOCS_DIR"

# Check if SUMMARY_FILE exists
if [ ! -f "$SUMMARY_FILE" ]; then
  echo "Error: Summary file not found at $SUMMARY_FILE"
  exit 1
fi

# Extract markdown file paths from SUMMARY.md, filter, and process
# - grep -oE: Extracts relative paths like 'getting_started.md' or 'core_abstraction/nodes.md'
# - sed: Cleans up the extracted path
# - grep -vE: Filters out paths starting with 'utility_function/'
grep -oE '\[.*\]\(([^)]+\.md)\)' "$SUMMARY_FILE" | \
sed -E 's/\[.*\]\(([^)]+\.md)\)/\1/' | \
grep -vE '^utility_function/' | \
while IFS= read -r filepath; do
  # Construct the full path relative to the repository root
  fullpath="$DOCS_DIR/$filepath"

  if [ -f "$fullpath" ]; then
    # Check for 'machine-display: false' in YAML frontmatter using awk
    # awk logic: f=0 initially. See '---', f=1. Inside frontmatter (f==1), if line matches, print "ignore" and exit (found). See second '---', f=2, exit.
    if awk '/^---$/{f++} f==1 && /^\s*machine-display:\s*false\s*$/{print "ignore"; exit} f>=2{exit}' "$fullpath" | grep -q "ignore"; then
      echo "Skipping (machine-display: false): $fullpath"
    else
      echo "Processing: $fullpath"
      # Add a header indicating the file origin
      printf "\n\n================================================\nFile: %s\n================================================\n" "$fullpath" >> "$OUTPUT_FILE"
      # Append the file content
      cat "$fullpath" >> "$OUTPUT_FILE"
      # Add extra newlines for separation
      printf "\n\n" >> "$OUTPUT_FILE"
    fi
  else
    # Log a warning if a file listed in SUMMARY.md is not found
    echo "Warning: File not found in $DOCS_DIR - $filepath (referenced in $SUMMARY_FILE, skipped)"
  fi
done

echo "Finished concatenating files based on $SUMMARY_FILE into $OUTPUT_FILE"
