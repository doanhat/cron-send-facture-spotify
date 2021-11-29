PROJECT_NUMBER = "400279913492"

.PHONY: terraform-init
terraform-init:
	cd terraform/ && terraform init

.PHONY: terraform-plan
terraform-plan:
	cd terraform/ && terraform plan

.PHONY: terraform-apply
terraform-apply:
	export GOOGLE_PROJECT=$(PROJECT_NUMBER)
	export TF_VAR_credentials=$(GOOGLE_APPLICATION_CREDENTIALS)
	cd terraform/ && terraform apply -auto-approve

.PHONY: terraform-destroy
terraform-destroy:
	export GOOGLE_PROJECT=$(PROJECT_NUMBER)
	export TF_VAR_credentials=$(GOOGLE_APPLICATION_CREDENTIALS)
	cd terraform/ && terraform apply -destroy