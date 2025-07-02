# Start the compose stack and log output to nfl_docker.log
docker-compose up --build *>&1 | Tee-Object -FilePath nfl_docker.log -Append

