{
    'name': 'Freight Management',
    'version': '17.0.1.0.1',
    'category': 'Sales',
    'summary': 'Manage freight orders, approvals, and reporting',
    'author': 'Vikash Tiwari',
    'maintainer': 'Vikash tiwari',
    'depends': ['base', 'sale_management','base_excel_report_model'],
    'data': [
        'security/freight_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/freight_wizard_report_views.xml',
        'report/freight_report_templates.xml',
        'views/freight_approval.xml',
        'views/freight_audit_logg.xml',
        'views/freight_menu.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
