#!/usr/bin/env python3
"""Install only the Glix scheduled copy; retain all other cPanel cron jobs."""
from pathlib import Path
import json
import os
import subprocess

MARKER='# glix-website-mirror'

def install(home,repo):
    state=home/'.glix-mirror'
    result=subprocess.run(['crontab','-l'],capture_output=True,text=True)
    if result.returncode and 'no crontab' not in result.stderr.lower():
        raise RuntimeError('Cannot read existing scheduled jobs: '+result.stderr)
    original=result.stdout
    command='* * * * * /usr/bin/python3 '+str(repo/'scripts/cpanel-poll.py')+' > /dev/null 2>&1 '+MARKER
    lines=original.splitlines()
    existing=[line for line in lines if line.endswith(MARKER)]
    if existing!=[command]:
        backup=state/'crontab.before-glix'
        if not backup.exists():backup.write_text(original);os.chmod(backup,0o600)
        new='\n'.join([line for line in lines if not line.endswith(MARKER)]+[command])+'\n'
        subprocess.run(['crontab','-'],input=new,text=True,check=True)
    installed=subprocess.check_output(['crontab','-l'],text=True)
    if command not in installed.splitlines():raise RuntimeError('Scheduled task verification failed')
    print(json.dumps({'cpanel_cron_installed':True,'interval_minutes':1,'other_cron_jobs_preserved':True}))
    success=state/'poll-last-success.json'
    if success.exists():print(success.read_text())

def audit(home):
    state=home/'.glix-mirror'
    if (state/'audit.json').exists():return
    report={}
    for label,args in {
        'spf':['EmailAuth','validate_current_spfs','domain=glixerp.com'],
        'dkim':['EmailAuth','validate_current_dkims','domain=glixerp.com'],
        'domain':['DomainInfo','single_domain_data','domain=glixerp.com'],
    }.items():
        p=subprocess.run(['/usr/local/cpanel/bin/uapi','--output=json',*args],capture_output=True,text=True,timeout=30)
        try:report[label]=json.loads(p.stdout)
        except ValueError:report[label]={'exit_code':p.returncode}
    htaccess=home/'public_html/.htaccess'
    report['hosting_directives']=[line for line in htaccess.read_text().splitlines() if line.strip().startswith(('php_flag','php_value','AddHandler','Options','Header','Expires','AddOutputFilterByType','RewriteRule','RewriteCond'))] if htaccess.exists() else []
    destination=state/'audit.json'
    destination.write_text(json.dumps(report,indent=2));os.chmod(destination,0o600)
    print(json.dumps({'hosting_audit':report}))

if __name__=='__main__':
    home=Path.home()
    if str(home)!='/home5/glixcpanel':raise SystemExit('This setup is specific to the Glix hosting account')
    install(home,Path(__file__).resolve().parents[1])
    audit(home)
    subprocess.run([os.sys.executable,str(Path(__file__).with_name('configure-cpanel-web.py'))],check=True)
