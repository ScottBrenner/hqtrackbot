workflow "New workflow" {
  on = "push"
  resolves = ["GitHub Action for AWS"]
}

action "Docker Registry" {
  uses = "actions/docker/login@76ff57a"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "GitHub Action for Docker" {
  uses = "actions/docker/cli@76ff57a"
  needs = ["Docker Registry"]
  args = "build -t scottbrenner/hqtrackbot ."
}

action "GitHub Action for Docker-1" {
  uses = "actions/docker/cli@76ff57a"
  needs = ["GitHub Action for Docker"]
  args = "push scottbrenner/hqtrackbot:latest"
}

action "GitHub Action for AWS" {
  uses = "actions/aws/cli@8d31870"
  needs = ["GitHub Action for Docker-1"]
  args = "ecs update-service --service hqtrackbot --force-new-deployment"
  secrets = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
}
