from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    n_autorizacion = fields.Char("Codigo de Autorización")
    codigo_control = fields.Char("Código de Control")
    n_factura = fields.Char("N° Factura")
    dui = fields.Char("DUI")
