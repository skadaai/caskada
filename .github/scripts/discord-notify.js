/**
 * Posts a message to Discord webhook
 * @param {string} webhookUrl - Discord webhook URL
 * @param {Object} releaseInfo - { packageName, version, changelog, repositoryUrl }
 */
export async function notifyDiscord(webhookUrl, releaseInfo) {
  const { packageName, version, changelog, repositoryUrl } = releaseInfo

  const embed = {
    title: `🚀 Brainyflow ${packageName} v${version} Released!`,
    description: changelog.substring(0, 2000), // Discord embed description limit
    color: packageName.toLowerCase() === 'typescript' ? 0x3178c6 : 0x3776ab, // TS blue or Python blue
    fields: [
      {
        name: 'Package',
        value: packageName,
        inline: true,
      },
      {
        name: 'Version',
        value: version,
        inline: true,
      },
    ],
    footer: {
      text: 'BrainyFlow Release Bot',
    },
    timestamp: new Date().toISOString(),
  }

  if (repositoryUrl) {
    embed.url = `${repositoryUrl}/releases/tag/${packageName.toLowerCase()}-v${version}`
  }

  const payload = {
    embeds: [embed],
  }

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error(`Discord webhook failed: ${response.status} ${response.statusText}`)
    }

    console.log('Successfully posted to Discord!')
  } catch (error) {
    console.error('Error posting to Discord:', error)
    throw error
  }
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const webhookUrl = process.argv[2]
  const packageName = process.argv[3]
  const version = process.argv[4]
  const changelog = process.argv[5] || `Release ${version}`
  const repositoryUrl = process.argv[6]

  if (!webhookUrl || !packageName || !version) {
    console.error('Usage: node discord-notify.js <webhookUrl> <packageName> <version> [changelog] [repositoryUrl]')
    process.exit(1)
  }

  await notifyDiscord(webhookUrl, { packageName, version, changelog, repositoryUrl })
}
