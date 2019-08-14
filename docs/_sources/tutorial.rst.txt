.. _tutorial:

Getting started with capiq_excel
**********************************

Install
=======

Install this package via::

    pip install capiq_excel

You must also be running Windows, have Excel installed,
and have the Capital IQ plugin for Excel installed.

Ensure that when you go to the S&P Capital IQ tab, that the buttons are not grayed
out. If they are, you have to go
to the tab and click the "Reconnect" button. Once you are
logged in, all the buttons should be highlighted on the tab. Then you can
close Excel and begin using :code:`capiq_excel`.

Overview
=========

This package downloads the data in three main steps:

1. Creates an XLSX workbook for each company containing the Excel function
for the Capital IQ Excel plugin to download the Capital IQ data

2. Opens each workbook, one by one, allowing the data to populate, then
closing and saving the workbook.

3. Reads the data from all the generated workbooks and combines into
one CSV file.

Usage
=========

There are four main functions in the package.
:py:func:`.download_financials` is the main function, which
is just a wrapper to call the other three main functions which complete
the three steps described above: :py:func:`.create_all_xlsx_with_financials_commands`,
:py:func:`.populate_all_files_in_folder`, and :py:func:`.combine_all_capiq_xlsx`.


This is a simple example::

    from capiq_excel import download_financials

    download_datastream(
        'output_folder',
        ['IQ21835', 'IQ24937'],  # Capital IQ ids
        {
            'IQ_TOTAL_REV': 'Sales',
            'IQ_COST_REV': 'COGS'
        },  # Variable names from Capital IQ, and desired names in output data
        outpath='data.csv',
        freq='Q',
        num_periods=6
    )


You may see errors relating to calling Excel and that Excel has been terminated.
There is retry logic built into the package as Excel does not respond very
consistently in this way, so Excel may be terminated and restarted many
times in the process of downloading.

A `failed` folder will be created and any XLSX that were unable
to pull data after several retries will be moved here so that they can be
re-run later.

Troubleshooting
================

Hopefully the :py:func:`.download_financials` function works end-to-end. But
the second step where the files populated may cause Excel to fail. There is
some logic in the package to keep restarting Excel, but this may eventually
fail as well. If this happens, get your Excel working manually again (may
require a restart or re-enabling the Eikon plugin), then you can run
:py:func:`.populate_all_files_in_folder` while passing `restart=False` to
continue where it left off. Repeat this as many times as needed, then at
the end you can run :py:func:`.combine_all_capiq_xlsx`.

For example::

    from capiq_excel import (
        populate_all_files_in_folder,
        combine_all_capiq_xlsx
    )

    # Run as many times as needed, fixing Excel in between
    populate_all_files_in_folder(
        'output_folder',
        restart=False
    )

    # Once populate can actually finish, then run this
    combine_all_capiq_xlsx(
        'output_folder',
        outpath='data.csv'
    )
