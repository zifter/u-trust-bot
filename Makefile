include .env

.EXPORT_ALL_VARIABLES:


dep-up:
	pipenv update --dev
	pipenv clean


#######
# IMAGE
image-build: IMAGE_TAG := test
image-build:
	podman build . -t ${IMAGE_TAG}

image-push: IMAGE_TAG := test
image-push:
	podman push ${IMAGE_TAG}

image-run: IMAGE_TAG := test
image-run:
	podman run ${IMAGE_TAG}

image-test: IMAGE_TAG := test
image-test:
	podman run ${IMAGE_TAG} pytest .

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

#######
# APP
app-tf-init:
	terraform -chdir=deploy/app/terraform init -backend-config="bucket=${TF_STATE_APP_BUCKET}"

app-tf-init-upgrade:
	terraform -chdir=deploy/app/terraform init -upgrade -backend-config="bucket=${TF_STATE_APP_BUCKET}"

app-tf-plan:
	terraform -chdir=deploy/app/terraform plan -var="gcp_sa_credentials=${TF_VAR_SERVICE_ACCOUNT}" -out=tfplan

app-tf-apply:
	terraform -chdir=deploy/app/terraform apply tfplan
