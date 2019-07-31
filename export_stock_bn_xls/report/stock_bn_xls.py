# -- coding: utf-8 --
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
import datetime
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx



class StockBNReportXls(ReportXlsx):


	def get_category(self,data):
		if data.get('form',False) and data['form'].get('category', False):
			categ_id	= []
			obj 		= self.env['product.category'].search([('id', 'in', data['form']['category'])])
			for j in obj:
				if len([x.id for x in self.env['product.product'].search([('categ_id', '=', j.id)])]) >= 1:
					categ_id.append(j)
			return categ_id

	def get_company_id(self,data):
		if data.get('form',False) and data['form'].get('company_id', False):
			company_id	= []
			obj 		= self.env['res.company'].search([('id', '=', data['form']['company_id'])])
			for j in obj:
				company_id.append(j)
			return company_id

	def get_product(self, each, company_id):
		product_param	= []
		kode 			= []
		product_data 	= self.env['product.product'].search([('categ_id', '=', each),('company_id','=',company_id)])
		for product in product_data:
			product_param.append(product)
		return product_param

	def generate_xlsx_report(self,workbook,data,lines):
		get_category 	= self.get_category(data)
		get_company_id = self.get_company_id(data)
		quant_obj 		= self.env['stock.quant']
		sheet = workbook.add_worksheet('Stock Info')
		format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
		format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
		format21 = workbook.add_format({'font_size': 9, 'align': 'left', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': False})
		format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
		format99 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
		font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10})
		red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'red'})

		format_company = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'blue'})

		format_cikupa = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'gray'})

		format_alsut = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'purple'})

		format_non_ppn = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'white'})

		format_grand_total = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10,
		                                'bg_color': 'pink'})


		justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
		format3.set_align('center')
		font_size_8.set_align('center')
		justify.set_align('justify')
		format1.set_align('center')
		red_mark.set_align('center')

		date_start = ''
		date_end = ''

		sheet.write(1,0,'Stock Batch Number',format_company)


		header_row  = 6
		header_column = 0

		line_row = 7
		line_column = 0

		sheet.write(header_row,header_column,'Product Code.',format_cikupa)
		sheet.write(header_row,header_column+1,'Name.',format_cikupa)
		sheet.write(header_row,header_column+2,'Warehouse.',format_cikupa)
		sheet.write(header_row,header_column+3,'Batch Number.',format_cikupa)
		sheet.write(header_row,header_column+4,'Total.',format_cikupa)

		for comp in get_company_id:
			for each in get_category:
				number_seq	= 0
				get_company_id = self.get_company_id(data)
				line_row 	+= 1 #12891
				sheet.write(line_row,line_column,each.name,format99)
				if comp.id != 3:
					for product in self.get_product(each.id,comp.id):
						number_seq 	+= 1
						lot_list_als = self.env['stock.production.lot'].search([('product_id','=',product.id)])
						for lot in lot_list_als:
							total_lot_m2 = 0
							total_lot_lbr = 0
							location = ''
							quant_data_als = self.env['stock.quant'].search([('product_id','=',product.id),('location_id','=',15),('lot_id','=',lot.id)],order='location_id desc')
							for datax in quant_data_als:
								total_lot_m2 += datax.qty
								location = datax.location_id.location_id.name
							total_lot_lbr_als = total_lot_m2 / lot.product_id.uom2_rate
							if total_lot_m2 != 0:
								line_row += 1
								sheet.write(line_row,line_column,lot.product_id.default_code,format21)
								sheet.write(line_row,line_column+1,lot.product_id.color,format21)
								sheet.write(line_row,line_column+2,location,format21)
								sheet.write(line_row,line_column+3,lot.name,format21)
								sheet.write(line_row,line_column+4,round(total_lot_lbr_als,2),format21)
								#line_row += 1
						lot_list_ckp = self.env['stock.production.lot'].search([('product_id','=',product.id)])
						for lot_ckp in lot_list_ckp:
							total_lot_m2_ckp = 0
							total_lot_lbr_ckp = 0
							location_ckp = ''
							quant_data_ckp = self.env['stock.quant'].search([('product_id','=',product.id),('location_id','=',29),('lot_id','=',lot_ckp.id)],order='location_id desc')
							for datax_ckp in quant_data_ckp:
								total_lot_m2_ckp += datax_ckp.qty
								location_ckp = datax_ckp.location_id.location_id.name
							total_lot_lbr_ckp = total_lot_m2_ckp / lot.product_id.uom2_rate
							if total_lot_m2_ckp != 0:
								line_row += 1
								sheet.write(line_row,line_column,lot_ckp.product_id.default_code,format21)
								sheet.write(line_row,line_column+1,lot_ckp.product_id.color,format21)
								sheet.write(line_row,line_column+2,location_ckp,format21)
								sheet.write(line_row,line_column+3,lot_ckp.name,format21)
								sheet.write(line_row,line_column+4,round(total_lot_lbr_ckp,2),format21)

				else:
					for product in self.get_product(each.id,comp.id):
						number_seq 	+= 1
						lot_list = self.env['stock.production.lot'].search([('product_id','=',product.id)])
						for lot in lot_list:
							total_lot_m2 = 0
							total_lot_lbr = 0
							location = ''
							quant_data = self.env['stock.quant'].search([('product_id','=',product.id),('location_id','in',(22,35)),('lot_id','=',lot.id)],order='location_id desc')
							for datax in quant_data:
								total_lot_m2 += datax.qty
								location = datax.location_id.location_id.name
							total_lot_lbr = total_lot_m2 / lot.product_id.uom2_rate
							if total_lot_m2 != 0:
								line_row += 1
								sheet.write(line_row,line_column,lot.product_id.default_code,format21)
								sheet.write(line_row,line_column+1,lot.product_id.color,format21)
								sheet.write(line_row,line_column+2,location,format21)
								sheet.write(line_row,line_column+3,lot.name,format21)
								sheet.write(line_row,line_column+4,round(total_lot_lbr,2),format21)




StockBNReportXls('report.export_stock_bn_xls.stock_bn_report_xls.xlsx', 'product.product')