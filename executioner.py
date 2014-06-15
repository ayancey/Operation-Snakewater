# Snakewater Executioner
# Copyright Meanberg Design 2014
# Version 1.0
import sys
import netstat_metric
import registry_metric
import chrome_metric

print 'Snakewater Executioner v1.0 by Meanberg Design'
sys.stdout.write("Press any key to begin...")
raw_input()

#chrome_metric.execute()
registry_metric.execute()
#netstat_metric.execute()
