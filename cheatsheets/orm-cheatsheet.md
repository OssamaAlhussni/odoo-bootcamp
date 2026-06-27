# Odoo ORM Cheatsheet

## CRUD

```python
self.env["model"].create({"field": "value"})
record.write({"field": "new_value"})
record.unlink()
self.env["model"].browse(record_id)
self.env["model"].search([("field", "=", "value")])
```

## Domain Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equals |
| `!=` | Not equals |
| `>` | Greater than |
| `<` | Less than |
| `like` | Contains |
| `ilike` | Case-insensitive contains |
| `in` | In list |
| `not in` | Not in list |
| `child_of` | Is child in hierarchy |

## Environment

```python
self.env.user              # Current user
self.env.company           # Current company
self.env.context           # Context dict
self.env.cr                # DB cursor
self.env["model"].sudo()   # Bypass security
self.env.ref("xml_id")     # Get by XML ID
```

## Context Keys

```python
self.env.context.get("active_id")       # Current record ID
self.env.context.get("active_ids")      # Selected IDs
self.env.context.get("active_model")    # Current model
```

## Useful Methods

```python
record.ensure_one()
record.mapped("field")
record.filtered(lambda r: r.field > 5)
record.sorted(key="name")
records.ids
```
