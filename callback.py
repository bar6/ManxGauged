"""
We want to run a function asychronously and run a
callback function with multiple parameters when it
returns!
In this example, we are pretending we're analyzing
the names and ages of some people. We want to print
out:
jack 0
jill 1
james 2
"""

import time
from multiprocessing.dummy import Pool
from functools import partial
pool = Pool(processes=1)

count = 0

def async_function(name):
	global count
	time.sleep(1)
	count = count + 1
	return
    
def callback_function(name, age):
	print count
	
	#do the loop again
	new_callback_function = partial(callback_function, age=6)
	pool.apply_async(
		async_function,
		args=["start"],
		callback=new_callback_function
	)
	
	
print "here"

new_callback_function = partial(callback_function, age=6)
pool.apply_async(
	async_function,
	args=["start"],
	callback=new_callback_function
)

while(1):
	
	print "--"
	time.sleep(0.2)
	

	

pool.close()
pool.join()

"""
Hooray!
"""
