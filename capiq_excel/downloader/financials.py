


if __name__ == '__main__':
    import argparse
    import os
    import shutil

    from capiq.workbook.create import create_all_xlsx_with_financials_commands
    from dataconfig.paths import capiq_path
    from capiq.downloader.tools import populate_all_files_in_folder, _get_company_id_list
    from capiq.variables.financials import variables


    parser = argparse.ArgumentParser(description='Create workbooks and download holdings data from capital IQ - financial data')
    # parser.add_argument('-i','--ids-file', default=capiq_path(r'all capiq ids.csv'))
    parser.add_argument('-i','--ids-file', default=capiq_path(r'capiq ids third acquired delisted pull new only.csv'))
    parser.add_argument('-o', '--output', default=capiq_path(r'inprogress5'))
    parser.add_argument('--restart', action='store_true')
    parser.add_argument('-f', '--failed', action='store_true')
    parser.add_argument('-s', '--skip-create', action='store_true')


    args = parser.parse_args()

    company_id_list = _get_company_id_list(args.ids_file)
    print(f'Got {len(company_id_list)} ids.')

    folder_exists = os.path.exists(args.output)

    if args.restart and folder_exists:
        shutil.rmtree(args.output)

    if folder_exists and (not args.restart) and (not args.skip_create):
        raise ValueError('Must pass --restart or --skip-create if output is for existing folder')

    if args.restart or (not folder_exists) and (not args.skip_create):
        os.makedirs(args.output)
        print(f'Creating workbooks')
        create_all_xlsx_with_financials_commands(args.output, company_id_list, variables)

    print('Populating workbooks')
    populate_all_files_in_folder(args.output, restart=args.restart, run_failed=args.failed)