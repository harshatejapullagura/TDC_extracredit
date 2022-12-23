# from gcloud import logging
# client = logging.Client()
# logger = client.logger('log_name')
# logger.log_text("A simple entry")  # API call
# entries, token = logger.list_entries()
# for entry in entries:
#     print(entry.payload)


# init credentials
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file("prject-key.json")

# create client
import google.cloud.run_v2 as run_v2
run_client = run_v2.ServicesClient(credentials=credentials)

# build request
from google.cloud.run_v2 import ListServicesRequest
request = ListServicesRequest(
    parent="projects/{projectnumber}/locations/{location}"
)

# response
response = run_client.list_services(request=request)