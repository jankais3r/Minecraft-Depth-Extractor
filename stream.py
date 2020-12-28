#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time
import ctypes
import socket
from threading import Event, Thread
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
try:
	import mss
except:
	print('Install mss with "pip3 install mss"')
	quit()
try:
	import win32api
	import win32gui
	from win32con import MONITOR_DEFAULTTONEAREST
except:
	print('Install pywin32 with "pip3 install pywin32"')
	quit()
try:
	import cv2
	import numpy as np
except:
	print('Install OpenCV with "pip3 install opencv-python"')
	quit()

ip = socket.gethostbyname(socket.gethostname())
port = 9090
x, y, w, h = 0, 0, 0, 0

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		global ip, port
		jpegQuality = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
		if self.path.endswith('/rgb.mjpg'):
			self.send_response(200)
			self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
			self.send_header('Access-Control-Allow-Origin', '*')
			self.end_headers()
			while True:
				if(rgbframe.any() != None):
					pass
				r, buf = cv2.imencode('.jpg', rgbframe, jpegQuality)
				try:
					self.wfile.write('--jpgboundary\r\n'.encode())
					self.end_headers()
					self.wfile.write(bytearray(buf))
				except:
					pass
			return
		
		if self.path.endswith('/depth.mjpg'):
			self.send_response(200)
			self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
			self.send_header('Access-Control-Allow-Origin', '*')
			self.end_headers()
			while True:
				if(depthframe.any() != None):
					pass
				r, buf = cv2.imencode('.jpg', depthframe, jpegQuality)
				try:
					self.wfile.write('--jpgboundary\r\n'.encode())
					self.end_headers()
					self.wfile.write(bytearray(buf))
				except:
					pass
			return
		
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>'.encode())
			self.wfile.write(('<img src="http://' + ip + ':' + str(port) + '/rgb.mjpg" style="max-width: 50%"/>').encode())
			self.wfile.write(('<img src="http://' + ip + ':' + str(port) + '/depth.mjpg" style="max-width: 50%"/>').encode())
			self.wfile.write('</body></html>'.encode())
			return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def callback(hwnd, extra):
	global x, y, w, h
	if win32gui.GetWindowText(hwnd)[:9] == 'Minecraft':
		shcore = ctypes.windll.shcore
		dpi_aware = shcore.SetProcessDpiAwareness(2)
		rect = win32gui.GetWindowRect(hwnd)
		x = rect[0] + 8
		y = rect[1] + 31
		w = rect[2] - x - 8
		h = rect[3] - y - 8
		print('Found "%s" ' % win32gui.GetWindowText(hwnd) + 'window of size (%d,%d) ' % (w, h) + 'in location (%d,%d).' % (x, y))

def main():
	global rgbframe, depthframe
	server = ThreadedHTTPServer(('0.0.0.0', port), CamHandler)
	print('Starting server on address ' + ip + ':' + str(port))
	target = Thread(target = server.serve_forever, args = ())
	target.start()
	mon = {'top': y, 'left': x, 'width': w, 'height': h}
	sct = mss.mss()
	
	while True:
		start = time.time()
		img = np.asarray(sct.grab(mon))
		if((img[0,0][0] == img[0,0][1] == img[0,0][2]) and (img[50,50][0] == img[50,50][1] == img[50,50][2])):
			depthframe = img
		else:
			rgbframe = img
		
		#cv2.imshow('Depthmap', depthframe)
		#cv2.imshow('RGB', rgbframe)
		#if cv2.waitKey(25) & 0xFF == ord("q"):
		#	cv2.destroyAllWindows()
		#	break

win32gui.EnumWindows(callback, None)
if(x ==0 and y == 0 and w == 0 and h == 0):
	print('No Minecraft window found.')
	quit()
rgbframe = np.zeros([w, h, 3], dtype = np.uint8)
rgbframe.fill(0)
depthframe = np.zeros([w, h, 3], dtype = np.uint8)
depthframe.fill(0)
main()
