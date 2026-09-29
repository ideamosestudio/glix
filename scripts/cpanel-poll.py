#!/usr/bin/env python3
"""Scheduled on the hosting account: validate and mirror the latest main commit."""
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

home=Path.home()
state=home/'.glix-mirror'
repo=home/'repositories/glix'
os.environ['PATH']='/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/bin:/usr/bin:/bin'
if state.is_symlink() or repo.is_symlink():raise SystemExit('Invalid operational path')
state.mkdir(mode=0o700,exist_ok=True)
with (state/'poll.lock').open('a') as lock:
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit(0)
    log=state/'poll.log'
    if log.exists() and log.stat().st_size>262144:log.replace(state/'poll.previous.log')
    try:
        latest=subprocess.check_output(['git','ls-remote','https://github.com/ideamosestudio/glix.git','refs/heads/main'],text=True,timeout=45).split()[0]
        if not re.fullmatch('[a-f0-9]{40}',latest):raise ValueError('Invalid remote revision')
        manifest=state/'manifest.json'
        current=json.loads(manifest.read_text())['revision'] if manifest.exists() else None
        success=state/'poll-last-success.json'
        last=json.loads(success.read_text()).get('revision') if success.exists() else None
        if latest==current and latest==last:raise SystemExit(0)
        env=dict(os.environ,SSH_ORIGINAL_COMMAND='glix-sync '+latest)
        result=subprocess.run(['/usr/bin/python3',str(state/'ssh-gateway.py')],env=env,capture_output=True,text=True,timeout=180)
        with log.open('a') as out:
            out.write(datetime.now(timezone.utc).isoformat()+' '+latest+'\n'+result.stdout+result.stderr)
        if result.returncode:raise RuntimeError('Deployment failed; see private poll.log')
        (state/'poll-last-success.json').write_text(json.dumps({'revision':latest,'updated_at':datetime.now(timezone.utc).isoformat(),'source':'cpanel-cron'}))
    except Exception as exc:
        with log.open('a') as out:out.write(datetime.now(timezone.utc).isoformat()+' ERROR '+str(exc)+'\n')
        raise
