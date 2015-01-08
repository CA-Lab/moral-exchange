import argparse
import data_objects as do
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

################################
# parse command line arguments #
################################
parser = argparse.ArgumentParser(description='prissoner dilema network simulation')
parser.add_argument('--db_url', default='sqlite:///db.sqlite', help='DB URL, default: sqlite:///db.sqlite')
parser.add_argument('--mode', required=True, choices=['init','walk'])
args = parser.parse_args()


####################
# database connect #
####################
engine  = create_engine(args.db_url)
do.Session = sessionmaker(bind=engine)



if args.mode == 'init':
    do.Base.metadata.create_all(engine)
    g = do.init_watts()
    do.network_to_db(g)
elif args.mode == 'walk':
    do.random_prissoner_walk()


