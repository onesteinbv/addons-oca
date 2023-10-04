
{
    'name': 'Move Line Attachment Preview',
    'summary': 'Preview PDF on journal item list',
    'version': '16.0.1.0.0',
    "author": "Onestein,Odoo Community Association (OCA)",
    'category': 'Accounting/Accounting',
    "development_status": "Alpha",
    'depends': ['account', 'attachment_preview'],
    'data': [
        'views/account_move_line.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_move_line_attachment_preview/static/src/**/*',
        ],
    }
}
