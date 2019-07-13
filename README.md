# Usage

## Add id infomation to .env file

```
cat << EOF >> .env
UID=$(id -u)
GID=$(id -g)
EOF
```

## Building container

```
docker-compose build
```

## Starting container

```
docker-compose up -d
```

## Exec tests

```
docker-compose exec app pipenv run scripts/run_tests
```
