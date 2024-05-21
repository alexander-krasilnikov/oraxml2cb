#!/usr/bin/env python3

import oracledb
import random
import string
import xml.etree.ElementTree as ET
import uuid
from mimesis import Datetime

ORACLE_DSN = "dbora.crz5ktxlyqu4.eu-central-1.rds.amazonaws.com/ORCL"
ORACLE_USER = "admin"
ORACLE_PASSWORD = "XXXXX"

# Connect to Oracle database
connection = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)

# Create a cursor object
cursor = connection.cursor()

# Function to generate random XML data
def generate_dp_data():
    num_value = random.choice([random.randint(1, 100), random.uniform(0, 100)])  # Random integer or float
    string_value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Random string of 10 characters
    bool_value = random.choice([True, False])  # Random boolean

    vector_values = [round(random.uniform(0, 100),5) for _ in range(10)]  # Vector of 10 random float values

    dp_value = ET.Element("dp_data")

    num_value_element = ET.SubElement(dp_value, "num_value")
    num_value_element.text = str(num_value)

    string_value_element = ET.SubElement(dp_value, "string_value")
    string_value_element.text = string_value

    bool_value_element = ET.SubElement(dp_value, "bool_value")
    bool_value_element.text = str(bool_value).lower()

    vector_value_element = ET.SubElement(dp_value, "vector")
    for value in vector_values:
        vector_value_element.append(ET.Element("vector_value"))
        vector_value_element[-1].text = str(value)

    return ET.tostring(dp_value, encoding="unicode")

# Insert 100 random XML data
dt = Datetime()
for _ in range(1000):
    cursor.execute("INSERT INTO ADMIN.DATAPOINT_ARCHIVE (UUID, DP_ID, DP_TIMESTAMP, DP_DATA) VALUES (null, :dp_id, :dp_timestamp, :dp_data)",
                    dp_id = f"{str(uuid.uuid4())[:4]}/{str(uuid.uuid4())[:4]}/{str(uuid.uuid4())[:4]}",  
                    dp_timestamp = dt.datetime(start=2020, end=2023).strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    dp_data = generate_dp_data()
    )

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()