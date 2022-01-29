import json
import glob

from collections import defaultdict

json_files = sorted(glob.glob('./*.json'))

capitals = {}

capital_words = ['capital', 'ventures', 'portfolio']

def is_a_capital(tag):
    return any(x in tag for x in capital_words)

for json_file in json_files:
    dt_string = json_file[2:10]
    print(dt_string)

    with open(json_file, 'r', encoding='utf-8') as f:
        ranking = json.load(f)

        for currency in ranking:
            symbol = currency['symbol']
            tags = currency['tags']

            for tag in tags:
                if not is_a_capital(tag):
                    continue

                if not tag in capitals:
                    capitals[tag] = {}
                
                if not dt_string in capitals[tag]:
                    capitals[tag][dt_string] = []

                capitals[tag][dt_string].append(symbol)

dt_strings = []

for capital, history in capitals.items():
    print(f'dump capital data {capital}({len(history)})')

    for dt_string, value in history.items():
        dt_strings.append(dt_string)

        history[dt_string] = {
            'count': len(value),
            'symbols': sorted(value)
        }
        
    with open(f'capitals/{capital}.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

holding_history = {}
dt_strings = sorted(set(dt_strings))

for dt_string in dt_strings:
    if not dt_string in holding_history:
        holding_history[dt_string] = defaultdict(lambda: 0)

    for capital, history in capitals.items():
        if not dt_string in history:
            continue

        for symbol in history[dt_string]['symbols']:
            holding_history[dt_string][symbol] += 1
    
    holdings = holding_history[dt_string]
    sorted_holdings = dict(sorted(holdings.items(), key=lambda x: x[1], reverse=True))
    holding_history[dt_string] = {
        'count': len(sorted_holdings),
        'symbols': sorted_holdings
    }

print(f'dump holding history data ({len(holding_history)})')

with open(f'capitals/holding-history.json', 'w', encoding='utf-8') as f:
    json.dump(holding_history, f, indent=2, ensure_ascii=False)