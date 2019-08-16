.. _tutorial:

Getting started with capiq_excel
**********************************

Install
=======

Install this package via::

    pip install capiq_excel

You must also be running Windows, have Excel installed,
and have the Capital IQ plugin for Excel installed. For Capital IQ plugin
install instructions, 
`check here <https://www.capitaliq.com/help/sp-capital-iq-help/office-plug-in/excel-plug-in/excel-plug-in-version-8x/frequently-asked-questions-(faq)/where-can-i-download-the-sp-capital-iq-excel-plug-in.aspx>`_.

Ensure that when you go to the S&P Capital IQ tab, that the buttons are not grayed
out. If they are, you have to go
to the tab and click the "Reconnect" button. Once you are
logged in, all the buttons should be highlighted on the tab. Then you can
close Excel and begin using :code:`capiq_excel`.

Overview
=========

Data must be downloaded from Capital IQ using Capital IQ ids. If you don't
have Capital IQ ids, this package can also handle retrieving them.

If you don't have Capital IQ ids, you'll want to use :py:func:`.download_data`
which accepts any sort of ids such as ticker, name, CUSIP, or ISIN. If you
already have Capital IQ ids, you'll want to use
:py:func:`.download_data_for_capiq_ids`.

This package downloads the data (and also the ids, if using
:py:func:`.download_data`) in three main steps:

1. Creates an XLSX workbook for each company containing the Excel function
for the Capital IQ Excel plugin to download the Capital IQ data

2. Opens each workbook, one by one, allowing the data to populate, then
closing and saving the workbook.

3. Reads the data from all the generated workbooks and combines into
one CSV file.

Usage
=========

There are two main functions in the package, depending on whether you
have Capital IQ ids or some other identifier. Assuming you do not have
Capital IQ ids,
:py:func:`.download_data` is the main function, while if you have
Capital IQ ids, :py:func:`.download_data_for_capiq_ids` is the main
function.

This is a simple example for when you have some arbitrary identifers::

    from capiq_excel import download_data

    download_data(
        ['MSFT', 'AAPL'],  # Any id type. Ticker, name, CUSIP, ISIN, etc.
        ['IQ_TOTAL_REV', 'IQ_COST_REV'], # Variable names from Capital IQ
        freq='Q',
        num_periods=6
    )



This is a simple example for when you have Capital IQ ids::

    from capiq_excel import download_data_for_capiq_ids

    download_data_for_capiq_ids(
        ['IQ21835', 'IQ24937'],  # Capital IQ ids
        ['IQ_TOTAL_REV', 'IQ_COST_REV'], # Variable names from Capital IQ
        freq='Q',
        num_periods=6
    )


You may see errors relating to calling Excel and that Excel has been terminated.
There is retry logic built into the package as Excel does not respond very
consistently in this way, so Excel may be terminated and restarted many
times in the process of downloading.

A :code:`failed` folder will be created and any XLSX that were unable
to pull data after several retries will be moved here so that they can be
re-run later.

Troubleshooting
================

Hopefully the main function works end-to-end. But
the second step where the files are populated may cause Excel to fail. There is
some logic in the package to keep restarting Excel, but this may eventually
fail as well. If this happens, get your Excel working manually again (may
require a restart or re-enabling the Capital IQ plugin), then you can run
the same function again while passing `restart=False` to
continue where it left off. Repeat this as many times as needed.

For example resuming with arbitrary ids::

    from capiq_excel import download_data

    download_data(
        ['MSFT', 'AAPL'],  # Any id type. Ticker, name, CUSIP, ISIN, etc.
        ['IQ_TOTAL_REV', 'IQ_COST_REV'], # Variable names from Capital IQ
        freq='Q',
        num_periods=6,
        restart=False
    )


For example resuming with Capital IQ ids::

    from capiq_excel import download_data_for_capiq_ids

    download_financials(
        ['IQ21835', 'IQ24937'],  # Capital IQ ids
        ['IQ_TOTAL_REV', 'IQ_COST_REV'], # Variable names from Capital IQ
        freq='Q',
        num_periods=6,
        restart=False
    )

