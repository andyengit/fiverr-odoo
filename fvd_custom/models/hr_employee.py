from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    marital = fields.Selection(
        selection_add=[
            ("married", "CASADX"),
            ("divorced", "DIVORCIADX"),
            ("cohabitant", "PAREJA DE HECHO"),
            ("single", "SOLTERX"),
            ("widower", "VIUDX"),
            ("separated", "SEPARADX"),
        ],
        groups="hr.group_hr_user",
        default="single",
        tracking=True,
    )

    employee_type = fields.Selection(
        [
            ("employee", "Employee"),
            ("student", "Student"),
            ("trainee", "Trainee"),
            ("contractor", "Contractor"),
            ("freelance", "Freelancer"),
            ("indf_time_comp", "Indefinido a tiempo completo"),
            ("indf_time_partial", "Indefinido a tiempo parcial"),
            ("indf_disc", "Indefinido de persona con discapacidad"),
            ("conver", "Conversión de contrato temporal en contrato indefinido"),
            ("indf_fix", "Conversión de contrato temporal en contrato indefinido"),
            ("temp_sus", "Temporal por sustitución o relevo"),
            ("temp_cir", "Temporal por circunstancias de la producción"),
            ("form_apr", "Formación y aprendizaje"),
            ("trial", "Prácticas"),
        ],
        string="Tipo de contrato",
        default="employee",
        required=True,
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.",
    )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'No Binario')
    ], groups="hr.group_hr_user", tracking=True)

    medical_examination = fields.Selection(
        string="Reconocimiento médico", selection=[("yes", "Si"), ("no", "No")], default="no"
    )
    file_medical_examination = fields.Binary()

    prevention_of_occupational_hazards = fields.Boolean("Prevenciòn de riesgos laborales")
    confidentiality_contract = fields.Boolean("Contrato de confidencialidad")
    lopd_obligations = fields.Boolean("Obligaciones LOPD")
    delivery_of_protective_equipment = fields.Boolean("Entrega equipos de protección")
    training_record = fields.Boolean("Anexo 1: registro de formación")
    mandatory_training = fields.Boolean("Formación obligatoria")
    complementary_manuals = fields.Boolean("Manuales complementarios")

    is_clause_annexed_to_the_contract_PD = fields.Boolean("Cláusula anexa al contrato PD")
    clause_annexed_to_the_contract_PD = fields.Binary("Cláusula anexa al contrato PD")

    is_confidentiality_commitment = fields.Boolean("Compromiso de confidencialidad")
    confidentiality_commitment = fields.Binary("Compromiso de confidencialidad")

    is_appointments_and_authorizations_PD = fields.Boolean("Nombramientos y autorizaciones PD")
    appointments_and_authorizations_PD = fields.Binary("Nombramientos y autorizaciones PD")

    is_receipt_of_training_documentation = fields.Boolean("Recepción documentación formativa")
    receipt_of_training_documentation = fields.Binary("Recepción documentación formativa")
