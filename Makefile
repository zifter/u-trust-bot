include .env

dep-up:
	pipenv update --dev

image-build:
	podman build .

tf-init:
	terraform -chdir=deploy/terraform init -backend-config="bucket=${TF_VAR_BACKEND_BUCKET}"

tf-init-upgrade:
	terraform -chdir=deploy/terraform init -upgrade -backend-config="bucket=${TF_VAR_BACKEND_BUCKET}"

tf-plan:
	terraform -chdir=deploy/terraform plan -var="gcp_sa_credentials=${TF_VAR_SERVICE_ACCOUNT}" -out=tfplan

tf-apply:
	terraform -chdir=deploy/terraform apply tfplan
