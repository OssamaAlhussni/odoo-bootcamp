from odoo import api, fields, models


class LibraryBorrowWizard(models.TransientModel):
    _name = "library.borrow.wizard"
    _description = "Borrow Book Wizard"

    member_id = fields.Many2one("library.member", string="Member", required=True)
    expected_return_date = fields.Date(string="Expected Return", required=True)

    def action_borrow(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        books = self.env["library.book"].browse(active_ids)
        for book in books:
            if book.state != "available":
                continue
            self.env["library.borrow"].create({
                "book_id": book.id,
                "member_id": self.member_id.id,
                "expected_return_date": self.expected_return_date,
            })
            book.state = "borrowed"
        return {"type": "ir.actions.act_window_close"}
