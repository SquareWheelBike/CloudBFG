# Python script to run `octave demoBatterySimulator.m`, and provide an interface between Python and Octave for battery simulation.

# todo: add HTML responses? Perhaps we can use a local server to simulate batteries, so the pi doesn't have to simulate the battery

import subprocess
process = subprocess.Popen(['octave', 'demoBatterySimulator.m'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE,
                           universal_newlines=True,
                           bufsize=0)
stdout, stderr = process.communicate()
print(stdout)
