import { readFile, writeFile, readdir, mkdir, stat, rm } from 'fs/promises'
import { join, resolve } from 'path'

const GITHUB_API = 'https://api.github.com'

// Resolve the repo root (one level up from dashboard/)
const REPO_ROOT = resolve(process.cwd(), '..')

function isLocal() {
  return !process.env.GITHUB_TOKEN || !process.env.GITHUB_REPO
}

function getConfig() {
  const token = process.env.GITHUB_TOKEN!
  const repo = process.env.GITHUB_REPO!
  return { token, repo }
}

function authHeaders(token: string) {
  return {
    Authorization: `Bearer ${token}`,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
  }
}

// --- Unified interface: local filesystem or GitHub API ---

export async function getFileContent(path: string): Promise<{ content: string; sha: string }> {
  if (isLocal()) {
    const content = await readFile(join(REPO_ROOT, path), 'utf-8')
    return { content, sha: '' }
  }
  const { token, repo } = getConfig()
  const res = await fetch(`${GITHUB_API}/repos/${repo}/contents/${path}`, {
    headers: authHeaders(token),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to read ${path}`)
  const data = await res.json()
  return {
    content: Buffer.from(data.content, 'base64').toString('utf-8'),
    sha: data.sha as string,
  }
}

export async function updateFile(path: string, content: string, sha: string, _message: string) {
  if (isLocal()) {
    await writeFile(join(REPO_ROOT, path), content, 'utf-8')
    return { ok: true }
  }
  const { token, repo } = getConfig()
  const res = await fetch(`${GITHUB_API}/repos/${repo}/contents/${path}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify({
      message: _message,
      content: Buffer.from(content).toString('base64'),
      sha,
    }),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to update ${path}`)
  return res.json()
}

export async function createFile(path: string, content: string, message: string) {
  if (isLocal()) {
    const fullPath = join(REPO_ROOT, path)
    await mkdir(join(fullPath, '..'), { recursive: true })
    await writeFile(fullPath, content, 'utf-8')
    return { ok: true }
  }
  const { token, repo } = getConfig()
  try {
    const existing = await getFileContent(path)
    return updateFile(path, content, existing.sha, message)
  } catch {
    // File doesn't exist — create it
  }
  const res = await fetch(`${GITHUB_API}/repos/${repo}/contents/${path}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify({
      message,
      content: Buffer.from(content).toString('base64'),
    }),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to create ${path}`)
  return res.json()
}

export async function getDirectory(path: string): Promise<Array<{ name: string; type: string; path: string }>> {
  if (isLocal()) {
    const fullPath = join(REPO_ROOT, path)
    try {
      const entries = await readdir(fullPath, { withFileTypes: true })
      return entries.map(e => ({
        name: e.name,
        type: e.isDirectory() ? 'dir' : 'file',
        path: join(path, e.name),
      }))
    } catch {
      return []
    }
  }
  const { token, repo } = getConfig()
  const res = await fetch(`${GITHUB_API}/repos/${repo}/contents/${path}`, {
    headers: authHeaders(token),
    cache: 'no-store',
  })
  if (!res.ok) return []
  const data = await res.json()
  return Array.isArray(data) ? data : []
}

export async function triggerWorkflow(skill: string) {
  if (isLocal()) {
    throw new Error('Cannot trigger GitHub Actions locally — set GITHUB_TOKEN and GITHUB_REPO to enable remote runs')
  }
  const { token, repo } = getConfig()
  const res = await fetch(`${GITHUB_API}/repos/${repo}/actions/workflows/aeon.yml/dispatches`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({ ref: 'main', inputs: { skill } }),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to trigger workflow`)
}

export async function getWorkflowRuns(perPage = 20) {
  if (isLocal()) {
    // Return empty — no GitHub Actions access locally
    return []
  }
  const { token, repo } = getConfig()
  const res = await fetch(
    `${GITHUB_API}/repos/${repo}/actions/runs?per_page=${perPage}`,
    { headers: authHeaders(token), cache: 'no-store' },
  )
  if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to fetch runs`)
  const data = await res.json()
  return data.workflow_runs || []
}

// --- Remote repo helpers (for importing skills) ---

export async function getRemoteDirectory(remoteRepo: string, path: string): Promise<Array<{ name: string; type: string }>> {
  // Always uses GitHub API (remote repo)
  const headers: Record<string, string> = { Accept: 'application/vnd.github+json' }
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`
  }
  const url = path
    ? `${GITHUB_API}/repos/${remoteRepo}/contents/${path}`
    : `${GITHUB_API}/repos/${remoteRepo}/contents`
  const res = await fetch(url, { headers, cache: 'no-store' })
  if (!res.ok) return []
  const data = await res.json()
  return Array.isArray(data) ? data : []
}

export async function getRemoteFileContent(remoteRepo: string, path: string): Promise<string | null> {
  const headers: Record<string, string> = { Accept: 'application/vnd.github+json' }
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`
  }
  const res = await fetch(`${GITHUB_API}/repos/${remoteRepo}/contents/${path}`, {
    headers,
    cache: 'no-store',
  })
  if (!res.ok) return null
  const data = await res.json()
  return Buffer.from(data.content, 'base64').toString('utf-8')
}

export async function deleteDirectory(path: string, message: string): Promise<void> {
  if (isLocal()) {
    await rm(join(REPO_ROOT, path), { recursive: true, force: true })
    return
  }
  const { token, repo } = getConfig()
  // GitHub API requires deleting files one by one
  const files = await getDirectory(path)
  for (const file of files) {
    if (file.type === 'dir') {
      await deleteDirectory(`${path}/${file.name}`, message)
    } else {
      const { sha } = await getFileContent(`${path}/${file.name}`)
      const res = await fetch(`${GITHUB_API}/repos/${repo}/contents/${path}/${file.name}`, {
        method: 'DELETE',
        headers: authHeaders(token),
        body: JSON.stringify({ message, sha }),
        cache: 'no-store',
      })
      if (!res.ok) throw new Error(`GitHub API ${res.status}: failed to delete ${path}/${file.name}`)
    }
  }
}

export async function fileExists(path: string): Promise<boolean> {
  if (isLocal()) {
    try {
      await stat(join(REPO_ROOT, path))
      return true
    } catch {
      return false
    }
  }
  try {
    await getFileContent(path)
    return true
  } catch {
    return false
  }
}
