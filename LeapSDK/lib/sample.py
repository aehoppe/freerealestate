import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import matplotlib.pyplot as plt

ohgod = []

class SampleListener(Leap.Listener):

	def on_connect(self, controller):
		print "Connected"


	def on_frame(self, controller):
	    frame = controller.frame()

	    everything = literallyEverything(controller)
	    ohgod.append(everything["position"])
	    print "pinchin: %f, position: %f, %f" % (frame.hands.rightmost.palm_velocity, everything["position"][0], everything["position"][1])
	    
	    # print "Pinch Strength: %f" % frame.hands.rightmost.pinch_strength
	    # # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
     # #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

def literallyEverything(controller):
	"""
	Returns literally literallyEverything
	"""	    
	frame = controller.frame()

	everything = {
		"mode": "None",
		"position": (-1,-1)
	}

	if frame.hands.rightmost.pinch_strength > 0.7:
		everything["mode"] = 'draw'
	elif frame.hands.rightmost.grab_strength > 0.7:
		everything["mode"] = 'clear'

	if frame.hands.rightmost.is_valid:
		everything["position"] = positionMap(controller)

	return everything

def positionMap(controller):
	"""
	maps position
	thanks leap motion website
	"""
	frame = controller.frame()

	app_width = 800
	app_height = 600

	app_x = -1
	app_y = -1

	pointable = frame.pointables.frontmost
	if pointable.is_valid:
	    iBox = frame.interaction_box
	    leapPoint = pointable.stabilized_tip_position
	    normalizedPoint = iBox.normalize_point(leapPoint, False)
	    
	    app_x = normalizedPoint.x * app_width
	    app_y = (1 - normalizedPoint.y) * app_height
	    #The z-coordinate is not used

	return (app_x, app_y)

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
    	plt.plot(*zip(*ohgod), marker='*')
    	plt.show()
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
	main()