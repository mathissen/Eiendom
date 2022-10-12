import argparse
from google.cloud import bigquery
from google.oauth2 import service_account

from sql.join_flom import JOIN_FLOM
from sql.join_kommuneplan import JOIN_KOMMUNEPLAN


parser = argparse.ArgumentParser(description='BQ Processing..')
parser.add_argument("-o", "--Output", help = "Location of local output", required=True)
parser.add_argument("-s", "--ServiceAccount", help = "Location of gcp service account json", required=True)
parser.add_argument("-t", "--JoinType", help = "Select either JOIN_FLOM or JOIN_KOMMUNEPLAN")
args = parser.parse_args()
 
if not args.OutputTablePath or not args.ServiceAccount or not args.JoinType:
    raise Exception("Missing parameters")

if args.JoinType == "JOIN_FLOM":
    sql = JOIN_FLOM
elif args.JoinType == "JOIN_FLOM":
    sql = JOIN_KOMMUNEPLAN
else:
    raise Exception("JoinType must be JOIN_FLOM or JOIN_KOMMUNEPLAN")


credentials = service_account.Credentials.from_service_account_file(
    args.ServiceAccount,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

df = client.query(sql).to_dataframe()

df.to_csv(args.Output, sep=";")


