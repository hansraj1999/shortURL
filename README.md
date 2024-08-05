# shortURL
 shortURL


Run Locally:
./local_setup/local_setup.sh --mode app
./local_setup/local_setup.sh --mode full
./local_setup/local_setup.sh --rebuild
or 
docker compose -f .\docker_compose_full.yml up --scale short_url-local-srvr=3