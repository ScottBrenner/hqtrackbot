workflow "New workflow" {
  on = "push"
  resolves = ["GitHub Action for Docker-1"]
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
