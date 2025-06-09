from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential
subscription_id="6fab868f-e7ff-4000-b366-b5d0a27cc581",
workspace_name="iat",
resource_group="shafi4"

# Connect to workspace using service principal (CLI) credentials
credential = DefaultAzureCredential()
ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

# 1. Register the H2O-3 MOJO model as a custom model
file_model = Model(
    path="model/my_mojo_model.zip",
    type=AssetTypes.CUSTOM_MODEL,
    name="h2o-mojo-model",
    description="H2O-3 MOJO model"
)
ml_client.models.create_or_update(file_model)  # registers or updates the model:contentReference[oaicite:11]{index=11}

# 2. (Optional) Register or reuse a conda Environment asset from conda.yaml
# [Environment registration code here, if needed]
import uuid

# Creating a unique name for the endpoint
endpoint_name = "iat-shafi-" + str(uuid.uuid4())[:8]

# 3. Create or update the managed online endpoint
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint)  # create endpoint

# 4. Create or update the deployment on the endpoint
deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=endpoint_name,
    model=f"azureml:{file_model.name}:1",    # use registered model version 1
    environment="azureml:my-env:1",        # pre-registered env or create inline
    code_configuration=CodeConfiguration(
        code="src",
        scoring_script="score.py"
    ),
    instance_type="Standard_DS3_v2",
    instance_count=1
)
ml_client.online_deployments.begin_create_or_update(deployment)  # deploy model:contentReference[oaicite:12]{index=12}:contentReference[oaicite:13]{index=13}
