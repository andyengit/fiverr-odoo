from odoo import models, fields


class IncidenceData(models.Model):
    _name = "fvd_custom.incidence_data"

    employee_id = fields.Many2one("hr.employee", "Trabajadxr que recoge la incidencia")
    employee_type = fields.Selection(
        related="employee_id.employee_type", string="Cargo del empleado", readonly=False
    )

    incidence_employee_id = fields.Many2one("hr.employee", "Trabajadxr")
    incidence_employee_type = fields.Selection(
        related="employee_id.employee_type", string="Puesto que desempeña", readonly=False
    )

    user = fields.Many2one("res.partner", "Usuarix")
    volunteer = fields.Many2one("res.partner", "Voluntarix")
    tbc = fields.Many2one("res.partner", "TBC")

    people_in_advocacy_ids = fields.One2many(
        "fvd_custom.incidence_line_data",
        "incidence_id",
        string="Persona/as involucradas en la incidencia",
    )

    description = fields.Text(string="Descripción de lo ocurrido")

    incidence_area = fields.Selection(
        [
            ("care_area", "Área de cuidado"),
            ("training_area", "Área de formación"),
            ("health_area", "Área de salud"),
            ("socialitation_area", "Área de socialización"),
            ("housing_area", "Área de vivienda"),
            ("socioeconomic_area", "Área socioeconómica"),
            ("labor_insertion", "Inserción laboral(TBC)"),
            ("volunteering", "Voluntariado"),
        ],
    )
    document_date = fields.Date(string="Fdo")
