import re
import datetime
from datapackage_pipelines.wrapper import process

DATE_RE = re.compile('[0-9]+')


def boolean(x):
    return isinstance(x, str) and x.strip() == 'כן'


def date(x):
    if isinstance(x, int) or isinstance(x, float):
        return datetime.date(1900, 1, 1) + datetime.timedelta(days=int(x))
    elif not isinstance(x, str):
        return x

    x = x.strip()
    if len(x) == 0:
        return None

    parts = DATE_RE.findall(x)
    if len(parts) == 3:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        if year < 100:
            year += 2000
        return datetime.date(year=year, month=month, day=day)


def budget_code(x):
    x = str(x).strip()
    if x.endswith('.0'):
        x = x[:-2]
    if len(x) == 11:
        x = '00'+x.replace('-', '').replace('=', '')
        assert(len(x) == 10)
    elif len(x) == 8:
        assert('-' not in x and '=' not in x)
        x = '00'+x
    elif len(x) == 7:
        assert('-' not in x and '=' not in x)
        x = '000'+x
    else:
        return None
    return x

BAD_WORDS = [
    'סה"כ',
    'סה״כ',
    '=SUBTOTAL',
    '=SUM'
]

def process_row(row, *_):
    for v in row.values():
        for bw in BAD_WORDS:
            if isinstance(v, str) and bw in v:
                return

    for k, v in row.items():
        if k in ['sensitive_order']:
            row[k] = boolean(v)
        elif k in ['budget_code']:
            row[k] = budget_code(v)
        elif k in ['end_date', 'order_date', 'start_date']:
            row[k] = date(v)
        elif isinstance(v, str):
            row[k] = v.strip()
    return row

process(process_row=process_row)
