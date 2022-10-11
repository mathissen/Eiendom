import argparse
from google.cloud import bigquery
from google.oauth2 import service_account

from sql.join_flom import JOIN_FLOM


parser = argparse.ArgumentParser(description='BQ Processing..')
parser.add_argument("-f", "--Output", help = "Location of local output")
parser.add_argument("-f", "--ServiceAccount", help = "Location of gcp service account json")
args = parser.parse_args()
 
if not args.OutputTablePath or not args.ServiceAccount:
    raise Exception("Missing parameters")


credentials = service_account.Credentials.from_service_account_file(
    args.ServiceAccount,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)


df = client.query(JOIN_FLOM).to_dataframe()

df.to_csv(args.Output, sep=";")


