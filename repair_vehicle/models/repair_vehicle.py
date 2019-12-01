from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class RepairVehicle(models.Model):
    _name = 'repair.vehicle'
    _description = 'Vehicle To Repair'


    name = fields.Char('Name',copy=False,track_visibility='always',readonly=True)

    product_id = fields.Many2one('product.product', 'Product', required=True)

    desc = fields.Char('Description')


    motor = fields.Many2one(
        'vehicle.motor', 'Motor', ondelete='cascade')

    color = fields.Many2one(
        'vehicle.color', 'Color', ondelete='cascade')

    quantity = fields.Integer("Quantity")

    lot_serial_number = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id','=',product_id)]")

    delivery_ref = fields.Char(string='Delivery Ref') 

    plate_num = fields.Char(string='Plate Number') 
    vehicle_model = fields.Char(string='Vehicle Model')
    vehicle_make = fields.Char(string='Vehicle Make')
    production_year = fields.Char(string='Production Year')
    vehicle_mileage = fields.Char(string='Vehicle Mileage')
    note = fields.Text(string='Note')




class VehicleDelivery(models.Model):
    _inherit = 'vehicle.delivery.transfer'


    @api.multi
    def _prepare_lines_vehicles(self, xline):
        self.ensure_one()
        return {
            'name': xline.lot_serial_number.name,
            'product_id': xline.product_id.id,
            'desc': xline.desc,
            'motor': xline.motor.id,
            'color': xline.color.id,
            'quantity': xline.quantity,
            'lot_serial_number': xline.lot_serial_number.id,
            'delivery_ref': xline.delivery_ref,
            'plate_num': xline.plate_num,
            'vehicle_model': xline.vehicle_model,
            'vehicle_make': xline.vehicle_make,
            'production_year': xline.production_year,
            'vehicle_mileage': xline.vehicle_mileage,
            'note': xline.note,
        }


    @api.multi
    def button_validate(self):
        for xline in self.delivery_lines:
            vals = self._prepare_lines_vehicles(xline)
            repair = self.env['repair.vehicle']
            repair.create(vals)
        return self.write({'state': 'confirm'})


class Repair(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one(
        'repair.vehicle', string='Vehicle to Repair',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    lot_name = fields.Char(related='vehicle_id.name')

    
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('name','=', lot_name)]",
        help="Products repaired are all belonging to this lot", oldname="prodlot_id", required=False)

    @api.onchange('vehicle_id')
    def _compute_product_id(self):
        self.product_id = self.vehicle_id.product_id.id

class RepairLine(models.Model):
    _inherit = 'repair.line'
    
    product_id = fields.Many2one('product.product', 'Product', required=True,domain="[('is_vehicle','=',False)]")
