from osv import osv, fields
import time
import datetime
import inspect
import xmlrpclib
import netsvc
import os
import logging
import urllib2
import base64
from tools.translate import _
import httplib, ConfigParser, urlparse
from xml.dom.minidom import parse, parseString
from lxml import etree
from xml.etree.ElementTree import ElementTree
import amazonerp_osv as mws
from mako.lookup import TemplateLookup

this_dir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
templates = TemplateLookup(directories=[os.path.join(this_dir, 'ups')], default_filters=['unicode', 'x'])

class amazon_instance(osv.osv):
    _inherit = 'amazon.instance'

    def create_orders(self, cr, uid, instance_obj, shop_id, results):
        res = super(amazon_instance, self).create_orders(cr, uid, instance_obj, shop_id, results)
        if res:
            amazon_order_ids = [result['AmazonOrderId']
                                for result in results
                                if result.get('OrderStatus') == 'Unshipped' and 'AmazonOrderId' in result]

            sale_order_pool = self.pool.get('sale.order')
            sale_order_pool.write(cr, uid, sale_order_pool.search(
                cr, uid, ['amazon_order_id', 'in', amazon_order_ids]), {
                'input_channel': 'amazon', 'payment_channel': 'amazon'
            })

        return res

amazon_instance()