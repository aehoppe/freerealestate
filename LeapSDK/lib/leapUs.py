
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import matplotlib.pyplot as plt

from numpy import pi

app_width = 1920/2
app_height = 1080/2

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        frame = controller.frame()

        everything = literallyEverything(controller)
        # ohgod.append(everything["position"])
        # print "pinchin: {}, color: {}, position: {}, {}".format(everything["mode"], everything["color"], everything["position"][0], everything["position"][1])

        # print "Pinch Strength: %f" % frame.hands.rightmost.pinch_strength
        # # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
    # #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

def literallyEverything(controller):
    """
    Returns literally literallyEverything
    """
    frame = controller.frame()

    everything = {
        "mode": "",
        "position": (-1,-1),
        "color": None,
        "thickness": None
    }

    if frame.hands.rightmost.is_right:

        pinch = frame.hands.rightmost.pinch_strength
        grab = frame.hands.rightmost.grab_strength

        if grab > pinch and grab > 0.9:
            everything["mode"] = 'clear'
        elif pinch > 0.7:
            everything["mode"] = 'draw'

        if frame.hands.rightmost.is_valid:
            everything["position"] = positionMap(controller)

            # #for finger thickness gestures
            # rIndexFinger = frame.hands.rightmost.fingers[1] #take right index finger
            # if frame.hands.leftmost.is_valid:
            #     lIndexFinger = frame.hands.leftmost.fingers[1] #take right index finger
            #     rIndexFingerPos = rIndexFinger.bone(3).center #position of tip of right index finger
            #
            #     if rIndexFingerPos == lIndexFinger.bone(0).center:
            #         print '0'
            #     elif rIndexFingerPos == lIndexFinger.bone(1).center:
            #         print '1'
            #     elif rIndexFingerPos == lIndexFinger.bone(2).center:
            #         print '2'
            #     elif rIndexFingerPos == lIndexFinger.bone(3).center:
            #         print '3'

    # if knownFinger.is_valid:
    #     fingerPos = knownFinger.position
    #     print "\n Finger Position: {}".format(fingerPos)

    if frame.hands.leftmost.is_left and frame.hands.leftmost.palm_normal.is_valid and frame.hands.leftmost.pinch_strength < 0.4:
        angle = frame.hands.leftmost.palm_normal.roll
        # Map color so you only need to do 270 degrees hand rotation to get the full color wheel
        everything["color"] = (((pi - angle) * 180 / pi) * 360/270) % 360 # don't even worry about it
    if frame.hands.leftmost.is_left and frame.hands.leftmost.grab_strength > 0.7:
        # print frame.hands.leftmost.palm_position
        iBox = frame.interaction_box
        leapPoint = frame.hands.leftmost.stabilized_palm_position
        normalizedPoint = iBox.normalize_point(leapPoint, False)
        thickness = normalizedPoint.x*10
        if thickness<1:
            thickness = 1
        elif thickness>10:
            thickness = 10
        everything["thickness"] = thickness
        print everything['thickness']

    return everything

def positionMap(controller):
    """
    maps position
    thanks leap motion website
    """
    frame = controller.frame()

    app_x = -1
    app_y = -1

    pointable = frame.pointables.rightmost
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
       # plt.plot(*zip(*ohgod), marker='*')
       # plt.show()

       # Remove the sample listener when done
       controller.remove_listener(listener)

if __name__ == "__main__":
    main()
