import argparse
import time
from google.cloud import bigquery
from google.cloud import storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


from sql.join_flom import JOIN_FLOM


# parser = argparse.ArgumentParser(description = "Output table path in BQ")
# parser.add_argument("-f", "--OutputTablePath", help = "Location of output table in BQ")
# args = parser.parse_args()
 
# if args.OutputTablePath:
#     FILE_PATH = args.FilePath
# else:
#     raise Exception("Output destination in GCP must be speficied")

output_location_gcp="gs://mathis_temp/matrikkel_flom*.csv"
output_local=r"C:/Users/themg/Downloads/matrikkel_flom.csv"

client = bigquery.Client()

# Run job in BQ
query_job = client.query(JOIN_FLOM.format(output_location=output_location_gcp))  

while(query_job.state != 'DONE'):
    if query_job.error_result:
        print(f"Query failed: {query_job.error_result}")
        raise Exception("Query invalid")
    time.sleep(30)
    query_job.reload()

if len(query_job.error_result) > 0:
    with open(output_local) as file_obj:
        client.download_blob_to_file(
            output_location_gcp, file_obj)
else:
    print("failed...")