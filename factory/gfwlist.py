"""Convert the official AutoProxy list into an ordered Shadowrocket rule block."""

import base64
import os
from pathlib import Path
import re
import tempfile
from urllib.request import urlopen

SOURCE = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
OUTPUT = Path(__file__).resolve().parent / 'resultant' / 'gfw.list'
HOST = re.compile(r'[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*')
HOST_END = r'(?=[:/?\x23]|$)'
# This upstream exception has an end anchor but lacks the closing regex delimiter.
OPEN_EXCEPTION = r'/^https?:\/\/(?=.*?(2x3|ni5|j5o))[a-z0-9.-]+\.xn--ngstr-lra8j\.com$'


def glob_regex(text, wildcard):
    return wildcard.join(re.escape(part) for part in text.split('*'))


def url_pattern(body):
    if body.startswith('/'):
        if body.endswith('/'):
            return body[1:-1]
        if body == OPEN_EXCEPTION:
            return body[1:]
        raise ValueError(f'Unterminated regex: {body}')

    if body.startswith('||'):
        host_path = body[2:]
        prefix = r'^[a-zA-Z][a-zA-Z0-9+.-]*://(?:[a-zA-Z0-9-]+\.)*'
    elif body.startswith(('|http://', '|https://')):
        scheme, host_path = body[1:].split('://', 1)
        prefix = '^' + scheme + '://'
    else:
        raise ValueError(f'Unsupported AutoProxy syntax: {body}')

    host, slash, path = host_path.partition('/')
    if not re.fullmatch(r'[a-zA-Z0-9.*-]+', host) or any(c in path for c in '^|$'):
        raise ValueError(f'Unsupported host or path: {body}')
    return prefix + glob_regex(host, '[a-zA-Z0-9.-]*') + (
        '/' + glob_regex(path, '.*') if slash else HOST_END)


def convert(text):
    lines = text.splitlines()
    if not lines or not lines[0].startswith('[AutoProxy '):
        raise ValueError('Missing AutoProxy header')
    exceptions, proxies = [], []
    for raw in lines[1:]:
        raw = raw.strip()
        if not raw or raw.startswith('!'):
            continue
        exception = raw.startswith('@@')
        body = raw[2:] if exception else raw
        policy = 'DIRECT' if exception else 'PROXY'
        if body.startswith('||') and HOST.fullmatch(body[2:].removesuffix('^')):
            rule = 'DOMAIN-SUFFIX,' + body[2:].removesuffix('^')
        elif HOST.fullmatch(body):
            # An unanchored hostname is restricted to that exact host.
            rule = 'DOMAIN,' + body
        else:
            pattern = url_pattern(body)
            if ',' in pattern or '#' in body:
                raise ValueError(f'Unsafe configuration delimiter: {body}')
            re.compile(pattern)
            rule = 'URL-REGEX,' + pattern
        (exceptions if exception else proxies).append(rule + ',' + policy)
    if not proxies or not exceptions:
        raise ValueError('Incomplete upstream proxy or exception list')
    return '\n'.join(dict.fromkeys(exceptions + proxies)) + '\n'


if __name__ == '__main__':
    with urlopen(SOURCE, timeout=30) as response:
        encoded = b''.join(response.read().split())
    result = convert(base64.b64decode(encoded, validate=True).decode('utf-8'))
    with tempfile.NamedTemporaryFile(dir=OUTPUT.parent, mode='w', encoding='utf-8',
                                     delete=False) as pending:
        pending.write(result)
    os.replace(pending.name, OUTPUT)
