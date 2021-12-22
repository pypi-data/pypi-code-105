from .wiki_reader import *
from .db_writer import DBWriter
from functools import partial
import argparse
from .wiki_downloader import WikiDumpDownloader
from multiprocessing import Pool, cpu_count


def main():
    parser = argparse.ArgumentParser(
        prog='archean',
        description='Archean is a tool to process Wikipedia dumps and '
                    + 'extract required information from them. The parser '
                    + 'accepts a few parameters that can be specified during '
                    + 'script invokation.'
    )
    parser.add_argument(
        '--no-db', action='store_true', help='No DB related operations'
    )
    parser.add_argument(
        '--host', default='127.0.0.1',
        help='Host location for the database server. Defaults to localhost.'
    )
    parser.add_argument(
        '-u', default=None,
        help='Username for the database authentication'
    )
    parser.add_argument(
        '-p', default=None,
        help='Password for the database authentication'
    )
    parser.add_argument(
        '--port', default='27017',
        help='Port for database'
    )
    parser.add_argument(
        '--conn', default='mongodb://localhost:27017',
        help='Connection string for the database. Defaults to local db server '
             + '`mongodb://localhost:27017`'
    )
    parser.add_argument(
        '--db', default='media',
        help='Database name to point to. Defaults to `media`.'
    )
    parser.add_argument(
        '--collection', default='movies',
        help='Collection in which the extracted JSON data will '
             + 'be stored in. Defaults to `movies`.'
    )
    parser.add_argument(
        '--download',
        help='The directory from which the dump is to be downloaded'
    )
    parser.add_argument(
        '--partition-directory', default='./extracts',
        help='Directory to store extracted information'
    )
    parser.add_argument(
        '--download-only', action='store_true',
        help='Only download files, Do NOT process them'
    )
    parser.add_argument(
        '--files', default=None,
        help='Number of files to download/process.'
    )
    args = parser.parse_args()
    if args.download:
        loader = WikiDumpDownloader(args.download)
        loader.fetch_dumps(
            int(args.files) if args.files else None
        )

    if args.download_only:
        # exit if download only
        return

    files = []
    skipped = []
    partitions = [os.path.realpath(file)
                  for file in
                  os.listdir() if 'xml-p' in file]

    partition_dir = os.path.realpath(args.partition_directory)

    for i in partitions:
        # Create file name based on partition name
        p_str = os.path.splitext(os.path.basename(i).split('/')[-1])[0]
        out_dir = partition_dir + f'{p_str}.json'
        if os.path.exists(out_dir):
            print(f'Skipping {p_str}.json since it already exists')
            skipped.append(out_dir)
            continue
        else:
            files.append(i)

    print(f'Skipped {len(skipped)} files')
    func = partial(find_films, partition_dir=partition_dir)
    # Create a pool of workers to execute processes
    with Pool(cpu_count()-1) as pool:
        # Map (service, tasks), applies function to each partition
        pool.map(func, files)

    # Write to db
    if not args.no_db:
        writer = DBWriter(connection_str = args.conn,
            host = args.host, user=args.u, passwrd=args.p, 
            collection=args.collection, db=args.db, port=args.port)
        if os.path.exists(partition_dir):
            writer.write(partition_dir)
            writer.process_dates()
        else:
            # Raise RuntimeError if partition directory does not exist
            raise RuntimeError(
                "No extracted data found.\n"
                + "Download some data and process it first.\n"
                + "Run archean -h for help"
            )
