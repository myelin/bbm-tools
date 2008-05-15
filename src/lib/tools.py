# Copyright (c) 2007-2008 Broadband Mechanics, Inc.
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os, os.path, re, sys
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], ".."))
try:
    import config
except ImportError:
    print "config.py not found; please read the README for more info"
    sys.exit(1)

def setup_config():
    for hostname,server in config.servers.items():
        server["hostname"] = hostname
setup_config()

class Script:
    
    def cmd(self, s):
        print s
        if os.system(s):
            raise Exception("Command failed")

def run_in_script_dir(func, *args, **kw):
    try:
        script_root = os.path.abspath(os.path.split(sys.argv[0])[0])
        cwd = os.getcwd()
        os.chdir(script_root)

        return func(*args, **kw)

    finally:
        os.chdir(cwd)

def find_hosts(pat):
    r = []
    for host,info in config.servers.items():
        if re.search(pat, host):
            r.append((host,info))
    return r

def find_host(pat):
    r = find_hosts(pat)
    if len(r) == 0: raise Exception("failed to find host matching %s" % pat)
    if len(r) > 1: raise Exception("pattern %s matched more than one host: %s" % (pat, ", ".join([h[0] for h in r])))

    return r[0]
