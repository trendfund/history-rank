import json
import glob
import datetime
import calendar

def write_json(file_name, data):
    with open(f'./coincodex/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

json_files = sorted(glob.glob('./coincodex/daily/*_statistic.json'))

market_caps = []
total_market_caps = []
volumns = []
gainers_vs_losers = {'gainers': [], 'losers': []}
turnovers = []

start_date = datetime.date(2020, 1, 1)

for json_file in json_files:
    dt_string = json_file[-23:-15]
    dt = datetime.datetime.strptime(dt_string, '%Y%m%d').date() - datetime.timedelta(days=1)

    print(dt)
    ts = calendar.timegm(dt.timetuple())

    with open(json_file, 'r', encoding='utf-8') as f:
        statistic = json.load(f)

        total_market_caps.append([ts, statistic['market_cap']['open']])

        if dt < start_date:
            continue

        market_caps.append([ts, statistic['market_cap']['open']])
        volumns.append([ts, statistic['volume']])
        gainers_vs_losers['gainers'].append([ts, statistic['gainers_percent']])
        gainers_vs_losers['losers'].append([ts, statistic['losers_percent']])
        turnovers.append([ts, round(statistic['volume'] / statistic['market_cap']['open'], 6)])

total_market_caps.append([ts + 60 * 60 * 24, statistic['market_cap']['close']])
market_caps.append([ts + 60 * 60 * 24, statistic['market_cap']['close']])

write_json('total_market_caps', total_market_caps)
write_json('market_caps', market_caps)
write_json('volumns', volumns)
write_json('gainers_vs_losers', gainers_vs_losers)
write_json('turnovers', turnovers)