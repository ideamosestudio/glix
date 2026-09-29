#!/usr/bin/env python3
"""Copy tracked site files into public_html, preserving unrelated hosting files."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def website_file(name):
    parts=PurePosixPath(name).parts
    if not parts or name.startswith('/') or '\\' in name or any(p in ('.','..') or p.startswith('.') for p in parts):
        return False
    suffix=Path(name).suffix.lower()
    return (parts[0]=='assets' and len(parts)>1 and suffix in
            ('.png','.jpg','.jpeg','.webp','.avif','.gif','.svg','.ico','.woff','.woff2','.ttf','.otf','.css','.js','.json','.txt','.pdf','.mp4','.webm')) or (
        len(parts)==1 and (suffix in ('.html','.css','.js','.png','.svg','.ico') or name in ('robots.txt','sitemap.xml')))


def safe_path(root,name):
    if not website_file(name):raise ValueError('Non-website path rejected: '+name)
    candidate=root
    for part in PurePosixPath(name).parts:
        candidate=candidate/part
        if candidate.is_symlink():raise ValueError('Symbolic link rejected: '+name)
    if os.path.commonpath((str(root.resolve()),str(candidate.resolve())))!=str(root.resolve()):
        raise ValueError('Path leaves its allowed directory')
    if candidate.exists() and not candidate.is_file():raise ValueError('Expected a regular file: '+name)
    return candidate


def atomic_copy(source,destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix='.glix-copy-',dir=str(destination.parent))
    try:
        with os.fdopen(fd,'wb') as out,source.open('rb') as inp:shutil.copyfileobj(inp,out)
        os.chmod(temp,0o644)
        os.replace(temp,destination)
    finally:
        if os.path.exists(temp):os.unlink(temp)


def _deploy(repo,home,revision,names,dry_run):
    target=home/'public_html'
    state=home/'.glix-mirror'
    manifest_path=state/'manifest.json'
    if manifest_path.is_symlink():raise ValueError('Manifest cannot be a symlink')
    old=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'files':{}}
    names=sorted(set(name for name in names if website_file(name)))
    if 'index.html' not in names:raise ValueError('Site must contain index.html')
    current={name:digest(safe_path(repo,name)) for name in names}
    for name in set(current)|set(old['files']):safe_path(target,name)
    changed=[name for name in names if not (target/name).exists() or digest(target/name)!=current[name]]
    removed=[name for name in old['files'] if name not in current and (target/name).exists()]
    for name in removed:
        if digest(target/name)!=old['files'][name]:
            raise ValueError('Obsolete managed file was modified outside Git; preserve and review: '+name)
    result={'revision':revision,'files':len(current),'changed':len(changed),'removed':len(removed)}
    if dry_run:return dict(result,dry_run=True)
    if (state/'backups').is_symlink():raise ValueError('Backup directory cannot be a symlink')
    backup=state/'backups'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+revision[:12])
    existing=[]
    if changed or removed:
        backup.mkdir(parents=True,mode=0o700)
    for name in changed+removed:
        dest=target/name
        if dest.exists():
            copy=backup/name
            copy.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(dest,copy)
            existing.append(name)
    touched=[]
    try:
        for name in changed:
            atomic_copy(repo/name,target/name)
            touched.append(name)
        for name in removed:
            (target/name).unlink()
            touched.append(name)
        if any(digest(target/name)!=value for name,value in current.items()):
            raise RuntimeError('Content verification failed')
        protected={}
        snapshot=state/'hosting-before.json'
        if not old['files'] and snapshot.exists():
            protected=json.loads(snapshot.read_text(encoding='utf-8'))
            for name,value in protected.items():
                original=target/name
                if original.is_symlink() or target.resolve() not in original.resolve().parents or digest(original)!=value:
                    raise RuntimeError('Hosting configuration changed during initial deployment')
        result['protected_files_checked']=len(protected)
        temporary=state/'manifest.next.json'
        if temporary.is_symlink():raise ValueError('Temporary manifest cannot be a symlink')
        temporary.write_text(json.dumps({'revision':revision,'files':current},indent=2),encoding='utf-8')
        os.chmod(temporary,0o600)
        os.replace(temporary,manifest_path)
    except Exception:
        for name in reversed(touched):
            if name in existing:atomic_copy(backup/name,target/name)
            elif (target/name).exists():(target/name).unlink()
        raise
    return dict(result,verified=True)


def deploy(repo,home,revision,names,dry_run=False):
    home=home.resolve()
    target=home/'public_html'
    if target.is_symlink() or not target.is_dir():
        raise ValueError('public_html must already be a real directory under the account home')
    state=home/'.glix-mirror'
    if state.is_symlink():raise ValueError('State directory cannot be a symlink')
    if dry_run:return _deploy(repo,home,revision,names,True)
    state.mkdir(mode=0o700,exist_ok=True)
    lock=state/'deploy.lock'
    lock.mkdir(mode=0o700)
    try:return _deploy(repo,home,revision,names,False)
    finally:lock.rmdir()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[1]
    def git(*args):return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
    if git('status','--porcelain','--untracked-files=no'):
        raise SystemExit('Refusing to deploy modified tracked files')
    subprocess.run([os.sys.executable,str(repo/'scripts/test-cpanel-deploy.py')],check=True)
    print(json.dumps(deploy(repo,Path.home(),git('rev-parse','HEAD'),git('ls-files','-z').split('\0'),args.dry_run)))
    if not args.dry_run:
        subprocess.run([os.sys.executable,str(repo/'scripts/setup-cpanel.py')],check=True)

if __name__=='__main__':main()
