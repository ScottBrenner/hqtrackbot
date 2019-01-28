workflow "Build and deploy on push" {
  on = "push"
  resolves = ["GitHub Action for AWS"]
}

action "Docker Registry Login" {
  uses = "actions/docker/login@master"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Docker Build" {
  uses = "actions/docker/cli@master"
  needs = ["Docker Registry Login"]
  args = "build -t scottbrenner/hqtrackbot ."
}

action "Docker Push" {
  uses = "actions/docker/cli@master"
  needs = ["Docker Build"]
  args = "push scottbrenner/hqtrackbot:latest"
}

action "GitHub Action for AWS" {
  uses = "actions/aws/cli@master"
  needs = ["Docker Push"]
  args = "--region us-west-1 ecs update-service --cluster hqtrackbot --service hqtrackbot --task-definition hqtrackbot --force-new-deployment"
  secrets = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
}
