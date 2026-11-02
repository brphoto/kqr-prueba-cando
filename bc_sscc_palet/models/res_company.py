from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    prefijo_gs1 = fields.Char(
        string="Prefijo GS1",
        help="Prefijo GS1 de empresa utilizado para generar los SSCC.",
    )

    @api.constrains("prefijo_gs1")
    def _check_prefijo_gs1(self):
        for company in self:
            prefix = company.prefijo_gs1 or ""
            if prefix and (not prefix.isascii() or not prefix.isdigit()):
                raise ValidationError(
                    _("El prefijo GS1 de la compañía debe contener únicamente dígitos.")
                )
            if len(prefix) > 15:
                raise ValidationError(
                    _("El prefijo GS1 debe dejar al menos un dígito para la referencia serial.")
                )

    def _get_sscc_sequence(self):
        """Return this company's SSCC sequence, creating it on first use."""
        self.ensure_one()
        sequence_model = self.env["ir.sequence"].sudo()
        sequence = sequence_model.search(
            [
                ("code", "=", "bc_sscc_palet.sscc"),
                ("company_id", "=", self.id),
            ],
            limit=1,
        )
        if not sequence:
            sequence = sequence_model.create(
                {
                    "name": _("SSCC - %(company)s", company=self.display_name),
                    "code": "bc_sscc_palet.sscc",
                    "padding": 1,
                    "number_increment": 1,
                    "company_id": self.id,
                }
            )
        return sequence
