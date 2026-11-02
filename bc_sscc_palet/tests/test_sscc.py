from odoo.exceptions import UserError
from odoo.tests import TransactionCase
from odoo.tools.barcode import check_barcode_encoding
from psycopg2 import IntegrityError


class TestSscc(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create(
            {"name": "Compañía A", "prefijo_gs1": "8412345"}
        )
        cls.company_b = cls.env["res.company"].create(
            {"name": "Compañía B", "prefijo_gs1": "841234567"}
        )
        cls.Package = cls.env["stock.package"]

    def test_public_gs1_example(self):
        self.assertEqual(self.Package._sscc_check_digit("10614141123456789"), "7")

    def test_company_a_sscc(self):
        package = self.Package.with_company(self.company_a).create({"name": "PALLET-A"})

        self.assertEqual(package.sscc[:8], "08412345")
        self.assertEqual(package.sscc[8:17], "000000001")
        self.assertEqual(len(package.sscc), 18)
        self.assertTrue(check_barcode_encoding(package.sscc, "sscc"))

    def test_company_b_sscc(self):
        package = self.Package.with_company(self.company_b).create({"name": "PALLET-B"})

        self.assertEqual(package.sscc[:10], "0841234567")
        self.assertEqual(package.sscc[10:17], "0000001")
        self.assertEqual(len(package.sscc), 18)
        self.assertTrue(check_barcode_encoding(package.sscc, "sscc"))

    def test_missing_prefix_warns_user(self):
        company = self.env["res.company"].create({"name": "Sin prefijo"})

        with self.assertRaisesRegex(UserError, "Configure el prefijo GS1"):
            self.Package.with_company(company).create({"name": "PALLET-NO-PREFIX"})

    def test_sscc_is_globally_unique(self):
        package_a, package_b = self.Package.with_company(self.company_a).create(
            [{"name": "PALLET-1"}, {"name": "PALLET-2"}]
        )

        with self.assertRaises(IntegrityError), self.cr.savepoint():
            package_b.sscc = package_a.sscc
