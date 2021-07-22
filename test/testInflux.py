import mysql.connector
import datetime
from influxdb_client import InfluxDBClient


def connectInlfux():
  client = InfluxDBClient(url="http://18.116.89.239:8086/", token="jIrsd7-eMaIwRxXI8FnnkeUGCAV7khgQJj3Gk6zVV51dDhB6Q0xM-2jPwM7iZpmOs7OI4lLjWV_1MZU1ouRgDA==", org="nexusproject")
  return client


def getNBpers():
  client = connectInlfux()
  returnData= {}
  query_api = client.query_api()

  query = """from(bucket: "mqttnexus")
    |> range(start: -5m)
    |> filter(fn: (r) => r["source_address"] == "12345678" or r["source_address"] == "13960537" or r["source_address"] == "22361595" or r["source_address"] == "24114793" or r["source_address"] == "51488201" or r["source_address"] == "54158491" or r["source_address"] == "58381714" or r["source_address"] == "60052006" or r["source_address"] == "62061965" or r["source_address"] == "68191831" or r["source_address"] == "69607072" or r["source_address"] == "73214383" or r["source_address"] == "7654321" or r["source_address"] == "94981317" or r["source_address"] == "987654543")
    |> filter(fn: (r) => r["_field"] == "data_value")
    |> filter(fn: (r) => r["_measurement"] == "NbPers" or r["_measurement"] == "Temperature")
    |> filter(fn: (r) => r["topic"] == "WEB2-GROUPE1/12345678/112" or r["topic"] == "WEB2-GROUPE1/12345678/122" or r["topic"] == "WEB2-GROUPE1/13960537/112" or r["topic"] == "WEB2-GROUPE1/13960537/122" or r["topic"] == "WEB2-GROUPE1/22361595/112" or r["topic"] == "WEB2-GROUPE1/22361595/122" or r["topic"] == "WEB2-GROUPE1/24114793/112" or r["topic"] == "WEB2-GROUPE1/24114793/122" or r["topic"] == "WEB2-GROUPE1/51488201/112" or r["topic"] == "WEB2-GROUPE1/51488201/122" or r["topic"] == "WEB2-GROUPE1/54158491/112" or r["topic"] == "WEB2-GROUPE1/54158491/122" or r["topic"] == "WEB2-GROUPE1/58381714/112" or r["topic"] == "WEB2-GROUPE1/58381714/122" or r["topic"] == "WEB2-GROUPE1/60052006/112" or r["topic"] == "WEB2-GROUPE1/60052006/122" or r["topic"] == "WEB2-GROUPE1/62061965/112" or r["topic"] == "WEB2-GROUPE1/62061965/122" or r["topic"] == "WEB2-GROUPE1/68191831/112" or r["topic"] == "WEB2-GROUPE1/68191831/122" or r["topic"] == "WEB2-GROUPE1/69607072/112" or r["topic"] == "WEB2-GROUPE1/69607072/122" or r["topic"] == "WEB2-GROUPE1/73214383/112" or r["topic"] == "WEB2-GROUPE1/73214383/122" or r["topic"] == "WEB2-GROUPE1/7654321/112" or r["topic"] == "WEB2-GROUPE1/7654321/122" or r["topic"] == "WEB2-GROUPE1/94981317/112" or r["topic"] == "WEB2-GROUPE1/94981317/122" or r["topic"] == "WEB2-GROUPE1/987654543/112" or r["topic"] == "WEB2-GROUPE1/987654543/122")
    |> yield(name: "mean")"""


  result = client.query_api().query(org="nexusproject", query=query)

  results = []
  for table in result:
      for record in table.records:
          results.append((record.get_value(), record.get_field(), record.get_measurement(), record.values.get("source_address")))

  for data in results:

    if data[2] == "NbPers":
      returnData[str(data[3])] = { "NbPers" : int(data[0])}
    
    if data[2] == "Temperature":
      returnData[str(data[3])]["Temperature"] = int(data[0])

  return returnData

print(getNBpers())