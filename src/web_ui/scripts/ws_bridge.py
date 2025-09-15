#!/usr/bin/env python3
import asyncio
import json
import math
import rospy
import websockets
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class WSBridge:
    def __init__(self):
        self.clients = set()
        self.loop = asyncio.get_event_loop()
        self.joint_pub = rospy.Publisher('/webui/joint_target', Float64MultiArray, queue_size=1)
        self.grip_pub = rospy.Publisher('/webui/gripper', Float64, queue_size=1)
        rospy.Subscriber('/joint_states', JointState, self.joint_state_cb)
        self.last_joint_state = None

    async def handler(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    rospy.logwarn('Invalid JSON: %s', message)
                    continue
                cmd = data.get('cmd')
                if cmd == 'set_joints':
                    arr = data.get('joints', [])
                    msg = Float64MultiArray(data=arr)
                    self.joint_pub.publish(msg)
                elif cmd == 'gripper':
                    val = data.get('value', 0.0)
                    self.grip_pub.publish(Float64(data=val))
                elif cmd == 'ping':
                    await websocket.send(json.dumps({'topic':'pong', 't': data.get('t')}))
                elif cmd == 'stop':
                    rospy.loginfo('Received stop command')
        finally:
            self.clients.remove(websocket)

    def joint_state_cb(self, msg):
        self.last_joint_state = msg
        deg = [math.degrees(p) for p in msg.position[:6]]
        payload = json.dumps({'topic':'state', 'joints_deg':deg, 'motion':'unknown'})
        for ws in list(self.clients):
            asyncio.run_coroutine_threadsafe(ws.send(payload), self.loop)

async def main():
    rospy.init_node('ws_bridge')
    bridge = WSBridge()
    server = await websockets.serve(bridge.handler, '0.0.0.0', 8765)
    rospy.loginfo('WebSocket bridge listening on 0.0.0.0:8765')
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
