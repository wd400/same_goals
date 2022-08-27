import sys
sys.path.append("..")
from config import DEFAULT_TABLE
from logs import LOGGER


def do_drop(id,user, milvus_cli, mysql_cli):
    print("DELETE ID",id)
    try:
        if not mysql_cli.delete_table(id,user):
            LOGGER.error("id not found")
            sys.exit(1)  
        print("lllllllllllla")
        milvus_cli.delete_collection(id)
        print("iiiici")
    except Exception as e:
        LOGGER.error(f"Error with  drop table: {e}")
        sys.exit(1)
