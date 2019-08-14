
always_keep_cols = [
    'CQID',
    'Date'
]

_institutional_only_keep_cols = [
    'Institutional Shares',
]

_insider_only_keep_cols = [
    'Insider Shares'
]

institutional_keep_cols = always_keep_cols + _institutional_only_keep_cols
insider_keep_cols = always_keep_cols + _insider_only_keep_cols