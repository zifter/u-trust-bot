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
* https://registry.terraform.io/providers/hashicorp/google/latest/docs
* https://registry.terraform.io/providers/integrations/github/latest/docs
* https://registry.terraform.io/providers/hashicorp/random/latest/docs
* https://cloud.google.com/iam/docs/understanding-roles
* https://docs.github.com/en/actions/learn-github-actions/variables

# TODO
Инициализация ссылки. А нужно ли она для передачи в cloud run?
* Перенести секреты в Secret Manager
Пайплайн для тестов
