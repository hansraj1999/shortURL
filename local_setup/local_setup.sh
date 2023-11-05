#!/usr/bin/env bash

# Initialize variables
mode=""
rebuild=""
docker_compose_shared_file_name=""
declare -A data_directories=(
    [mongoSharedVolume]=/Users/$USER/bithash/docker-data/mongodb/db
    [redisSharedVolume]=/Users/$USER/bithash/docker-data/redis/data
)

for i in ${data_directories[@]}

    do
        if [[ -d $i ]]; then
            echo "data directory $i already exists, Reusing it."
        else
            echo "data directory $i doesn't exists, Creating it."
            mkdir -p $i
        fi
    done
echo "Data directory creation/verification complete"

echo "Exporting data directory information to operating system"
for i in ${!data_directories[@]}
    do
        echo "Exporting $i=${data_directories[$i]}"
        export $i=${data_directories[$i]}
    done
echo "Done!"
echo "setting up fyndnet for connecting containers..."
    network_list=$(docker network list --format '{{.Name}}')
    if echo $network_list | grep -q "bithash"; then
        echo "existing network found, reusing it";
    else
        echo "Creating new network";
        docker network create bithash > /dev/null 2>&1
        echo "Done!"
    fi
# Function to display usage information
usage() {
  echo "Usage: $0 [--mode <mode>] [--rebuild]"
  echo "  --mode: 'full' or 'app' (optional if --rebuild is present)"
  echo "  --rebuild: 'rebuild'"
  exit 1
}

# Loop through the command line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --mode)
      shift
      mode="$1"
      ;;
    --rebuild)
      rebuild="rebuild"
      ;;
    *)
      echo "Error: Unknown option: $1"
      usage
      ;;
  esac
  shift
done

# Check and validate the 'rebuild' argument
if [ -n "$rebuild" ] && [ "$rebuild" != "rebuild" ]; then
  echo "Error: Invalid 'rebuild' argument. It should be 'rebuild'."
  usage
fi
# Perform actions based on the arguments
if [ -n "$rebuild" ]; then
  echo "Rebuild is requested."
  
  docker-compose -f "./local_setup/docker_compose_full.yml" up  -d --build
else
  # If rebuild is not requested, validate the 'mode' argument
  if [ -n "$mode" ]; then
    if [ "$mode" != "full" ] && [ "$mode" != "app" ]; then
      echo "Error: Invalid 'mode' argument. It should be 'full' or 'app'."
      usage
    else
      echo "Mode is set to: $mode"
      if [ "$mode" == "full" ]; then
        echo "performing actions for mode=full."
        docker-compose -f "./local_setup/docker_compose_full.yml" up  -d
      elif [ "$mode" == "app" ]; then
        echo "performing actions for mode=app."
        docker-compose -f "./local_setup/docker_compose_app.yml" up  -d
      fi
    fi
  else
    echo "Error: Please provide '--mode' or '--rebuild'."
    usage
  fi
fi
