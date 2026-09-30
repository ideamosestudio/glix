#!/usr/bin/env python3
"""Maintain a scoped, reversible Apache block for the Glix static website."""
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import tempfile
import subprocess

START='# BEGIN GLIX STATIC WEBSITE'
END='# END GLIX STATIC WEBSITE'

def merge(original,block):
    if original.count(START)!=original.count(END) or original.count(START)>1:
        raise ValueError('Ambiguous managed Apache configuration')
    if START in original:
        before,tail=original.split(START,1)
        _,after=tail.split(END,1)
        return before+block+after
    return original.rstrip('\n')+'\n\n'+block+'\n'

def build(names):
    pages=[n for n in names if n.endswith('.html') and '/' not in n]
    text=[n for n in names if n.endswith(('.html','.css','.js','.svg','.txt','.xml'))]
    assets=[n for n in names if n.endswith(('.webp','.png','.woff2'))]
    def expression(items,root=False):
        pattern='|'.join(re.escape(n).replace('\\.','[.]') for n in sorted(items))
        return '%{REQUEST_URI} =~ m#^/(?:'+pattern+(')?$#' if root else ')$#')
    all_expr=expression(names,True)
    pages_expr=expression(pages,True)
    text_expr=expression(text,True)
    assets_expr=expression(assets)
    lines=[START,'# Applies only to paths managed by this website.','<IfModule mod_headers.c>',
        'Header set X-Content-Type-Options "nosniff" "expr='+all_expr+'"',
        'Header set Referrer-Policy "strict-origin-when-cross-origin" "expr='+all_expr+'"',
        'Header set X-Frame-Options "DENY" "expr='+pages_expr+'"',
        'Header set Content-Security-Policy "frame-ancestors \'none\'" "expr='+pages_expr+'"',
        'Header set Permissions-Policy "camera=(), microphone=(), geolocation=()" "expr='+pages_expr+'"',
        'Header set Cache-Control "no-cache" "expr='+text_expr+'"',
        'Header set Cache-Control "public, max-age=86400" "expr='+assets_expr+'"',
        '</IfModule>','<IfModule mod_deflate.c>',
        '<If "'+text_expr+'">','SetOutputFilter DEFLATE','</If>','</IfModule>',END]
    return '\n'.join(lines)

def atomic(path,content):
    fd,tmp=tempfile.mkstemp(prefix='.glix-config-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'w') as out:out.write(content)
        os.chmod(tmp,0o644)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def main():
    home=Path.home();state=home/'.glix-mirror';target=home/'public_html/.htaccess'
    if str(home)!='/home5/glixcpanel' or target.is_symlink():raise ValueError('Unexpected hosting path')
    manifest=json.loads((state/'manifest.json').read_text())
    original=target.read_text() if target.exists() else ''
    content=merge(original,build(list(manifest['files'])))
    if content!=original:
        backup=state/('htaccess-'+hashlib.sha256(original.encode()).hexdigest()[:16]+'.backup')
        if not backup.exists():backup.write_text(original);os.chmod(backup,0o600)
        atomic(target,content)
    cache=subprocess.run(['/usr/local/cpanel/bin/uapi','--output=json','NginxCaching','clear_cache'],capture_output=True,text=True,timeout=30)
    try:cache_result=json.loads(cache.stdout).get('result',{})
    except ValueError:cache_result={'status':0,'errors':['Cache API unavailable']}
    print(json.dumps({'nginx_cache_clear':cache_result}))
    # Verify Apache directly; this hosting closes self-directed HTTPS requests.
    report={'configured':False,'checks':[]}
    import gzip
    for address in ['127.0.0.1','167.250.5.104']:
        try:
            backend=http.client.HTTPConnection(address,81,timeout=10)
            backend.request('GET','/index.html',headers={'Host':'glixerp.com','Accept-Encoding':'gzip','X-Forwarded-Proto':'https'})
            response=backend.getresponse();body=response.read()
            if response.getheader('Content-Encoding')=='gzip':body=gzip.decompress(body)
            report['checks'].append({'address':address,'status':response.status,'headers':dict(response.getheaders())})
            if (response.status==200 and hashlib.sha256(body).hexdigest()==manifest['files']['index.html']
                    and response.getheader('X-Content-Type-Options')=='nosniff'
                    and response.getheader('X-Frame-Options')=='DENY'
                    and response.getheader('Cache-Control')=='no-cache'):
                report['configured']=True
                report['content_verified']=True
                break
        except Exception as exc:report['checks'].append({'address':address,'error':str(exc)})
    if not report['configured']:
        if content!=original:atomic(target,original)
        report['configuration_restored']=True
        report['pending']='Hosting did not permit verification of Apache; preserve provider configuration.'
    (state/'web-verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':main()
