import { NextResponse } from 'next/server'
import { execSync } from 'child_process'
import { resolve } from 'path'
import { getFileContent, getDirectory, updateFile, deleteDirectory } from '@/lib/github'

function getRepoSlug(): string {
  if (process.env.GITHUB_REPO) return process.env.GITHUB_REPO
  try {
    const url = execSync('git remote get-url origin', { stdio: 'pipe', cwd: resolve(process.cwd(), '..') }).toString().trim()
    // https://github.com/owner/repo.git or git@github.com:owner/repo.git
    const m = url.match(/github\.com[/:]([\w.-]+\/[\w.-]+?)(?:\.git)?$/)
    return m ? m[1] : ''
  } catch {
    return ''
  }
}

function parseModel(yaml: string): string {
  const match = yaml.match(/^model:\s*(\S+)/m)
  return match?.[1] || 'claude-sonnet-4-6'
}

function parseJsonrenderEnabled(yaml: string): boolean {
  const match = yaml.match(/channels:\s*\n\s+jsonrender:\s*\n\s+enabled:\s*(true|false)/)
  return match?.[1] === 'true'
}

function parseConfig(yaml: string): Record<string, { enabled: boolean; schedule: string; var: string; model: string }> {
  const skills: Record<string, { enabled: boolean; schedule: string; var: string; model: string }> = {}

  // Support inline format: skill-name: { enabled: true, schedule: "..." }
  const inlineRegex = /^ {2}([a-z][a-z0-9-]*):\s*\{([^}]+)\}/gm
  let match
  while ((match = inlineRegex.exec(yaml)) !== null) {
    const name = match[1]
    const block = match[2]
    skills[name] = {
      enabled: /enabled:\s*true/.test(block),
      schedule: block.match(/schedule:\s*"([^"]*)"/)?.[ 1] || '',
      var: block.match(/var:\s*"([^"]*)"/)?.[ 1] || '',
      model: block.match(/model:\s*"([^"]*)"/)?.[ 1] || '',
    }
  }

  // Support multi-line format: skill-name:\n    enabled: true\n    schedule: "..."
  const multilineRegex = / {2}([a-z][a-z0-9-]*):\s*\n((?:\s{4}\S.*\n)*)/g
  while ((match = multilineRegex.exec(yaml)) !== null) {
    const name = match[1]
    if (skills[name]) continue // inline already parsed
    const block = match[2]
    skills[name] = {
      enabled: /enabled:\s*true/.test(block),
      schedule: block.match(/schedule:\s*"([^"]*)"/)?.[ 1] || '',
      var: block.match(/var:\s*"([^"]*)"/)?.[ 1] || '',
      model: block.match(/model:\s*"([^"]*)"/)?.[ 1] || '',
    }
  }
  return skills
}

