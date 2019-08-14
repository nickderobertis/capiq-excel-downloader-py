


if __name__ == '__main__':
    import argparse
    import os
    import shutil

    from capiq.workbook.create import create_all_xlsx_with_holdings_commands
    from dataconfig.paths import big_capiq_path, capiq_path
    from capiq.downloader.tools import populate_all_files_in_folder, _get_company_id_list
    from capiq.variables.holdings import insider_variables, institutional_variables, date_strs


    parser = argparse.ArgumentParser(description='Create workbooks and download holdings data from capital IQ - holdings data')
    parser.add_argument('-i','--ids-file', default=capiq_path(r'public company ids.csv'))
    parser.add_argument('-o', '--output', default=big_capiq_path(r'inprogress'))
    parser.add_argument('--restart', action='store_true')
    parser.add_argument('--insider', action='store_true')
    parser.add_argument('-f', '--failed', action='store_true')

    args = parser.parse_args()

    company_id_list = _get_company_id_list(args.ids_file)

    if args.insider:
        variables = insider_variables
    else:
        variables = institutional_variables

    folder_exists = os.path.exists(args.output)

    if not folder_exists:
        os.makedirs(args.output)

    if args.restart and folder_exists:
        shutil.rmtree(args.output)
        os.makedirs(args.output)

    if args.restart or (not folder_exists):
        create_all_xlsx_with_holdings_commands(args.output, company_id_list, date_strs, variables)

    populate_all_files_in_folder(args.output, restart=args.restart, run_failed=args.failed)