from pymongo import MongoClient


class MongoConnection:
    def __init__(self, user: str, password: str, host: str, port: str = "27017"):
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def create_client(self):
        """
        Beware NOT fork safe, in practice this means err on the side of
        excessive client creation as opposed to re-use.
        """

        # below logic is to deal with replica set / multiple mongo nodes
        # more info at https://stackoverflow.com/a/42530573
        if len(self._host.split(",")) == 1:
            conn_str = self._host + ":" + self._port
        else:
            # script can now accept comma delimited list of hosts
            # e.g. "host1,host2,host3" no spaces and no [ ]
            hosts = self._host.split(",")
            hosts_with_ports = list(map(lambda x: f"{x}:{self._port}", hosts))
            conn_str = ",".join(hosts_with_ports)

        mongo_client = MongoClient(
            conn_str,
            username=self._user,
            password=self._password,
            maxPoolSize=100,  # default
            authSource="beholdai",
        )
        return mongo_client

    def get_collection(self, collection_name: str):
        db = self.create_client()["beholdai"]
        return db[collection_name]
