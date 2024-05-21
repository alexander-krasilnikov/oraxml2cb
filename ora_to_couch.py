import oracledb
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import xmltodict
import ast

ORACLE_DSN = "dbora.crz5ktxlyqu4.eu-central-1.rds.amazonaws.com/ORCL"
ORACLE_USER = "admin"
ORACLE_PASSWORD = "XXXXX"

COUCHBASE_URL = "couchbase://localhost"
COUCHBASE_USER = "root"
COUCHBASE_PASSWORD = "XXXXX"
def auto_cast_str(val):
  # Try fails if cannot eval, therefore is string
  try:
    val = ast.literal_eval(val)
  except:
    pass
  return val

def xml_postprocessor(path, key, value):
  # XML standard requires lower case bools
  if value == "true": value = "True"
  if value == "false": value = "False"
  return key, auto_cast_str(value)

# Connect to Oracle database
oracle_connection = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
oracle_cursor = oracle_connection.cursor()

# Connect to Couchbase
authenticator = PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD)

cluster_options = ClusterOptions(authenticator=authenticator)
cluster = Cluster(COUCHBASE_URL, authenticator=authenticator)
bucket = cluster.bucket("eso").scope('archive').collection('datapoint')

# Fetch data from Oracle
oracle_cursor.execute("SELECT uuid, dp_id, dp_timestamp, dp_data, replace(to_char(archive_date, 'YYYY-MM-DD HH24:MI:SS'), ' ', 'T') FROM datapoint_archive")
rows = oracle_cursor.fetchall()

# Transfer data to Couchbase
for row in rows:
    uuid = row[0]
    dp_id = row[1]
    dp_timestamp = row[2]
    dp_data = row[3]
    archive_date = row[4]

    # Convert XML to JSON
    dp_data = xmltodict.parse(dp_data, postprocessor=xml_postprocessor)

    # Insert into Couchbase
    key = f"uuid::{uuid}"
    value = {
        "dp_id": dp_id,
        "dp_timestamp": dp_timestamp,
        "archive_date": archive_date
    }
    value.update(dp_data)
    bucket.upsert(key, value)

# Close connections
oracle_cursor.close()
oracle_connection.close()
cluster.close()

