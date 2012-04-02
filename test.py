#! /usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

subprocess.call( [ 'python', '-m', 'unittest', 'kernel.sites.tests' ] )
subprocess.call( [ 'python', 'manage.py', 'test', 'kernel' ] )
