"""
Reads data from a stats collector and exposes it via HTTP
"""
import simplejson
import sqlite3
import sys
import threading
import urlparse
import SocketServer
import BaseHTTPServer
from pkg_resources import resource_filename

cols = [
    'model_id', 'model_make_id', 'model_name', 'model_trim',
    'model_year', 'model_body_style', 'model_engine_position',
    'model_engine_cc', 'model_engine_num_cyl', 'model_engine_type',
    'mode_engine_valves_per_cyl', 'model_engine_power_ps',
    'model_engine_power_rpm', 'model_engine_torque_nm',
    'model_engine_torque_rpm', 'model_engine_bore_mm',
    'model_engine_stroke_mm', 'model_engine_compression',
    'model_engine_fuel', 'model_top_speed_kph', 'model_0_to_100_kph',
    'model_drive', 'model_transmission_type', 'model_seats', 'model_doors',
    'model_weight_kg', 'model_length_mm', 'model_width_mm', 'model_height_mm',
    'model_wheelbase', 'model_lkm_hwy', 'model_lkm_mixed', 'model_lkm_city',
    'model_fuel_cap_l', 'model_sold_in_us', 'model_co2', 'model_make_display']


def carquery(args, conn=None):
    if not conn:
        conn = sqlite3.connect('cars.db')

    query = []
    if "model" in args:
        query.append('model_name LIKE "%%%s%%"' % args['model'])
    if "trim" in args:
        query.append('model_trim LIKE "%%%s%%"' % args['trim'])
    if "make" in args:
        query.append('model_make_display LIKE "%%%s%%"' % args['make'])
    if "year" in args:
        query.append('model_year LIKE "%%%s%%"' % args['year'])

    try:
        c = conn.cursor()
        result = c.execute("SELECT * from cars where %s limit 1000 COLLATE NOCASE" % ' AND '.join(
                query))
    except:
        return []

    output = [cols]
    output.extend(result.fetchall())
    return output


class CarQueryHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect('cars.db')
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        urldata = urlparse.urlparse(self.path)
        array_args = urlparse.parse_qs(urldata.query)
        args = dict([(k, v[0]) for k, v in array_args.items()])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(simplejson.dumps(carquery(args, self.conn)))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def app(environ, start_response):
    import time
    start = time.time()
    qs = environ['QUERY_STRING']
    array_args = urlparse.parse_qs(qs)
    args = dict([(k, v[0]) for k, v in array_args.items()])
    data = simplejson.dumps(carquery(args))
    start_response("200 OK", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(data)))
            ])
    print "Took: %s, %s bytes" % ((time.time() - start), len(data))
    return [data]

#if __name__ == '__main__':
    #httpd = ThreadedTCPServer(('', 9001), CarQueryHandler)
    #httpd.timeout = 1
    #httpd.serve_forever(poll_interval=0.1)
