import { NextResponse } from 'next/server'
import { execSync } from 'child_process'
import { resolve } from 'path'

const REPO_ROOT = resolve(process.cwd(), '..')

export async function GET() {
  try {
    const out = execSync(
      'gh run list --json databaseId,name,status,conclusion,createdAt,url,displayTitle --limit 20',
      { stdio: 'pipe', cwd: REPO_ROOT },
    ).toString()
    const raw = JSON.parse(out)
    const runs = raw.map((r: Record<string, unknown>) => ({
      id: r.databaseId,
      workflow: r.displayTitle || r.name,
      status: r.status,
      conclusion: r.conclusion,
      created_at: r.createdAt,
      url: r.url,
    }))
    return NextResponse.json({ runs })
  } catch {
    return NextResponse.json({ runs: [] })
  }
}
