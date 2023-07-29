from odoo import models, fields

class IncidenceLineData(models.Model):
    _name = "fvd_custom.incidence_line_data"

    incidence_id = fields.Many2one("fvd_custom.incidence_data", string="Incidencia")
    employee_id = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Selection(related='employee_id.employee_type', string="Papel dentro de la fundación")