#!/usr/bin/env python
import Image
import ImageStat
import math
import os
import time
import sys
import json


default_samplerate = 5
fixed = False
home_path = os.getenv("HOME")
file_path = home_path + "/.config/wildguppy/config.json"
default_config = {'samplerate':str(default_samplerate), 'maxbrightness':"100", 'minbrightness':"0"}

try:
    config_file = json.load(open(file_path))
except:
    os.system("mkdir %s/.config/wildguppy/" % home_path)
    os.system("touch %s" % file_path)
    json.dump(default_config, open(file_path, 'w'))
    config_file = json.load(open(file_path))
    
maxbr = float(config_file['maxbrightness'])
minbr = float(config_file['minbrightness'])

def brightness(im_file):
       im = Image.open(im_file)
       stat = ImageStat.Stat(im)
       r,g,b = stat.mean
       return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def takeSample(tmpimg):
    os.system("fswebcam -r 356x292 -d /dev/video0 %s" %tmpimg)

def error_msg(type, arg):
    if type == 1:
        print "Error: enter your argument after '%s'" % arg 

    if type == 2:
        print "autobrightness: There is no '%s' OPTION." % arg

    if type == 3:
        print "Invalid Input: Enter only numbers as arguments!"

    print "\nTry 'autobrightness --help' for more information"
    pass

class autoBrightness():
    def __init__(self):
        self.maxbr_ = maxbr
        self.minbr_ = minbr
        
    def run(self, samplerate=config_file['samplerate']):
        self.samplerate = float(samplerate)
        first = True
        old_set = 0
        while True:
            sum_new_set = 0
            for x in xrange(0,5):
                tmpimg = "/tmp/autobrightness-sample.jpg"
                takeSample(tmpimg)
                brightnessLevel = brightness(tmpimg)
                print brightnessLevel
                set = (brightnessLevel*100.0)/110.0
                new_set = self.minbr_ + ((self.maxbr_ - self.minbr_)*set)/100.0
                # print 'in cal avg new_set is'
                # print new_set
                sum_new_set += new_set
                if first == False:
                    time.sleep(self.samplerate / 5)
            new_set = sum_new_set / 5
            # print "new_set is"
            # print new_set

            # print "old_set is"
            # print old_set
            
            if first == False:
                new_set = (2 * old_set + new_set) / 3
            first = False
            # print 'final set is'
            # print new_set
            old_set = new_set
            os.system('xbacklight -set %s' % str(new_set))
            # print 'xbacklight is'
            # print os.system('xbacklight')
            # time.sleep(self.samplerate)
            
    def run_once(self):
        tmpimg = "/tmp/autobrightness-sample.jpg"
        takeSample(tmpimg)
        brightnessLevel = brightness(tmpimg)
        print brightnessLevel
        set = (brightnessLevel*100.0)/110.0
        new_set = self.minbr_ + ((self.maxbr_ - self.minbr_)*set)/100.0
        print "\n"
        print new_set
        # new_set = (old_set + new_set) / 2
        # print "old_set is"
        # global old_set
        # print old_set
        # old_set = new_set;
        os.system('xbacklight -set %s' % str(new_set))
        return True
        
if __name__ == "__main__":
    run = False
    args = sys.argv
    if len(args) >= 2:
        for i in xrange(len(args)):
            error = True
            if args[i] == "help" or args[i] == "--help" or args[i] == "-help" or args[i] == "-h":
                print "USAGE: autobrightness [OPTION]... [VALUE]...\n\n Adjusts a laptop's brightness automatically, by using camera samples taken at a user definable interval.\n\n -s, --set              set time between samples to your configuration file\n -t, --time             set time between samples for this session\n -x, --max              set maximium brightness level to the config file\n -n, --min              set minimium brightness level to the config file"
                sys.exit()

            if args[i] == "-s" or args[i] == "--set":
                error = False
                try:
                    float(args[i+1])
                    config_file['samplerate'] = args[i+1]
                    json.dump(config_file, open('config.json', 'w'))
                    print "Your default time interval is now '%s' seconds\n" % args[i+1]
                except IndexError:
                    error_msg(1, args[i])
                    sys.exit()
                except ValueError:
                    error_msg(3, args[i+1])
                    sys.exit()

            
            if args[i] == "-x" or args[i] == "--max":
                try:
                    float(args[i+1])
                    config_file['maxbrightness'] = args[i+1]
                    json.dump(config_file, open('config.json', 'w'))
                    print "Your maximium brightness value is now '%s'\n" % args[i+1]
                except IndexError:
                    error_msg(1, args[i])
                    sys.exit()
                except ValueError:
                    error_msg(3, args[i+1])
                    sys.exit()

            if args[i] == "-n" or args[i] == "--min":
                try:
                    float(args[i+1])
                    config_file['minbrightness'] = args[i+1]
                    json.dump(config_file, open('config.json', 'w'))
                    print "Your minimium brightness value is now '%s'\n" % args[i+1]
                except IndexError:
                    error_msg(1, args[i])
                    sys.exit()
                except ValueError:
                    error_msg(3, args[i+1])
                    sys.exit()

            if args[i] == "-t" or args[i] == "--time":
                error = False
                run = True
                try:
                    arg = float(args[i+1])
                    if arg < 0:
                        print "Your sampling rate cannot be a negative number.  Resetting to default value of 5."
                    else:
                        samplerate = arg
                except IndexError:
                    error_msg(1, args[i])
                    sys.exit()
                except ValueError:
                    error_msg(3, args[i+1]) 
                    sys.exit()
                break
                        if args[i] == "-g" or args[i] == "--gui":
                   error = False
                           os.system("./panel_app.py")

        if error:
            error_msg(2, args[i])
    else:
        run = True

    if run:
        a = autoBrightness()
        a.run()
