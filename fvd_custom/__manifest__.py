{
    "name": "Fundacion Veintiseis de Diciembre - Custom",
    "version": "1.2",
    "category": "Human Resources/Employees",
    "description": """PERSONALIZACIONES PARA FVD""",
    "website": "andersonarmeya.com",
    "depends": ["base", "mail", "hr", "project","account"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_activity_type.xml",
        "data/res_partner_title.xml",
        "report/cesion_de_datos.xml",
        "report/suspencion_de_datos.xml",
        "report/cesion_imagen.xml",
        "report/compromiso.xml",
        "report/expediente.xml",
        "report/contrato.xml",
        "report/previas.xml",
        "views/hr_employee_views.xml",
        "views/res_partner_views.xml",
        "views/account_move_views.xml",
        "views/project_task_views.xml",
        "views/incidence_data.xml",
        "views/pai_views.xml",
        "views/social_report_views.xml",
        "views/dafo.xml",
        "views/menu.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            (
                "replace",
                "mail/static/src/models/activity_view.js",
                "fvd_custom/static/src/js/activity_view.js",
            )
        ]
    },
    "author": "Anderson Armeya (andyenfiverr)",
}
