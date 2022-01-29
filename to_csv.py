import csv
import json
import glob

base_dir = 'coincodex/daily/'

def to_csv(src):
    file_name = src.split(base_dir)[-1].split('.')[0]
    dest = f'{base_dir}{file_name}.csv'

    with open(src, 'r', encoding='UTF-8') as f:
        json_res = json.load(f)

    with open(dest, 'w', encoding='UTF-8') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='`', quoting=csv.QUOTE_MINIMAL)
        heads = json_res[0].keys()
        csv_writer.writerow(heads)
        rows = [list(x.values()) for x in json_res]
        csv_writer.writerows(rows)

res = glob.glob(f'{base_dir}*.json')
res = [x for x in res if not 'statistic' in x]

for src in res:
    print(src)
    to_csv(src)