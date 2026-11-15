"""Small client for the fleet engine's gate. Standard library only, no proxy.

Usage:
  gate.py get <path>
  gate.py post <path> '<json body>'
  gate.py patch|delete <path> ['<json body>']
  gate.py raw <pilot> <action> ['<json params>'] [toolGroup]
  gate.py goal <pilot> <type> ['<json options>']
Prints the JSON answer (passwords masked), cut to 3000 chars unless FULL=1.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(method, path, body=None, timeout=400):
    data = None if body is None else json.dumps(body).encode('utf-8')
    req = urllib.request.Request(GATE + path, data=data, method=method.upper(),
                                 headers={'Content-Type': 'application/json'} if data is not None else {})
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def q(name):
    return urllib.parse.quote(name, safe='')


def main():
    verb = sys.argv[1]
    if verb in ('get', 'delete') and len(sys.argv) == 3:
        status, text = call(verb, sys.argv[2])
    elif verb in ('post', 'patch', 'delete'):
        status, text = call(verb, sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {})
    elif verb == 'raw':
        params = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        group = sys.argv[5] if len(sys.argv) > 5 else 'spacemolt'
        status, text = call('post', f'/accounts/{q(sys.argv[2])}/raw', {'toolGroup': group, 'action': sys.argv[3], 'params': params})
    elif verb == 'goal':
        options = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        status, text = call('post', f'/accounts/{q(sys.argv[2])}/goal', {'type': sys.argv[3], 'options': options})
    else:
        sys.exit(__doc__)
    text = re.sub(r'("password"\s*:\s*)"[^"]*"', r'\1"<masked>"', text)
    print('http', status)
    print(text if os.environ.get('FULL') else text[:3000])


if __name__ == '__main__':
    main()
