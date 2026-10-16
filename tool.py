"""Compare CycloneDX-style component inventories, detect ambiguous identities and explain version/license changes."""
def inventory(bom):
    result = {}
    for component in bom.get('components',[]):
        key = component.get('bom-ref') or component.get('purl') or ':'.join([component.get('group',''),component['name']])
        if key in result:
            raise ValueError('duplicate component identity: '+key)
        licenses = sorted(str(x.get('expression') or x.get('license',{}).get('id') or x.get('license',{}).get('name','UNKNOWN')) for x in component.get('licenses',[]))
        result[key] = dict(version=component.get('version'),licenses=licenses)
    return result

def analyze(data):
    before,after = inventory(data['before']), inventory(data['after'])
    findings = []
    for key in sorted(before.keys() | after.keys()):
        if key not in before:
            findings.append(dict(kind='added',component=key,after=after[key]))
        elif key not in after:
            findings.append(dict(kind='removed',component=key,before=before[key]))
        elif before[key] != after[key]:
            findings.append(dict(kind='changed',component=key,before=before[key],after=after[key]))
    return findings


def main():
    import argparse, json, sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='path to JSON input, or - for stdin')
    args = parser.parse_args()
    try:
        if args.input == '-':
            data = json.load(sys.stdin)
        else:
            with open(args.input, encoding='utf-8') as stream:
                data = json.load(stream)
        result = analyze(data)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as error:
        print('Invalid input: '+str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
