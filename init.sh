python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "POSTGRES_DB=example_db
POSTGRES_USER=postgres
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=example_password
" > .env

docker compose up -d

python manage.py createsuperuser
