# Day 1 — Odoo Setup & Architecture

**Date:** June 27, 2026

## What I Learned

### Odoo Architecture
- Odoo follows a **multi-tier architecture**: PostgreSQL → Odoo server (Python) → Web client (OWL)
- **Modules** are the building blocks — each contains models, views, security
- Odoo ORM handles all database interactions automatically

### Setup Process
- Installed PostgreSQL 17
- Set up Python 3.11 virtual environment
- Cloned Odoo 18.0 source from GitHub
- Installed dependencies from `requirements.txt`
- Started Odoo server on port 8069

### Key Commands
```bash
# Start Odoo
python odoo-bin --addons-path=addons -d mydb \
    --db_user=odoo --db_password=odoo --http-port=8069

# Upgrade a module
python odoo-bin -d mydb -u module_name --stop-after-init

# Install a module
python odoo-bin -d mydb -i module_name --stop-after-init
```

### Issues & Fixes
- PostgreSQL 17 had DLL init error (0xC0000142) — removed incompatible plpython3/plperl DLLs
- Used fresh `initdb` data directory instead of the old one

## Key Commands
```bash
pg_ctl start -D <data_dir>         # start PostgreSQL
pg_ctl stop -D <data_dir> -m fast  # stop PostgreSQL
psql -U postgres -c "SQL"          # run SQL
pg_isready -h localhost            # check if running
```

## Resources
- [Odoo Installation Docs](https://www.odoo.com/documentation/18.0/administration/install/install.html)
- [Odoo Developer Tutorials](https://www.odoo.com/documentation/18.0/developer/tutorials.html)
