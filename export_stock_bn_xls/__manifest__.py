
{
    'name': 'Export Stock Batch Number ',
    'version': '10',
    'summary': "Report Stock Batch Number",
    'category': 'Project',
    'author': 'Dion Martin <dion.martin.h@gmail.com>',
    'company': '',
    'depends': [
                'base',
                'stock',
                'sale',
                'purchase',
                'sales_team',
                'report_xlsx',
                'project',
                ],
    'data': [
            'views/wizard_view.xml',
            ],
    #'images': ['static/description/banner.jpg'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
}
