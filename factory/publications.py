"""Published Shadowrocket configurations and pre-deployment checks."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_NAMES = (
    'sr_top500_whitelist_plus',
    'sr_top500_whitelist_ad_plus',
    'sr_cnip_plus',
    'sr_cnip_ad_plus',
    'sr_cnip_ad_plus_dns',
)


def check_files(actual, expected):
    if actual != expected:
        raise SystemExit(f'Missing: {sorted(expected - actual)}, unexpected: {sorted(actual - expected)}')


def verify():
    check_files({p.relative_to(ROOT) for p in ROOT.rglob('*.conf')},
                {Path(name + '.conf') for name in CONFIG_NAMES})
    check_files({p.stem for p in (ROOT / 'figure').glob('*.png')}, set(CONFIG_NAMES))

    for name in CONFIG_NAMES:
        content = (ROOT / (name + '.conf')).read_text(encoding='utf-8')
        lines = set(content.lower().splitlines())
        required = {'[general]', '[rule]', 'final,proxy', 'geoip,cn,direct'}
        if name == 'sr_cnip_ad_plus_dns':
            required.update({'[proxy group]', 'domain-suffix,openai.com,ai'})
        has_ad_rules = any(line.endswith(',reject') for line in lines)
        if required - lines or '{{' in content or has_ad_rules != ('_ad_' in name):
            raise SystemExit(f'Incomplete configuration: {name}')
        if not (ROOT / 'figure' / (name + '.png')).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise SystemExit(f'Invalid QR image: {name}')


if __name__ == '__main__':
    verify()
