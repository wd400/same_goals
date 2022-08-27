import sys

from config import MILVUS_HOST, MILVUS_PORT, VECTOR_DIMENSION, METRIC_TYPE
from logs import LOGGER

COLLECTION_NAME="embeddings"
print("00000000000000000")
from pymilvus import  FieldSchema
print(1111111111111)
from pymilvus import  CollectionSchema, DataType, Collection, utility
print("milvus import start")
from pymilvus import connections
print("milvus import end")

class MilvusHelper:
    """
      class
    """
    def __init__(self):
        try:
            print("INIT BEFORE",file=sys.stderr)
            self.collection =None
            connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
            LOGGER.debug(f"Successfully connect to Milvus with IP:{MILVUS_HOST,} and PORT:{MILVUS_PORT}")
        except Exception as e:
            LOGGER.error(f"Failed to connect Milvus: {e}")
            sys.exit(1)
        print("create_collection BEFORE")
        self.set_collection()
        print("create_collection DONE")
        
        self.collection.load()
        print("iiiiiiinit MilvusHelper done")

    def set_collection(self, collection_name=COLLECTION_NAME):
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name)
            else:
                self.create_collection()
            #    raise Exception(f"There has no collection named:{collection_name}")
        except Exception as e:
            LOGGER.error(f"Error: {e}")
            sys.exit(1)

    def has_collection(self, collection_name):
        # Return if Milvus has the collection
        try:
            status = utility.has_collection(collection_name)
            print(",,,,,,,,,,,,",status)
            return status
        except Exception as e:
            LOGGER.error(f"Failed to check collection: {e}")
            sys.exit(1)

    def create_collection(self, collection_name=COLLECTION_NAME):
        # Create milvus collection if not exists
        try:
            if not self.has_collection(collection_name):
                field1 = FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True,auto_id=True)
    #            field2= FieldSchema(name="user", dtype=DataType.STRING,is_primary=False,descrition="user")
                field3 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector", dim=VECTOR_DIMENSION, is_primary=False)
                LOGGER.error(f"SCHEMA  00000")
                #field2,
                schema = CollectionSchema(fields=[ field1,field3], description="collection description")
                LOGGER.error(f"SCHEMA  ")

                self.collection = Collection(name=collection_name, schema=schema)
                LOGGER.debug(f"Create Milvus collection: {self.collection}")
                self.create_index()
            return "OK"
        except Exception as e:
            LOGGER.error(f"Failed to create collection: {e}")
            sys.exit(1)

    def insert(self,  vector):
        # Batch insert vectors to milvus collection
        try:
            self.collection = Collection(name=COLLECTION_NAME)
            data = [vector]
            mr = self.collection.insert(data)
            ids =  mr.primary_keys
        #    self.collection.load()
            return ids
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")
            sys.exit(1)


    def nearest_ids(self, ids, k):
        # Batch insert vectors to milvus collection
        search_params = {"metric_type":  METRIC_TYPE, "params": {"nprobe": 16}}
        try:
            print("BEFORE")
            res=self.collection.search(
                data=ids,
                param=search_params,
                anns_field="embedding",
                output_fields=["id"],
                limit=k*len(ids),
                expr=None
            )
            print("AFTER")
            return res[0].ids[:50]
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")
            sys.exit(1)

    def vector_nearest_ids(self,  embedding,k):
        # Batch insert vectors to milvus collection
        search_params = {"metric_type":  METRIC_TYPE, "params": {"nprobe": 16}}
        try:
            res=self.collection.search(
                data=[embedding],
                param=search_params,
                anns_field="embedding",
                output_fields=["id"],
                limit=k,
                expr=None
            )
            print(res)
            return res[0].ids
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")
            sys.exit(1)

    def id_vectors(self,  ids):
        # Batch insert vectors to milvus collection
        try:
            res=self.collection.query(
             
                output_fields= ["embedding"],
                expr=f"id in {ids}"
            )
            return [x['embedding'] for x in res]
        except Exception as e:
            LOGGER.error(f"Failed to insert data into Milvus: {e}")
            sys.exit(1)

    def create_index(self, collection_name=COLLECTION_NAME):
        # Create IVF_FLAT index on milvus collection
        try:
            self.set_collection(collection_name)
            default_index= {"index_type": "IVF_SQ8", "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
            status= self.collection.create_index(field_name="embedding", index_params=default_index)
            if not status.code:
                LOGGER.debug(
                   f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            LOGGER.error(f"Failed to create index: {e}")
            sys.exit(1)

    def delete_collection(self, id):
         # Delete Milvus collection
        try:
            #TODO: use ==
            self.collection.delete(f"id in [{id}]")
            
            LOGGER.debug("Successfully deleted!")
        except Exception as e:
            LOGGER.error(f"Failed to drop collection: {e}")
            sys.exit(1)

    def search_vectors(self, vectors, top_k):
        # Search vector in milvus collection
        try:
            search_params = {"metric_type":  METRIC_TYPE, "params": {"nprobe": 16}}
            res=self.collection.search(vectors, anns_field="embedding", param=search_params, limit=top_k)
            print(res[0])
            LOGGER.debug(f"Successfully search in collection: {res}")
            return res
        except Exception as e:
            LOGGER.error(f"Failed to search in Milvus: {e}")
            sys.exit(1)

    def count(self, collection_name):
         # Get the number of milvus collection
        try:
            self.set_collection(collection_name)
            num =self.collection.num_entities
            LOGGER.debug(f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            LOGGER.error(f"Failed to count vectors in Milvus: {e}")
            sys.exit(1)

