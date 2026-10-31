import pexpect,re
PROMPT=re.compile(r'(: |\? )$')
def run(binp, cmds, leaks=True):
    c=pexpect.spawn(binp,encoding='utf-8',timeout=3,
        env={'ASAN_OPTIONS':'detect_leaks=%d'%(1 if leaks else 0),'TERM':'dumb'})
    out=''
    for cmd in cmds:
        c.expect(PROMPT.pattern)
        out+=c.before+c.after
        c.send(cmd+'\r')
    try: c.expect(pexpect.EOF)
    except Exception: pass
    out+=c.before
    out=re.sub(r'\x1b\[[0-9;]*m','',out).replace('\r','')
    return out
