import sys
import numpy as np
import pandas as pd

sys.path.append("..")
from config import DEFAULT_TABLE
from logs import LOGGER


# Import vectors to Milvus and data to Mysql respectively
def do_load(todo, user, model, milvus_client, mysql_cli):

    collection_name = DEFAULT_TABLE
    embedding=model.sentence_encode([todo])

    print("embedded")
    id = milvus_client.insert( embedding)[0]
    print("milvus_client insered")
 #   milvus_client.create_index(collection_name)
  #  mysql_cli.create_mysql_table(collection_name)
    mysql_cli.load_data_to_mysql( id, user, todo)
    return id
    
