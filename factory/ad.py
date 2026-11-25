"""Extract whole-domain advertising blocks for Shadowrocket."""

import re
import time
from pathlib import Path


rules_url = [
    # EasyList China
    'https://easylist-downloads.adblockplus.org/easylistchina.txt',
    # EasyList + China
    'https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt',
    # 乘风 广告过滤规则
    'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt',
    # Peter Lowe 广告和隐私跟踪域名
    'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=0&mimetype=plaintext',
]

RESULTANT = Path(__file__).resolve().parent / 'resultant'
DOMAIN = re.compile(r'[a-z0-9][-a-z0-9]{0,62}(?:\.[a-z0-9][-a-z0-9]{0,62})*\.[a-z0-9][-a-z0-9]+')
IPV4 = re.compile(r'\d{1,3}(?:\.\d{1,3}){3}')


def blocked_host(rule):
    # Preserve the host-only representations accepted by the existing blocklist.
    host = re.sub(r'^\|?https?://', '', rule.lower()).removeprefix('||')
    host = host.lstrip('.*').rstrip('/*').rstrip('^')
    host = re.sub(r':\d{2,5}$', '', host)
    if DOMAIN.fullmatch(host) or IPV4.fullmatch(host):
        return host
    return None


def exception_host(rule):
    # Paths, ports, protocol-specific filters and $options cannot be expressed
    # as an unconditional exception in this whole-domain list.
    host = rule.lower().removeprefix('||').removeprefix('*.')
    host = re.sub(r'(?:\^|/\*|/)$', '', host)
    if DOMAIN.fullmatch(host) or IPV4.fullmatch(host):
        return host
    return None


def host_suffixes(host):
    yield host
    if not IPV4.fullmatch(host):
        labels = host.split('.')
        for index in range(1, len(labels) - 1):
            yield '.'.join(labels[index:])


def extract_domains(lines, ignored=()):
    blocks = set()
    exceptions = set()
    for line in lines:
        rule = line.strip()
        if rule.startswith('@@'):
            host = exception_host(rule[2:])
            if host:
                exceptions.add(host)
        elif rule and not rule.startswith('!') and '$' not in rule and '##' not in rule:
            host = blocked_host(rule)
            if host:
                blocks.add(host)

    # A DOMAIN-SUFFIX block for a parent would also reject an excepted child.
    # Keep independent sibling blocks and the existing exact local exclusions.
    blocked_parents = {parent for host in exceptions for parent in host_suffixes(host)}
    blocks.difference_update(blocked_parents, {host.lower() for host in ignored})
    return sorted(host for host in blocks if exceptions.isdisjoint(host_suffixes(host)))


def download_rules(url):
    import requests

    print('loading... ' + url)
    for attempt in range(5):
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            if not response.text.lstrip('\ufeff \r\n\t').startswith('[Adblock Plus'):
                raise SystemExit('Unexpected ad list format from ' + url)
            return response.text
        if attempt < 4:
            time.sleep(1)
    raise SystemExit(f'error in request {url}\n\treturn code: {response.status_code}')


def main():
    sources = [download_rules(url) for url in rules_url]
    with (RESULTANT / 'ad_ignore.list').open(encoding='utf-8') as file:
        ignored = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    domains = extract_domains((line for source in sources for line in source.splitlines()), ignored)
    with (RESULTANT / 'ad.list').open('w', encoding='utf-8') as file:
        file.write('# adblock rules refresh time: ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        for host in domains:
            file.write(host + '\n')
    print('done.')


if __name__ == '__main__':
    main()
