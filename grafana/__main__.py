import pulumi
import pulumi_docker as docker
from pulumi_gcp import cloudrun, storage, serviceaccount, projects
import lbrlabs_pulumi_grafana as grafana
import json

# Retrieve the GCP project and location.
project = pulumi.Config("gcp").require("project")
region = pulumi.Config("gcp").get("region") or "us-central1"

# Create a new service account
service_account = serviceaccount.Account("grafana-datasource",
                                         account_id="grafana-datasource",
                                         display_name="Service Account for Grafana to fetch from data source")

# Grant BigQuery Admin role to the service account
bigquery_admin = projects.IAMMember("bigquery-admin",
    member=f"serviceAccount:{service_account.email}",
    role="roles/bigquery.admin",
    project=project)

key = serviceaccount.Key("grafana-datasource-key",
    service_account_id=service_account.name,
    public_key_type="TYPE_X509_PEM_FILE")

# Export the service account key file path
json_key = key.private_key

# Create a storage bucket for the Grafana configuration.
config_bucket = storage.Bucket("grafana-config", location=region)

# Create a Google Cloud Run service for Grafana.
grafana_image = "grafana/grafana"
grafana_service = cloudrun.Service(
    "grafana-service",
    location=region,
    template=cloudrun.ServiceTemplateArgs(
        spec=cloudrun.ServiceTemplateSpecArgs(
            containers=[
                cloudrun.ServiceTemplateSpecContainerArgs(
                    image=grafana_image,
                    envs=[
                        cloudrun.ServiceTemplateSpecContainerEnvArgs(
                            name="GF_SERVER_HTTP_PORT", value="8080"
                        ),
                        # cloudrun.ServiceTemplateSpecContainerEnvArgs(
                        #     name="GF_PATHS_CONFIG",
                        #     value=config_bucket.url.apply(lambda url: url + "/grafana.ini")
                        # ),
                    ],
                )
            ],
        ),
    ),
    autogenerate_revision_name=True,
    traffics=[cloudrun.ServiceTrafficArgs(percent=100)],
    opts=pulumi.ResourceOptions(depends_on=[config_bucket]),
)

# Create an IAM member to make the service publicly accessible.
invoker = cloudrun.IamMember(
    "invoker",
    cloudrun.IamMemberArgs(
        location=region,
        service=grafana_service.name,
        role="roles/run.invoker",
        member="allUsers",
    ),
)

# Export the Grafana Cloud Run URL.
grafana_instance_url = grafana_service.statuses.apply(lambda statuses: statuses[0].url)
pulumi.export("grafana_url", grafana_instance_url)