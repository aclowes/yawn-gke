move files to https://cloud.google.com/container-optimized-os/docs/concepts/disks-and-filesystem

gcloud compute --project "wise-vim-178017" ssh --zone "us-west1-b" "yawn-server" -- -L 2222:/var/run/docker.sock -N &
export DOCKER_HOST=localhost:2222

https://hub.docker.com/r/jwilder/nginx-proxy
https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion

# move the database on first run
docker-compose up -d postgres
docker-compose exec -u postgres postgres bash
psql -U yawn yawn

kubectl exec -it postgres-db-66f698c77-8hb28 -- su postgres -c 'pg_dump -U yawn yawn' > db.sql

docker cp db.sql d7b9dda38af4:/var/lib/postgresql/
psql -U yawn yawn -f /var/lib/postgresql/db.sql

curl -v --resolve yawn.live:8000:127.0.0.1 yawn.live:8000

# delete the worker to free space
docker-compose stop worker
docker-compose rm worker
docker-compose up -d worker
