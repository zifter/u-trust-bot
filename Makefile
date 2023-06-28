include .env

.EXPORT_ALL_VARIABLES:

dep-up:
	pipenv update --dev
	pipenv clean



#######
# LOCAL
local-test:
	pipenv run pytest . --cov=src
	start htmlcov/index.html

#######
# IMAGE
podman-login:
	gcloud auth print-access-token --quiet | podman login -u oauth2accesstoken --password-stdin ${GCP_ARTIFACT_REGISTRY}

image-build:
	podman build . -t ${IMAGE_TAG}

image-push:
	podman push ${IMAGE_TAG}

image-run:
	podman run ${IMAGE_TAG}

image-test:
	podman run ${IMAGE_TAG} pytest . --cov=src

#######
# INFRA
infra-tf-init:
	terraform -chdir=deploy/infra/terraform init -backend-config="bucket=${TF_STATE_INFRA_BUCKET}"

infra-tf-init-upgrade:
	terraform -chdir=deploy/infra/terraform init -upgrade -backend-config="bucket=${TF_STATE_INFRA_BUCKET}"

infra-tf-plan:
	terraform -chdir=deploy/infra/terraform plan -out=tfplan

infra-tf-apply:
	terraform -chdir=deploy/infra/terraform apply tfplan

infra-tf-destroy:
	terraform -chdir=deploy/infra/terraform destroy

#######
# APP
app-tf-init:
	terraform -chdir=deploy/app/terraform init -backend-config="bucket=${TF_STATE_APP_BUCKET}"

app-tf-init-upgrade:
	terraform -chdir=deploy/app/terraform init -upgrade -backend-config="bucket=${TF_STATE_APP_BUCKET}"

app-tf-plan:
	terraform -chdir=deploy/app/terraform plan -out=tfplan

app-tf-apply:
	terraform -chdir=deploy/app/terraform apply tfplan

app-tf-destroy:
	terraform -chdir=deploy/app/terraform destroy
