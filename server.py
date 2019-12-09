#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:15:16 2019

@author: shreyarora
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import os
import json
import math

import ml


def convert_coordinate(coordinate):
        dec_part, int_part = math.modf(coordinate)
        dec_part = dec_part * 1000
        return int(dec_part)
    
def convert_time(time):
    converted_time = time.split(":")
    return (int(converted_time[0])*60 + int(converted_time[1]))

def convert_date(date):
    year, month, day = date.split("-")
    return(int(month),int(day))
    
class S(BaseHTTPRequestHandler):

    def do_GET(self):
        rootdir = os.getcwd() 
  
        try:
            print(rootdir + self.path)
            
            path = self.path.split("?",1)[0]
            if path == '/':
                self.path += 'index.html'   # default to index.html
                
            if path == '/result':
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin","*")
                self.send_header("Access-Control-Allow-Methods","*")
                self.send_header("Access-Control-Allow-Headers","*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                         
            elif self.path.endswith('.html'):
                f = open(rootdir + self.path)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))  
                f.close()  
            elif self.path.endswith('.js'):
                f = open(rootdir + self.path)
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))  
                f.close()
            elif self.path.endswith('.css'):
                f = open(rootdir + self.path)
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))  
                f.close()  
            else:
                self.send_error(404, 'file not supported')  
                
        except IOError:
            self.send_error(404, 'file not found')  
    
    def do_POST(self):
        rootdir = os.getcwd() 
  
        try:
            print(rootdir + self.path)
            
            path = self.path.split("?",1)[0]

            # handle 'addone' endpoint
            if path == '/result':
			
                # JSON string
                payloadString = self.rfile.read(int(self.headers['Content-Length']))
				
                # Python dictionary
                payload = json.loads(payloadString)
                              
                duration = int(payload['trip_seconds'])
                miles = int(payload['trip_miles'])
                pickup_latitude = float(payload['pickup_latitude'])
                pickup_lat = convert_coordinate(pickup_latitude)
                pickup_longitude = float(payload['pickup_longitude'])
                pickup_lon = convert_coordinate(pickup_longitude)
                dropoff_latitude = float(payload['dropoff_latitude'])
                dropoff_lat = convert_coordinate(dropoff_latitude)
                dropoff_longitude = float(payload['dropoff_longitude'])
                dropoff_lon = convert_coordinate(dropoff_longitude)
                time = str(payload['time'])
                converted_time = convert_time(time)
                date = str(payload['date'])
                converted_month, converted_day = convert_date(date)
                
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin","*")
                self.send_header("Access-Control-Allow-Methods","*")
                self.send_header("Access-Control-Allow-Headers","*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                
                # call the prediction function in ml.py
                result = ml.predict(duration, miles, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, converted_time, converted_month, converted_day)
                accuracy = ml.get_accuracy(converted_month)
                
                # make a dictionary from the result
                resultObj = { "fare": result,
                              "accuracy": accuracy }
                
                # convert dictionary to JSON string
                resultString = json.dumps(resultObj)
                
                self.wfile.write(resultString.encode('utf-8'))
                
            else:
                self.send_error(404, 'endpoint not supported')  
                
        except IOError:
            self.send_error(404, 'endpoint not found')  

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print("Starting training...")
    ml.kNN_train()
    print(f"Starting server on {addr}:{port}")
    httpd.serve_forever()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
       "-l",
       "--listen",
       default="localhost",
       help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
       "-p",
       "--port",
       type=int,
       default=8000,
       help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
