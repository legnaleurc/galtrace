#! /usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

subprocess.call( [ 'python', '-m', 'unittest', 'galtrace.libs.crawler.tests' ] )
subprocess.call( [ 'python', 'manage.py', 'test', 'shell' ] )
