import datetime
import logging

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.tools.misc import clean_context, OrderedSet
from operator import itemgetter
from itertools import groupby
from collections import defaultdict, Counter

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_volume = fields.Float(string="Volume", store=False, compute='_compute_total_volume')
    volume_uom_name = fields.Char(store=False, compute='_compute_volume_uom')

    def _compute_total_volume(self):
        for record in self:
            v = 0
            for line in record.order_line:
                v += line.volume * line.product_uom_qty
            record.write({
                'total_volume': v,
            })
    
    def _compute_volume_uom(self):
        for record in self:
            res = ""
            if len(record.order_line) > 0:
                l = record.order_line[0]
                if l.product_id and l.product_id.volume_uom_name:
                    res = l.product_id.volume_uom_name
            record.write({
                'volume_uom_name': res,
            })

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    volume = fields.Float(string="Item Volume", store=False, related='product_id.volume')
    

