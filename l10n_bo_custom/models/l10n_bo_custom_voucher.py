from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class DisbursementVoucher(models.Model):
    _name = "l10n_bo_custom.voucher"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", default=lambda x: x.env.company.id)
    name = fields.Char(string="Nº Comprobante", required=True)
    date = fields.Date(string="Fecha", required=True, default=fields.Date.today())
    description = fields.Text(string="Descripcion")
    voucher_line_ids = fields.One2many("l10n_bo_custom.voucher.line", "voucher_id")
    pagado_a = fields.Char("Pagado A")
    lugar = fields.Char("Lugar")
    tc = fields.Float("T.C", compute="_compute_tc")
    tc_inverse = fields.Float("T.C", compute="_compute_tc")
    account_move_line_ids = fields.Many2many(
        "account.move.line", string="Apuntes Contable", compute="_compute_account_move_line_ids"
    )
    currency_id = fields.Many2one("res.currency", default=lambda x: x.env.ref("base.BOB").id)

    @api.depends("voucher_line_ids")
    def _compute_account_move_line_ids(self):
        for record in self:
            if not record.voucher_line_ids:
                record.account_move_line_ids = False
            if not record.voucher_line_ids.name.line_ids:
                record.account_move_line_ids = False

            for line in record.voucher_line_ids.name.line_ids:
                record.account_move_line_ids += line

    @api.depends("tc", "date")
    def _compute_tc(self):
        for record in self:
            values = record.env["res.currency.rate"].compute_rate(
                record.env.ref("base.USD").id, record.date
            )
            record.tc = values.get("rate", 0)
            record.tc_inverse = values.get("inverse_rate", 0)

    def get_amount_text(self, text):
        entero = int(text)

        decimal = int(round((text - entero) * 100))
        if decimal == 0:
            return numero_to_letras(entero)
        return f"{numero_to_letras(entero)} CON {numero_to_letras(decimal)} "


class DisbursementVoucherLine(models.Model):
    _name = "l10n_bo_custom.voucher.line"

    name = fields.Many2one(
        "account.move",
        string="Asiento Contable / Factura",
        domain="['|',('date','=',date),('invoice_date','=',date)]",
        required=True,
    )

    date = fields.Date(related="voucher_id.date")
    voucher_id = fields.Many2one("l10n_bo_custom.voucher")
    is_invoice = fields.Boolean("Es factura?")
    move_type = fields.Char("Tipo de Asiento", default="entry")

    @api.onchange("is_invoice")
    def _compute_move_type(self):
        self.move_type = "in_invoice" if self.is_invoice else "entry"


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    def compute_rate(self, currency_id, date):
        rates = self.env["res.currency.rate"].search(
            [
                ("currency_id", "=", currency_id),
                ("company_id", "=", self.env.company.id),
                ("name", "<=", date),
            ]
        )
        if not rates:
            return {}

        rate = rates.filtered(lambda r: r.name == date) or rates[0]
        return {"rate": rate.inverse_company_rate, "inverse_rate": rate.company_rate}


def numero_to_letras(numero):
    indicador = [
        ("", ""),
        ("MIL", "MIL"),
        ("MILLON", "MILLONES"),
        ("MIL", "MIL"),
        ("BILLON", "BILLONES"),
    ]

    entero = int(numero)

    decimal = int(round((numero - entero) * 100))

    # print 'decimal : ',decimal

    contador = 0

    numero_letras = ""

    while entero > 0:
        a = entero % 1000

        if contador == 0:
            en_letras = convierte_cifra(a, 1).strip()

        else:
            en_letras = convierte_cifra(a, 0).strip()

        if a == 0:
            numero_letras = en_letras + " " + numero_letras

        elif a == 1:
            if contador in (1, 3):
                numero_letras = indicador[contador][0] + " " + numero_letras

            else:
                numero_letras = en_letras + " " + indicador[contador][0] + " " + numero_letras

        else:
            numero_letras = en_letras + " " + indicador[contador][1] + " " + numero_letras

        numero_letras = numero_letras.strip()

        contador = contador + 1

        entero = int(entero / 1000)

    numero_letras = numero_letras 

    return numero_letras


def convierte_cifra(numero, sw):
    lista_centana = [
        "",
        ("CIEN", "CIENTO"),
        "DOSCIENTOS",
        "TRESCIENTOS",
        "CUATROCIENTOS",
        "QUINIENTOS",
        "SEISCIENTOS",
        "SETECIENTOS",
        "OCHOCIENTOS",
        "NOVECIENTOS",
    ]

    lista_decena = [
        "",
        (
            "DIEZ",
            "ONCE",
            "DOCE",
            "TRECE",
            "CATORCE",
            "QUINCE",
            "DIECISEIS",
            "DIECISIETE",
            "DIECIOCHO",
            "DIECINUEVE",
        ),
        ("VEINTE", "VEINTI"),
        ("TREINTA", "TREINTA Y "),
        ("CUARENTA", "CUARENTA Y "),
        ("CINCUENTA", "CINCUENTA Y "),
        ("SESENTA", "SESENTA Y "),
        ("SETENTA", "SETENTA Y "),
        ("OCHENTA", "OCHENTA Y "),
        ("NOVENTA", "NOVENTA Y "),
    ]

    lista_unidad = [
        "",
        ("UN", "UNO"),
        "DOS",
        "TRES",
        "CUATRO",
        "CINCO",
        "SEIS",
        "SIETE",
        "OCHO",
        "NUEVE",
    ]

    centena = int(numero / 100)

    decena = int((numero - (centena * 100)) / 10)

    unidad = int(numero - (centena * 100 + decena * 10))

    # print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

    texto_centena = ""

    texto_decena = ""

    texto_unidad = ""

    # Validad las centenas

    texto_centena = lista_centana[centena]

    if centena == 1:
        if (decena + unidad) != 0:
            texto_centena = texto_centena[1]

        else:
            texto_centena = texto_centena[0]

    # Valida las decenas

    texto_decena = lista_decena[decena]

    if decena == 1:
        texto_decena = texto_decena[unidad]

    elif decena > 1:
        if unidad != 0:
            texto_decena = texto_decena[1]

        else:
            texto_decena = texto_decena[0]

    if decena != 1:
        texto_unidad = lista_unidad[unidad]
    if unidad == 1:
        texto_unidad = texto_unidad[sw]

    return "%s %s %s" % (texto_centena, texto_decena, texto_unidad)
