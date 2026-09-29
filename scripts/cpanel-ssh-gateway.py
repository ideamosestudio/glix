#!/usr/bin/env python3
"""Forced command for the dedicated Glix GitHub SSH key; install outside the webroot."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

home=Path.home()
repo=home/'repositories/glix'
state=home/'.glix-mirror'
command=os.environ.get('SSH_ORIGINAL_COMMAND','')

def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()

if command=='glix-status':
    manifest=json.loads((state/'manifest.json').read_text(encoding='utf-8'))
    for name,expected in manifest['files'].items():
        path=home/'public_html'/name
        if path.is_symlink() or (home/'public_html').resolve() not in path.resolve().parents:
            raise SystemExit('Unexpected managed file path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise SystemExit('Mirror verification failed: '+name)
    print(json.dumps({'revision':manifest['revision'],'repository_revision':git('rev-parse','HEAD'),'files':len(manifest['files']),'verified':True}))
    raise SystemExit(0)
match=re.fullmatch(r'glix-(sync|dry-run) ([a-f0-9]{40})',command)
if not match:raise SystemExit('Only glix-sync, glix-dry-run and glix-status are allowed')
operation,expected=match.groups()
if repo.is_symlink():raise SystemExit('Repository must not be a symlink')
state.mkdir(mode=0o700,exist_ok=True)
lock=state/'sync.lock'
lock.mkdir(mode=0o700)
try:
    if git('remote','get-url','origin')!='https://github.com/ideamosestudio/glix.git':
        raise SystemExit('Unexpected source repository')
    if git('status','--porcelain','--untracked-files=no'):
        raise SystemExit('Tracked server files were modified; refusing to overwrite them')
    git('fetch','origin','main')
    latest=git('rev-parse','origin/main')
    if latest!=expected:
        print(json.dumps({'skipped':'superseded by newer main commit','requested':expected,'latest':latest}))
        raise SystemExit(0)
    git('checkout','main')
    git('merge','--ff-only','origin/main')
    subprocess.run(['/usr/bin/python3',str(repo/'scripts/check-site.py')],check=True)
    args=['/usr/bin/python3',str(repo/'scripts/deploy-cpanel.py')]
    if operation=='dry-run':args.append('--dry-run')
    subprocess.run(args,check=True)
finally:lock.rmdir()
