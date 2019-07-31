# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Jesni Banu(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import except_orm, Warning, RedirectWarning

class StockBNReport(models.TransientModel):
	_name = "wizard.stock.bn.report"
	_description = "Stock Batch Number Report"


	company_id		= fields.Many2one('res.company','Company', default=1)
	category        = fields.Many2many('product.category')



	@api.multi
	def export_xls(self):
		context = self._context
		datas = {'ids': context.get('active_ids', [])}
		datas['model'] = 'product.product'
		datas['form'] = self.read()[0]
		for field in datas['form'].keys():
			if isinstance(datas['form'][field], tuple):
				datas['form'][field] = datas['form'][field][0]
		if context.get('xls_export'):
			print ">>>>>>>>>"
			return {'type': 'ir.actions.report.xml',
					'report_name': 'export_stock_bn_xls.stock_bn_report_xls.xlsx',
					'datas': datas,
					'name': 'Stock BN Report'
					}
