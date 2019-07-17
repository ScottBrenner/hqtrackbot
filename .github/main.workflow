workflow "Build and deploy on push" {
  on = "push"
  resolves = ["CDK Synth"]
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

action "CDK Synth" {
  uses = "docker://scottbrenner/aws-cdk:master"
  needs = ["Docker Push"]
  args = "--app python3 app.py cdk-fargate/synth"
  secrets = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
}
