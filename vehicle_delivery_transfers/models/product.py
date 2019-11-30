
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_vehicle = fields.Boolean('Is a Vehicle', help='Indicates whether the product is a Vehicle.')
