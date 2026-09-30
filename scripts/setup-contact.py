#!/usr/bin/env python3
"""Install the contact handler privately and validate it without sending mail."""
from pathlib import Path
import os
import json
import secrets
import shutil
import subprocess
import tempfile

repo=Path(__file__).resolve().parents[1]
home=Path.home()
if str(home)!='/home5/glixcpanel':raise SystemExit('Unexpected hosting account')
php=next((p for p in ['/opt/cpanel/ea-php83/root/usr/bin/php','/usr/local/bin/php','/usr/bin/php'] if Path(p).is_file()),None)
if not php:raise SystemExit('PHP CLI is required to validate the contact handler')
for name in ['api/glix-contact.php','server/contact-lib.php','server/test-contact.php']:
    subprocess.run([php,'-l',str(repo/name)],check=True)
subprocess.run([php,str(repo/'server/test-contact.php')],check=True)
state=home/'.glix-contact'
if state.is_symlink():raise SystemExit('Invalid contact storage')
state.mkdir(mode=0o700,exist_ok=True)
os.chmod(state,0o700)
secret=state/'secret'
if secret.is_symlink():raise SystemExit('Invalid contact secret path')
if not secret.exists():
    fd=os.open(str(secret),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as out:out.write(secrets.token_hex(32))
handler=state/'contact-lib.php'
if handler.is_symlink():raise SystemExit('Invalid contact handler path')
fd,tmp=tempfile.mkstemp(prefix='handler-',dir=str(state))
try:
    with os.fdopen(fd,'wb') as out:out.write((repo/'server/contact-lib.php').read_bytes())
    os.chmod(tmp,0o600);os.replace(tmp,handler)
finally:
    if os.path.exists(tmp):os.unlink(tmp)
print('Contact handler installed privately; no email was sent during setup.')

result=subprocess.run(['/usr/local/cpanel/bin/uapi','--output=json','Email','list_pops','domain=glixerp.com'],capture_output=True,text=True,timeout=30)
try:
    response=json.loads(result.stdout).get('result',{})
    found=any(row.get('email')=='info@glixerp.com' for row in (response.get('data') or [])) if response.get('status')==1 else None
    print(json.dumps({'recipient':'info@glixerp.com','local_mailbox_found':found}))
except (ValueError,AttributeError,TypeError):print('Mailbox availability could not be checked automatically.')
