# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp

class CarSpecs(models.Model):
    _name = 'car.specs'
    _description = 'Car Specs'


    name_ref = fields.Char('Specs Reference', readonly=True , default=lambda x: str('New')) #default=default_randint_value
    name = fields.Char('Car Model', required=True)
    model_year = fields.Char('Model Year')
    engine_capacity = fields.Float('Engine Capacity (liters)')
    cylinders = fields.Selection([('four', '4 Cylinders'), ('six', '6 Cylinders'), ('eight', '8 Cylinders')], default='four', string="Cylinders")
    drive_type = fields.Selection([('fwd', 'FWD - Front Wheel Drive'), ('awd', 'AWD - All Wheel Drive'), ('rwd', 'RWD - Rear Wheel Drive'), ('4wd', '4WD - 4 Wheel Drive')], default='fwd', string="Drive Type")
    fuel_capacity = fields.Float('Fuel Tank Capacity (liters)')
    fuel_economy = fields.Float('Fuel Economy (L/100 Km)')
    fuel_type = fields.Selection([('petrol', 'Petrol'), ('diesel', 'Diesel')], default='petrol', string="Fuel Type")
    horsepower = fields.Float('Horsepower (bhp)')
    torque = fields.Float('Torque (Nm)')
    transmission = fields.Selection([('automatic', 'Automatic'), ('Manual', 'Manual')], default='automatic', string="Transmission")
    top_speed = fields.Float('Top Speed (Km/h)')
    seating_cpacity = fields.Char(string="Seating Capacity")

    acceleration = fields.Float('Acceleration 0-100 Km/h (sec)')
    options_lines = fields.One2many('car.specs.options', 'car_specs', string="Options", translate=True)
    public_price = fields.Monetary('Public Price')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)

    image = fields.Binary("Car Image", attachment=True)


    @api.model
    def create(self, vals):
        if vals.get('name_ref', _('New')) == _('New'):
            vals['name_ref'] = self.env['ir.sequence'].next_by_code('car.specs') or _('New')                
            result = super(CarSpecs, self).create(vals)
            return result

    @api.multi
    def action_view_car_specs(self):
        action = self.env.ref('product.product_normal_action_sell').read()[0]
        return {
            'name': _('Product Variants'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('car_specs', '=', self.id)],
        }





class CarSpecsOptions(models.Model):
    _name = 'car.specs.options'
    _description = 'Car Specs'

    options = fields.Char('Options', required=True, translate=True)
    car_specs = fields.Many2one('car.specs', string='Car Specs')



class CarCatalogue(models.Model):
    _name = 'car.specs.catalogue'
    _description = 'Cars Catalogue'

    name = fields.Char('Catalogue Name', required=True)
    car_specs = fields.Many2many('car.specs', 'car_specs_cat', string='Car Specs')


    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.user.company_id)



class ProductProduct(models.Model):
    _inherit = 'product.product'

    car_specs = fields.Many2one('car.specs', string='Car Specs')





class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    def get_sale_order_line_multiline_description_sale(self, product):
        """ Compute a default multiline description for this sales order line.
        This method exists so it can be overridden in other modules to change how the default name is computed.
        In general only the product is used to compute the name, and this method would not be necessary (we could directly override the method in product).
        BUT in event_sale we need to know specifically the sales order line as well as the product to generate the name:
            the product is not sufficient because we also need to know the event_id and the event_ticket_id (both which belong to the sale order line).
        """
        return product.get_product_multiline_description_sale() + self._get_sale_order_line_multiline_description_variants() + self._get_description()


    def _get_description(self):
        specs_id = self.product_id.car_specs.id
        car_specs = self.env['car.specs'].search([('id', '=', specs_id)])
        if car_specs:
            data = "\n" + 'Car Model : ' + str(car_specs.name) + "\n" + 'Model Year : ' + str(car_specs.model_year) + "\n" + 'Public Price : ' + str(car_specs.public_price)+ "\n" + 'Transmission : ' + str(car_specs.transmission)+ "\n" + 'Engine Capacity (liters) : ' + str(car_specs.engine_capacity)+ "\n" + 'Cylinders : ' + str(car_specs.cylinders)+ "\n" + 'Fuel Type : ' + str(car_specs.fuel_type)+ "\n" + 'Fuel Tank Capacity (liters) : ' + str(car_specs.fuel_capacity)+ "\n" + 'Fuel Economy (L/100 Km) : ' + str(car_specs.fuel_economy)+ "\n" + 'Drive Type : ' + str(car_specs.drive_type)+ "\n" + 'Horsepower (bhp) : ' + str(car_specs.horsepower)+ "\n" + 'Torque (Nm) : ' + str(car_specs.torque)+ "\n" + 'Top Speed (Km/h) : ' + str(car_specs.top_speed)+ "\n" + 'Acceleration 0-100 Km/h (sec) : ' + str(car_specs.acceleration)+ "\n" + 'Seating Capacity : ' + str(car_specs.seating_cpacity)
            return data
        else :
            data = ''
            return data
