from CONF import DB_TYPE, DB_INDEX_TYPE, DB_LOCATION, DB_NAME, DB_COLLECTION_NAME, DB_EMB_DIMENSION, DB_USER, DB_PASSWD

if DB_TYPE == "milvus" or DB_TYPE == "milvus_lite":
    from pymilvus import connections, MilvusClient
    class MilvusDB:
        def __init__(self):
            self.db_type = DB_TYPE
            self.client = None
            if self.db_type == 'milvus':
                connections.connect(user=DB_USER, password=DB_PASSWD, uri=DB_LOCATION, db_name=DB_NAME)
                self.client = MilvusClient(uri=DB_LOCATION, db_name=DB_NAME)
                self.client.load_collection(DB_COLLECTION_NAME)
            elif self.db_type == 'milvus_lite':
                self.client = MilvusClient(DB_LOCATION)
                if DB_COLLECTION_NAME not in self.client.list_collections():
                    self.client.create_collection(DB_COLLECTION_NAME, dimension=DB_EMB_DIMENSION)
                else:
                    self.client.load_collection(DB_COLLECTION_NAME)
            else:
                raise "Unknown database type"

        def search_db(self, emb, limit=10, output_field="file_path", search_params=None):
            if not search_params:
                search_params = {
                        "metric_type": "COSINE",
                        "params": {"nprobe": 100}
                    }
            db_resp = self.client.search(
                collection_name=DB_COLLECTION_NAME,
                data=emb,
                limit=limit,
                output_fields=[output_field],
                search_params=search_params
            )[0]

            results = []

            for each in db_resp:
                results.append(each["entity"][output_field])
            return results

        def insert_db(self, embs: list, file_paths: list):
            self.client.insert(DB_COLLECTION_NAME, data=dict(zip(embs, file_paths)))

if __name__ == '__main__':
    milvus_db = MilvusDB()
    print(milvus_db.search_db([[0.1]*1024]))