from odoo.tests import TransactionCase


class TestLibraryBook(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Book = self.env["library.book"]
        self.Category = self.env["library.category"]
        self.Member = self.env["library.member"]
        self.Borrow = self.env["library.borrow"]

        self.category = self.Category.create({"name": "Test Category"})
        self.book = self.Book.create({
            "name": "Test Book",
            "author": "Test Author",
            "isbn": "9780061120084",
            "category_id": self.category.id,
        })
        self.member = self.Member.create({
            "name": "Test Member",
            "email": "test@example.com",
        })

    def test_book_creation(self):
        self.assertEqual(self.book.state, "draft")
        self.assertEqual(self.book.author, "Test Author")

    def test_book_available_flow(self):
        self.book.action_available()
        self.assertEqual(self.book.state, "available")

    def test_book_borrow_flow(self):
        self.book.action_available()
        borrow = self.Borrow.create({
            "book_id": self.book.id,
            "member_id": self.member.id,
            "expected_return_date": "2026-07-15",
        })
        self.assertEqual(borrow.state, "ongoing")
        self.assertEqual(self.book.state, "borrowed")

    def test_book_return_flow(self):
        self.book.action_available()
        borrow = self.Borrow.create({
            "book_id": self.book.id,
            "member_id": self.member.id,
            "expected_return_date": "2026-07-15",
        })
        borrow.action_return()
        self.assertEqual(borrow.state, "returned")
        self.assertEqual(self.book.state, "available")

    def test_isbn_validation(self):
        with self.assertRaises(Exception):
            self.Book.create({
                "name": "Bad Book",
                "isbn": "123",
            })