function extractDescription(content: string): string {
  const fm = content.match(/^---\s*\n([\s\S]*?)\n---/)
  if (fm) {
    const desc = fm[1].match(/description:\s*(.+)/)
    if (desc) return desc[1].trim().replace(/^['"]|['"]$/g, '')
  }
  for (const line of content.split('\n')) {
    const t = line.trim()
    if (t && !t.startsWith('#') && !t.startsWith('---')) {
      return t.length > 120 ? t.slice(0, 117) + '...' : t
    }
  }
  return ''
}

function escapeRe(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

export async function GET() {
  try {
    const [configResult, skillDirs] = await Promise.all([
      getFileContent('aeon.yml'),
      getDirectory('skills'),
    ])
    const config = parseConfig(configResult.content)
    const dirNames = skillDirs.filter(d => d.type === 'dir').map(d => d.name)

    const descs = await Promise.all(
      dirNames.map(async (name) => {
        try {
          const { content } = await getFileContent(`skills/${name}/SKILL.md`)
          return { name, description: extractDescription(content) }
        } catch {
          return { name, description: '' }
        }
      }),
    )

    const skills = dirNames.map(name => ({
      name,
      description: descs.find(d => d.name === name)?.description || '',
      enabled: config[name]?.enabled ?? false,
      schedule: config[name]?.schedule || '0 12 * * *',
      var: config[name]?.var || '',
      model: config[name]?.model || '',
    }))

    const model = parseModel(configResult.content)
    const repo = getRepoSlug()
    const jsonrenderEnabled = parseJsonrenderEnabled(configResult.content)
    return NextResponse.json({ skills, model, repo, jsonrenderEnabled })
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Unknown error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}

export async function PATCH(request: Request) {
  try {
    const { name, enabled, schedule, var: skillVar, model, skillModel, jsonrenderEnabled } = await request.json()
    const { content, sha } = await getFileContent('aeon.yml')
    let updated = content

    // Update jsonrender enabled flag
    if (typeof jsonrenderEnabled === 'boolean') {
      const hasChannels = /channels:\s*\n\s+jsonrender:\s*\n\s+enabled:\s*(true|false)/.test(updated)
      if (hasChannels) {
        updated = updated.replace(
          /(channels:\s*\n\s+jsonrender:\s*\n\s+enabled:\s*)(true|false)/,
          `$1${jsonrenderEnabled}`
        )
      } else {
        // Append channels section before telegram section or at end
        const channelsBlock = `\n# Output channels\nchannels:\n  jsonrender:\n    enabled: ${jsonrenderEnabled}\n`
        const telegramIdx = updated.indexOf('\ntelegram:')
        if (telegramIdx !== -1) {
          updated = updated.slice(0, telegramIdx) + channelsBlock + updated.slice(telegramIdx)
        } else {
          updated += channelsBlock
        }
      }
    }

    // Update top-level model field
    if (typeof model === 'string' && model) {
      updated = updated.replace(/^model:\s*\S+/m, `model: ${model}`)
    }

    if (name && (typeof enabled === 'boolean' || typeof schedule === 'string' || typeof skillVar === 'string' || typeof skillModel === 'string')) {
      const escaped = escapeRe(name)
      // Match inline format:  skill-name: { enabled: true, schedule: "...", var: "..." }
      const inlineRe = new RegExp(`(  ${escaped}:\\s*)\\{([^}]+)\\}`)
      const inlineMatch = updated.match(inlineRe)

      if (inlineMatch) {
        let block = inlineMatch[2]
        if (typeof enabled === 'boolean') {
          block = block.replace(/enabled:\s*(true|false)/, `enabled: ${enabled}`)
        }
        if (typeof schedule === 'string' && schedule) {
          block = block.replace(/schedule:\s*"[^"]*"/, `schedule: "${schedule}"`)
        }
        if (typeof skillVar === 'string') {
          if (/var:\s*"/.test(block)) {
            block = block.replace(/var:\s*"[^"]*"/, skillVar ? `var: "${skillVar}"` : '')
            block = block.replace(/,\s*,/g, ',').replace(/\{\s*,/, '{').replace(/,\s*\}/, '}').replace(/,(\s*)$/, '$1')
          } else if (skillVar) {
            block = block.replace(/\s*$/, `, var: "${skillVar}"`)
          }
        }
        if (typeof skillModel === 'string') {
          if (/model:\s*"/.test(block)) {
            block = block.replace(/model:\s*"[^"]*"/, skillModel ? `model: "${skillModel}"` : '')
            block = block.replace(/,\s*,/g, ',').replace(/\{\s*,/, '{').replace(/,\s*\}/, '}').replace(/,(\s*)$/, '$1')
          } else if (skillModel) {
            block = block.replace(/\s*$/, `, model: "${skillModel}"`)
          }
        }
        updated = updated.replace(inlineRe, `$1{${block}}`)
      } else {
        // Multi-line format fallback
        if (typeof enabled === 'boolean') {
          const re = new RegExp(`(  ${escaped}:\\n    enabled: )(true|false)`)
          updated = updated.replace(re, `$1${enabled}`)
        }
        if (typeof schedule === 'string' && schedule) {
          const re = new RegExp(`(  ${escaped}:\\n    enabled: (?:true|false)\\n    schedule: ")[^"]*"`)
          updated = updated.replace(re, `$1${schedule}"`)
        }
        if (typeof skillVar === 'string') {
          const hasVar = new RegExp(`  ${escaped}:[\\s\\S]*?var: "`)
          if (hasVar.test(updated)) {
            const re = new RegExp(`(  ${escaped}:\\n    enabled: (?:true|false)\\n    schedule: "[^"]*"\\n    var: ")[^"]*"`)
            updated = updated.replace(re, `$1${skillVar}"`)
          } else if (skillVar) {
            const re = new RegExp(`(  ${escaped}:\\n    enabled: (?:true|false)\\n    schedule: "[^"]*")`)
            updated = updated.replace(re, `$1\n    var: "${skillVar}"`)
          }
        }
        if (typeof skillModel === 'string') {
          const hasModel = new RegExp(`  ${escaped}:[\\s\\S]*?model: "`)
          if (hasModel.test(updated)) {
            if (skillModel) {
              const re = new RegExp(`(  ${escaped}:\\n(?:    \\S.*\\n)*?    model: ")[^"]*"`)
              updated = updated.replace(re, `$1${skillModel}"`)
            } else {
              const re = new RegExp(`(  ${escaped}:\\n(?:    \\S.*\\n)*?)    model: "[^"]*"\\n`)
              updated = updated.replace(re, '$1')
            }
          } else if (skillModel) {
            const hasVar = new RegExp(`  ${escaped}:[\\s\\S]*?var: "`)
            if (hasVar.test(updated)) {
              const re = new RegExp(`(  ${escaped}:\\n    enabled: (?:true|false)\\n    schedule: "[^"]*"\\n    var: "[^"]*")`)
              updated = updated.replace(re, `$1\n    model: "${skillModel}"`)
            } else {
              const re = new RegExp(`(  ${escaped}:\\n    enabled: (?:true|false)\\n    schedule: "[^"]*")`)
              updated = updated.replace(re, `$1\n    model: "${skillModel}"`)
            }
          }
        }
      }
    }

    if (updated !== content) {
      const msg = model ? `chore: set model to ${model}` : typeof jsonrenderEnabled === 'boolean' ? `chore: ${jsonrenderEnabled ? 'enable' : 'disable'} json-render channel` : `chore: update ${name} config`
      await updateFile('aeon.yml', updated, sha, msg)
    }

    return NextResponse.json({ ok: true })
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Unknown error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}

export async function DELETE(request: Request) {
  try {
    const { name } = await request.json()
    if (!name || !/^[a-z][a-z0-9-]*$/.test(name)) {
      return NextResponse.json({ error: 'Invalid skill name' }, { status: 400 })
    }

    // Delete skill directory
    await deleteDirectory(`skills/${name}`, `chore: delete ${name} skill`)

    // Remove from aeon.yml
    try {
      const { content, sha } = await getFileContent('aeon.yml')
      // Match inline format:  skill-name: { ... }  # optional comment\n
      const inlineRe = new RegExp(`  ${escapeRe(name)}:\\s*\\{[^}]*\\}[^\\n]*\\n?`)
      // Match multi-line format
      const multiRe = new RegExp(`  ${escapeRe(name)}:\\n(?:    \\S.*\\n)*(?:\\n(?=  [a-z]|  #|\\n|[a-z]|$))?`)
      let updated = content
      if (inlineRe.test(updated)) {
        updated = updated.replace(inlineRe, '')
      } else {
        updated = updated.replace(multiRe, '')
      }
      if (updated !== content) {
        await updateFile('aeon.yml', updated, sha, `chore: remove ${name} from config`)
      }
    } catch { /* config cleanup is best-effort */ }

    return NextResponse.json({ ok: true })
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Unknown error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
