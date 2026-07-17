# Setup Notes — εκκρεμότητες πριν το πρώτο πραγματικό deployment

## Domain (δωρεάν εναλλακτική αντί για αγορά)

Χρησιμοποίησε DuckDNS (https://www.duckdns.org) — δωρεάν subdomain
(π.χ. nickbs-flasky.duckdns.org), δουλεύει κανονικά με Certbot/Let's
Encrypt, καμία διαφορά στη διαδικασία SSL από πραγματικό αγορασμένο
domain.

Βήματα:
1. Sign in στο duckdns.org (με GitHub/Google account)
2. Δημιούργησε subdomain, βάλε το IP του VPS σου
3. Χρησιμοποίησε αυτό το subdomain ως server_name στο nginx config
   και ως -d flag στο certbot command

## VPS provider

Εκκρεμεί: DigitalOcean signup, blocked στο billing verification step
(κάρτα δεν περνούσε authorization hold). Πιθανή αιτία: online/διεθνείς
συναλλαγές μπλοκαρισμένες by default στην τράπεζα/Revolut — έλεγξε
ρύθμιση "online payments" στην εφαρμογή πριν ξαναδοκιμάσεις.

Εναλλακτικές αν ξαναχτυπήσει πρόβλημα: Hetzner Cloud, ή ξαναδοκίμασε
Oracle Cloud Free Tier (Ελλάδα δεν εμφανιζόταν στη λίστα χωρών κατά
το πρώτο signup attempt — άξιζε δεύτερη ματιά/retry).

## DATABASE_URL format (χωρίς Docker, native Postgres στο VPS)

    postgresql://<db_user>:<db_password>@localhost:5432/flasky

Σημείωση: εδώ το host είναι "localhost" (όχι "db" όπως στο Docker
Compose) — γιατί η Postgres τρέχει native πάνω στο ίδιο VPS, όχι σε
ξεχωριστό container με δικό του network.

## Πραγματικά credentials (ΝΑ ΜΗΝ μπουν ποτέ στο git)

SECRET_KEY, MAIL_PASSWORD, DATABASE_URL password: μόνο μέσα στο .env
του VPS, ποτέ committed. Το .gitignore ήδη τα καλύπτει.

## Πρώτη πραγματική δοκιμή — checklist πριν θεωρηθεί "done"

- [ ] VPS δημιουργημένο, SSH σύνδεση επιβεβαιωμένη
- [ ] DuckDNS subdomain δείχνει σωστά στο IP (ping <domain> το επιβεβαιώνει)
- [ ] flask deploy έτρεξε επιτυχώς πάνω στην πραγματική Postgres
- [ ] systemctl status flasky -> active (running)
- [ ] http://<domain> προσβάσιμο
- [ ] certbot ολοκληρώθηκε, https://<domain> προσβάσιμο με valid cert
- [ ] δοκιμή "μελλοντικό deployment" flow (git pull + restart) μία φορά
