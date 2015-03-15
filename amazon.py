from osv import osv, fields

class amazon_instance(osv.osv):
    _inherit = 'amazon.instance'

    def create_orders(self, cr, uid, instance_obj, shop_id, results):
        return super(amazon_instance, self).create_orders(cr, uid, instance_obj, shop_id, results, defaults={
            "payment_channel": "amazon",
            "input_channel": "amazon"
        })

amazon_instance()