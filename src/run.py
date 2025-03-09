import argparse
from Uzabase_assignment import process_data, process_data_all

def main():
    parser = argparse.ArgumentParser(description="Process AG News dataset.")
    subparsers = parser.add_subparsers(dest="command")

    # Parser for process_data
    parser_process_data = subparsers.add_parser('process_data')
    parser_process_data.add_argument('--cfg', required=True, help="Path to config file")
    parser_process_data.add_argument('--dataset', required=True, help="Dataset name")
    parser_process_data.add_argument('--dirout', required=True, help="Output directory")

    # Parser for process_data_all
    parser_process_data_all = subparsers.add_parser('process_data_all')
    parser_process_data_all.add_argument('--cfg', required=True, help="Path to config file")
    parser_process_data_all.add_argument('--dataset', required=True, help="Dataset name")
    parser_process_data_all.add_argument('--dirout', required=True, help="Output directory")

    args = parser.parse_args()

    if args.command == 'process_data':
        process_data(args.cfg, args.dataset, args.dirout)
    elif args.command == 'process_data_all':
        process_data_all(args.cfg, args.dataset, args.dirout)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
