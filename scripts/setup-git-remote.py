import subprocess

token = subprocess.check_output(['gh', 'auth', 'token']).decode().strip()
url = f'https://x-access-token:{token}@github.com/aaronjmars/aeon-website.git'
subprocess.run(['git', '-C', '/home/runner/work/aeon-agent/docs-sync-work', 'remote', 'set-url', 'origin', url], check=True)
print('Remote URL set with token')
