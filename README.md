# u-trust-bot
Telegram Personal Assistant

## Prepare

### Local
Setup development access
```commandline
gcloud auth application-default login
```

Put here everything for deployment
```commandline
touch .env
```

### Project
* Create project
* Create service account for terraform (Project Editor + Service Usage Admin, Project IAM Admin)
* Create bucket fot tf-state


# References:
## Terraform
* https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints
* https://registry.terraform.io/providers/hashicorp/google/latest/docs
* https://registry.terraform.io/providers/integrations/github/latest/docs
* https://registry.terraform.io/providers/hashicorp/random/latest/docs


## Github
* https://docs.github.com/en/actions/learn-github-actions/variables

## GCP
### Cloud
* https://cloud.google.com/iam/docs/understanding-roles

### Python
https://github.com/googleapis/python-ndb/blob/main/tests/system/test_crud.py


### e2e
* https://shallowdepth.online/posts/2021/12/end-to-end-tests-for-telegram-bots/