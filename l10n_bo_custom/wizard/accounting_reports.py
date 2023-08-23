from dateutil.relativedelta import relativedelta
from datetime import datetime
from io import BytesIO
from odoo import models, fields
import xlsxwriter
from xlsxwriter import utility
import logging

_logger = logging.getLogger(__name__)
INIT_LINES = 1


class WizardAccountingInvoice(models.TransientModel):
    _name = "wizard.accounting.reports"
    _description = "Wizard para generar reportes de libro de compra y ventas"
    _check_company_auto = True

    def _default_date_from(self):
        current_day = fields.Date.today()
        return current_day

    def _default_date_to(self):
        current_day = self._default_date_from()
        final_day_month = relativedelta(months=1, days=-1)
        increment_date = current_day + final_day_month
        return increment_date

    def _default_company_id(self):
        company_id = self.env.company.id
        return company_id

    report = fields.Selection(
        [("purchase", "Libro de Compras"), ("sale", "Libro de Ventas")],
        required=True,
    )

    date_from = fields.Date(string="Date Start", required=True, default=_default_date_from)

    date_to = fields.Date(
        string="Date End",
        required=True,
        default=_default_date_to,
    )

    company_id = fields.Many2one("res.company", default=_default_company_id)

    def _fields_sale_book_line(self, move):
        return {
            "_id": move.id,
            "espec": "2",
            "document_date": self._format_date(move.invoice_date),
            "document_number": move.n_factura,
            "n_autorizacion": move.n_autorizacion,
            "vat": move.partner_id.vat,
            "complement": move.partner_id.complement or "",
            "partner_name": move.invoice_partner_display_name,
            "amount_total": move.amount_total,
            "amount_ice": 0,
            "amount_iehd": 0,
            "amount_ipi": 0,
            "amount_tasas": 0,
            "amount_not_iva": 0,
            "amount_export_and_others": 0,
            "amount_sale_rate_zero": 0,
            "subtotal": move.amount_untaxed,
            "des_bon_reb": 0,
            "import_gift_card": 0,
            "amount_base_fiscal_debit": move.amount_untaxed,
            "amount_fiscal_debit": move.amount_untaxed * 0.13,
            "code_num": move.codigo_control,
            "type_sale": 0,
            "state": "V",
        }

    def _fields_purchase_book_line(self, move):
        return {
            "_id": move.id,
            "espec": "1",
            "vat": move.partner_id.vat,
            "partner_name": move.invoice_partner_display_name,
            "n_autorizacion": move.n_autorizacion,
            "document_number": move.n_factura,
            "document_dui": move.dui,
            "document_date": self._format_date(move.invoice_date),
            "complement": move.partner_id.complement or "",
            "amount_total": move.amount_total,
            "amount_ice": 0,
            "amount_iehd": 0,
            "amount_ipi": 0,
            "amount_tasas": 0,
            "amount_not_iva": 0,
            "amount_export_and_others": 0,
            "amount_sale_rate_zero": 0,
            "subtotal": move.amount_untaxed,
            "des_bon_reb": 0,
            "import_gift_card": 0,
            "amount_base_fiscal_debit": move.amount_untaxed,
            "amount_fiscal_debit": move.amount_untaxed * 0.13,
            "code_num": move.codigo_control,
            "type_sale": 1,
            "state": "V",
        }

    def parse_sale_book_data(self):
        sale_book_lines = []
        moves = self.search_moves()

        for move in moves:
            sale_book_line = self._fields_sale_book_line(move)
            sale_book_lines.append(sale_book_line)
        return sale_book_lines

    def parse_purchase_book_data(self):
        purchase_book_lines = []
        moves = self.search_moves()

        for move in moves:
            purchase_book_line = self._fields_purchase_book_line(move)
            purchase_book_lines.append(purchase_book_line)

        return purchase_book_lines

    def sale_book_fields(self):
        return [
            {
                "name": "N°",
                "field": "index",
            },
            {
                "name": "Especificacion",
                "field": "espec",
            },
            {
                "name": "Fecha de la Factura",
                "field": "document_date",
                "size": 15,
            },
            {
                "name": "Nº Factura",
                "field": "document_number",
                "size": 20,
            },
            {
                "name": "Codigo de Autorización",
                "field": "n_autorizacion",
                "size": 20,
            },
            {"name": "NIT/CI CLIENTE", "field": "vat", "size": 15},
            {"name": "Complemento", "field": "complement", "size": 15},
            {
                "name": "Nombre o Razón Social",
                "field": "partner_name",
                "size": 25,
            },
            {
                "name": "Importe Total de la Ventas",
                "field": "amount_total",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe ICE",
                "field": "amount_ice",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe IEHD",
                "field": "amount_iehd",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe IPI",
                "field": "amount_ipi",
                "format": "number",
                "size": 15,
            },
            {
                "name": "TASAS",
                "field": "amount_tasas",
                "format": "number",
                "size": 15,
            },
            {
                "name": "OTROS NO SUJETOS AL IVA",
                "field": "amount_not_iva",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Exportaciones y Operaciones Exentas",
                "field": "amount_export_and_others",
                "format": "number",
                "size": 15,
            },
            {
                "name": "VENTAS GRAVADAS A TASA CERO",
                "field": "amount_sale_rate_zero",
                "format": "number",
                "size": 15,
            },
            {
                "name": "SUBTOTAL",
                "field": "subtotal",
                "format": "number",
                "size": 15,
            },
            {
                "name": "DESCUENTOS, BONIFICACIONES Y REBAJAS SUJETAS AL IVA",
                "field": "des_bon_reb",
                "format": "number",
                "size": 15,
            },
            {
                "name": "IMPORTE GIFT CARD",
                "field": "import_gift_card",
                "format": "number",
                "size": 15,
            },
            {
                "name": "IMPORTE BASE PARA DEBITO FISCAL",
                "field": "amount_base_fiscal_debit",
                "format": "number",
            },
            {
                "name": "DEBITO FISCAL",
                "field": "amount_fiscal_debit",
                "format": "number",
            },
            {"name": "Estado", "field": "state"},
            {"name": "Codigo de control", "field": "code_num"},
            {"name": "Tipo de venta", "field": "type_sale"},
        ]

    def purchase_book_fields(self):
        return [
            {
                "name": "N°",
                "field": "index",
            },
            {
                "name": "Especificacion",
                "field": "index",
            },
            {"name": "NIT PROVEEDOR", "field": "vat", "size": 15},
            {
                "name": "Nombre o Razón Social",
                "field": "partner_name",
                "size": 25,
            },
            {
                "name": "Codigo de Autorización",
                "field": "n_autorizacion",
                "size": 20,
            },
            {
                "name": "Nº Factura",
                "field": "document_number",
                "size": 20,
            },
            {
                "name": "Numero DUI/DIM",
                "field": "document_dui",
                "size": 20,
            },
            {
                "name": "Fecha de Factura/DUI/DIM",
                "field": "document_date",
                "size": 15,
            },
            {
                "name": "Importe Total compra",
                "field": "amount_total",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe ICE",
                "field": "amount_ice",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe IEHD",
                "field": "amount_iehd",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importe IPI",
                "field": "amount_iehd",
                "format": "number",
                "size": 15,
            },
            {
                "name": "TASAS",
                "field": "amount_tasas",
                "format": "number",
                "size": 15,
            },
            {
                "name": "OTROS NO SUJETOS A CREDITO FISCAL",
                "field": "amount_not_iva",
                "format": "number",
                "size": 15,
            },
            {
                "name": "Importes Exentos",
                "field": "amount_export_and_others",
                "format": "number",
                "size": 15,
            },
            {
                "name": "VENTAS GRAVADAS A TASA CERO",
                "field": "amount_sale_rate_zero",
                "format": "number",
                "size": 15,
            },
            {
                "name": "SUBTOTAL",
                "field": "subtotal",
                "format": "number",
                "size": 15,
            },
            {
                "name": "DESCUENTOS, BONIFICACIONES Y REBAJAS SUJETAS AL IVA",
                "field": "des_bon_reb",
                "format": "number",
                "size": 15,
            },
            {
                "name": "IMPORTE GIFT CARD",
                "field": "import_gift_card",
                "format": "percent",
                "size": 15,
            },
            {
                "name": "IMPORTE BASE PARA CREDITO FISCAL",
                "field": "amount_base_fiscal_debit",
                "format": "number",
            },
            {
                "name": "CREDITO FISCAL",
                "field": "amount_fiscal_debit",
                "format": "number",
            },
            {"name": "Tipo de compra", "field": "type_sale"},
            {"name": "Codigo de control", "field": "code_num"},
        ]

    def _get_domain(self, current_company_id=False):
        search_domain = []
        is_purchase = self.report == "purchase"

        field_date = "date" if is_purchase else "invoice_date"

        if current_company_id:
            search_domain += [("company_id", "=", current_company_id)]

        move_type = (
            ["out_invoice", "out_refund"]
            if not is_purchase
            else ["in_invoice", "in_refund", "in_debit"]
        )

        search_domain += [(field_date, ">=", self.date_from)]
        search_domain += [(field_date, "<=", self.date_to)]
        search_domain += [
            ("state", "not in", ["draft"]),
            ("move_type", "in", move_type),
        ]

        return search_domain

    def generate_report(self):
        is_sale = self.report == "sale"

        if is_sale:
            return self.download_sales_book()

        return self.download_purchases_book()

    def download_sales_book(self):
        self.ensure_one()
        url = "/web/download_sales_book"
        return {"type": "ir.actions.act_url", "url": url, "target": "self"}

    def download_purchases_book(self):
        self.ensure_one()
        url = "/web/download_purchase_book"
        return {"type": "ir.actions.act_url", "url": url, "target": "self"}

    def _format_date(self, date):
        _fn = datetime.strptime(str(date), "%Y-%m-%d")
        return _fn.strftime("%d/%m/%Y")

    def search_moves(self):
        order = "invoice_date asc"
        env = self.env
        move_model = env["account.move"]
        domain = self._get_domain()
        moves = move_model.search(domain, order=order)
        return moves

    def generate_sales_book(self):
        sale_book_lines = self.parse_sale_book_data()
        file = BytesIO()

        workbook = xlsxwriter.Workbook(file, {"in_memory": True, "nan_inf_to_errors": True})
        worksheet = workbook.add_worksheet()

        merge_format = workbook.add_format({"border": 1, "align": "center", "valign": "vcenter"})
        cell_formats = {
            "number": workbook.add_format({"num_format": "#,##0.00"}),
            "percent": workbook.add_format({"num_format": "0.00%"}),
        }

        name_columns = self.sale_book_fields()
        total_idx = 0

        for index, field in enumerate(name_columns):
            worksheet.set_column(index, index, len(field.get("name")) + 4)
            worksheet.write(0, index, field.get("name").upper(), merge_format)

            for index_line, line in enumerate(sale_book_lines):
                total_idx = (INIT_LINES + index_line) + 1

                if field["field"] == "index":
                    worksheet.write(INIT_LINES + index_line, index, index_line + 1)
                else:
                    cell_format = cell_formats.get(field.get("format"), workbook.add_format())
                    worksheet.write(
                        INIT_LINES + index_line, index, line.get(field["field"]), cell_format
                    )

            if field.get("format") == "number":
                col = utility.xl_col_to_name(index)
                worksheet.write_formula(
                    total_idx, index, f"=SUM({col}2:{col}{total_idx})", cell_formats.get("number")
                )

        workbook.close()
        return file.getvalue()

    def generate_purchases_book(self):
        purchase_book_lines = self.parse_purchase_book_data()
        file = BytesIO()

        workbook = xlsxwriter.Workbook(file, {"in_memory": True, "nan_inf_to_errors": True})
        worksheet = workbook.add_worksheet()

        merge_format = workbook.add_format({"border": 1, "align": "center", "valign": "vcenter"})
        cell_formats = {
            "number": workbook.add_format({"num_format": "#,##0.00"}),
            "percent": workbook.add_format({"num_format": "0.00%"}),
        }

        name_columns = self.purchase_book_fields()
        total_idx = 0

        for index, field in enumerate(name_columns):
            worksheet.set_column(index, index, len(field.get("name")) + 4)
            worksheet.write(0, index, field.get("name").upper(), merge_format)

            for index_line, line in enumerate(purchase_book_lines):
                total_idx = (INIT_LINES + index_line) + 1

                if field["field"] == "index":
                    worksheet.write(INIT_LINES + index_line, index, index_line + 1)
                else:
                    cell_format = cell_formats.get(field.get("format"), workbook.add_format())
                    worksheet.write(
                        INIT_LINES + index_line, index, line.get(field["field"]), cell_format
                    )

            if field.get("format") == "number":
                col = utility.xl_col_to_name(index)
                worksheet.write_formula(
                    total_idx, index, f"=SUM({col}2:{col}{total_idx})", cell_formats.get("number")
                )

        workbook.close()
        return file.getvalue()
