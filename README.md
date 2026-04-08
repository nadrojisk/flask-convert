# FlaskConvert

## Description

Simple Flask application that converts different bases based on user input.

## Setup (Bare metal)

Ensure Python3 and pipenv are installed on your system. After that install the dependencies required by the project:

`pipenv install`

After that spin up the server. It should be accessible at http://localhost:5000

`pipenv run python app.py`

## Setup (Docker)

The Docker Compose configuration includes [Caddy](https://caddyserver.com/) as a reverse proxy with automatic HTTPS via Cloudflare DNS. This setup uses a custom Caddy image with the Cloudflare DNS plugin (`ghcr.io/caddybuilds/caddy-cloudflare`).

**Prerequisites:**

- Docker and docker-compose installed
- A Cloudflare API token with DNS edit permissions for your domain

**Configuration:**

Update the `Caddyfile` with your domain. Caddy will handle TLS automatically using the Cloudflare DNS challenge:

```caddy
your.domain.com {
    reverse_proxy flask_convert:5000

    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
}
```

**Running:**

Set your Cloudflare API token and start the stack:

```bash
export CLOUDFLARE_API_TOKEN=your_token_here
docker-compose up -d
```

The app will be accessible at your configured domain on ports 80 and 443 (HTTP/3 via UDP also supported).
