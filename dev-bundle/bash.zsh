git clone --recursive https://github.com/dv-net/dv-bundle.git
cd dv-bundle
cp .env.example .env  # Configure environment variables if necessary
docker compose up -d
# Update all submodules to the latest versions
git submodule update --remote

# Rebuild and restart services
docker compose up --build -d
git submodule update --init --recursive
docker compose down -v && docker compose up --build -d
docker compose down && docker compose up --build -d
$ sudo bash -c "$(curl -fsSL https://dv.net/install.sh)"
$ nano /etc/nginx/conf.d/{your_domain or subdomain}.conf
