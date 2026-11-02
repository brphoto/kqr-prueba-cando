from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.barcode import get_barcode_check_digit


class StockPackage(models.Model):
    _inherit = "stock.package"

    sscc = fields.Char(
        string="SSCC",
        readonly=True,
        copy=False,
        index="btree_not_null",
    )

    _sscc_unique = models.Constraint(
        "UNIQUE(sscc)",
        "El SSCC debe ser único.",
    )

    @api.model
    def _sscc_check_digit(self, payload):
        """Return the GS1 mod-10 check digit for a 17-digit payload."""
        if len(payload) != 17 or not payload.isascii() or not payload.isdigit():
            raise ValidationError(_("La base del SSCC debe contener exactamente 17 dígitos."))
        return str(get_barcode_check_digit(f"{payload}0"))

    @api.model
    def _next_sscc(self, company):
        prefix = company.prefijo_gs1 or ""
        if not prefix:
            raise UserError(
                _(
                    "Configure el prefijo GS1 de la compañía %(company)s antes de crear paquetes.",
                    company=company.display_name,
                )
            )
        if not prefix.isascii() or not prefix.isdigit() or len(prefix) > 15:
            raise UserError(
                _("El prefijo GS1 de la compañía %(company)s no es válido.", company=company.display_name)
            )

        serial_length = 16 - len(prefix)
        serial_value = company._get_sscc_sequence().next_by_id()
        if not serial_value or not serial_value.isdigit():
            raise UserError(
                _("No se pudo obtener la siguiente referencia serial para %(company)s.", company=company.display_name)
            )
        if len(serial_value) > serial_length:
            raise UserError(
                _(
                    "La secuencia SSCC de %(company)s agotó los %(digits)s dígitos disponibles.",
                    company=company.display_name,
                    digits=serial_length,
                )
            )

        payload = f"0{prefix}{serial_value.zfill(serial_length)}"
        return f"{payload}{self._sscc_check_digit(payload)}"

    @api.model_create_multi
    def create(self, vals_list):
        company = self.env.company
        vals_list = [dict(vals, sscc=self._next_sscc(company)) for vals in vals_list]
        return super().create(vals_list)
