# Deployment Guide — flask-grinberg σε VPS (χωρίς Docker)

Οδηγός βήμα-βήμα για deployment σε φρέσκο Ubuntu VPS. Προϋποθέτει: VPS
με Ubuntu 24.04, SSH key ήδη προστιθεμένο στον provider, domain (ή
δωρεάν DuckDNS subdomain) που δείχνει στο IP του VPS.

## 1. Πρώτη σύνδεση & βασικό provisioning

    ssh root@<VPS_IP>

    # Δημιουργία non-root user για την εφαρμογή
    adduser deploy
    usermod -aG sudo deploy

    # Firewall — άνοιξε μόνο ό,τι χρειάζεται
    ufw allow OpenSSH
    ufw allow 'Nginx Full'
    ufw enable

    # SSH hardening (προαιρετικό αλλά προτεινόμενο):
    # απενεργοποίησε root login, password authentication
    # (μόνο SSH key) στο /etc/ssh/sshd_config

## 2. Εγκατάσταση dependencies

    sudo apt update
    sudo apt install python3-venv python3-pip nginx postgresql \
        postgresql-contrib libpq-dev

## 3. Βάση δεδομένων (Postgres)

    sudo -u postgres createuser --interactive
    sudo -u postgres createdb flasky

## 4. Κώδικας εφαρμογής

    # ως user "deploy"
    git clone <repo-url> flask-grinberg
    cd flask-grinberg
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements/prod.txt

    # Αντέγραψε/φτιάξε το .env με σωστό DATABASE_URL, SECRET_KEY, κλπ.

    flask deploy   # migrations + roles

## 5. Gunicorn ως systemd service

    sudo cp deployment/gunicorn/flasky.service \
        /etc/systemd/system/flasky.service
    sudo systemctl start flasky
    sudo systemctl enable flasky
    sudo systemctl status flasky   # επιβεβαίωση ότι τρέχει

## 6. nginx reverse proxy

    sudo cp deployment/nginx/flasky.conf \
        /etc/nginx/sites-available/flasky
    sudo ln -s /etc/nginx/sites-available/flasky \
        /etc/nginx/sites-enabled/
    sudo nginx -t          # έλεγχος συντακτικού πριν restart
    sudo systemctl restart nginx

Στο σημείο αυτό, το site πρέπει να είναι προσβάσιμο μέσω
http://<domain> (χωρίς SSL ακόμα).

## 7. SSL μέσω Certbot/Let's Encrypt

    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d flasky.example.com

Το Certbot ενημερώνει αυτόματα το nginx config για HTTPS,
και ρυθμίζει αυτόματη ανανέωση certificate.

## 8. Μελλοντικά deployments (μετά από νέο κώδικα)

    cd flask-grinberg
    git pull
    source .venv/bin/activate
    pip install -r requirements/prod.txt
    flask deploy
    sudo systemctl restart flasky
