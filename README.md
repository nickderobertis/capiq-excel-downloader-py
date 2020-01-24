# capiq_excel

## Overview

Use this tool to drive Excel using the Capital IQ plugin to
download Capital IQ data. It's as easy as:

```python
from capiq_excel import download_data

download_data(
    ['MSFT', 'AAPL'],  # Any id type. Ticker, name, CUSIP, ISIN, etc.
    ['IQ_TOTAL_REV', 'IQ_COST_REV'], # Variable names from Capital IQ
    freq='Q',
    num_periods=6
)
```

## Links

For more information, see the
[documentation here.](https://nickderobertis.github.io/capiq-excel-downloader-py/)
