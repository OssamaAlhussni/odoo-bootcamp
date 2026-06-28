# Day 2 — Real Estate Workshop Module

## What I Did
- Fixed a broken Odoo workshop module: reconstructed all Python model files from `.pyc` bytecode
- Wrote complete views, menus, security for the estate module
- Added educational comments to every file explaining Odoo concepts

## Module Structure

```
estate/
├── __init__.py           # Package init — imports models
├── __manifest__.py       # Module info — name, depends, data files
├── models/
│   ├── __init__.py       # Imports all model files
│   ├── estate_property.py       # Main model (15 fields, computed, actions)
│   ├── estate_property_type.py  # Property categories
│   ├── estate_property_tag.py   # Colored tags
│   ├── estate_property_offer.py # Offers (accept/refuse workflow)
│   └── res_users.py             # Extended user model (inheritance)
├── security/
│   └── ir.model.access.csv      # ACL permissions
└── views/
    ├── estate_menus.xml                # Menu structure
    ├── estate_property_views.xml       # Tree, form, kanban, search
    ├── estate_property_type_views.xml  # Type tree + form
    ├── estate_property_tag_views.xml   # Tag tree + form
    ├── estate_property_offer_views.xml # Offer tree + form
    └── res_users_views.xml             # User form inheritance
```

## Odoo Concepts Learned

| Concept | What it means |
|---------|--------------|
| `_name` | Technical model name (dots → DB underscores) |
| `fields.Char/Text/Float/Integer/Boolean` | Field types = DB column types |
| `compute` | Field value calculated from other fields |
| `@api.depends` | Tells Odoo when to recompute |
| `@api.constrains` | Python-level validation |
| `_sql_constraints` | DB-level validation (UNIQUE, CHECK) |
| `Many2one → One2many` | Parent-child relationship |
| `Many2many` | Both-sides-many relationship |
| `_inherit` (no _name) | Extension inheritance (add to existing model) |
| `view_mode` | Which views to offer (tree, form, kanban, etc.) |
| `inherit_id` + XPath | View inheritance (extend existing views) |

## How to Install & Test
```powershell
cd C:\Users\TUF GAMING\odoo
python odoo-bin -d odoo_db -u estate --stop-after-init
```
Then open Odoo → Apps → Real Estate → Properties
