# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
	_inherit = 'stock.move'

	def import_serials(self):
		if self.product_id.tracking != "serial":
			raise UserError("Please Reconfigure The Product To Be Tracked By Serial")
		return {
		'name':'Serial Numbers Import',
		'type':'ir.actions.act_window',
		'res_model':'stock.serial',
		'view_mode':'tree',
		'target':'new',
		'domain':[('move_id','=',self.id)],
		'context':{'move_id':self.id}
		}

class StockSerial(models.Model):
	_name = 'stock.serial'
	_description = 'Stock Serial'

	name = fields.Char('Serial Number')
	move_id = fields.Many2one('stock.move','Move')

	@api.model
	def create(self,vals):
		move = self.env['stock.move'].browse(self._context.get('move_id'))
		if move:
			for line in move.move_line_ids:
				if not line.lot_name:
					line.lot_name=vals.get('name')
					line.qty_done=1
					vals['lot_id'] = False
					vals['move_id'] = move.id
					return super(StockSerial,self).create(vals)
