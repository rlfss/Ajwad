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

class SotckSerial(models.Model):
	_name = 'sotck.serial'
class StockSerial(models.Model):
	_name = 'stock.serial'
	_description = 'Stock Serial'

	name = fields.Char('Serial Number')
	move_id = fields.Many2one('stock.move','Move')

	@api.model
	def create(self,vals):
		move = self.env['stock.move'].browse(self._context.get('move_id'))
		if move:
			if move.product_uom_qty > move.quantity_done:
				move.move_line_ids = [(0,0,{'lot_name':vals.get('name'),
					'product_id':move.product_id.id,
					'product_uom_id':move.product_uom.id,
					'location_id':move.location_id.id,
					'location_dest_id':move.location_dest_id,
					'qty_done':1})]
				vals['move_id'] = move.id
		return super(StockSerial,self).create(vals)