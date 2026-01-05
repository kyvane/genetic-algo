# works

import pybullet as p
import pybullet_data as pd
import creature
import time

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)

c = creature.Creature(gene_count=5)

with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())
    
cid = p.loadURDF('test.urdf')

p.setRealTimeSimulation(1)
c.update_position([0, 0, 0])

# Set position so object will not be pushed upwards
p.resetBasePositionAndOrientation(cid, [0, 0, 1], [0, 0, 0, 1])


while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]
        p.setJointMotorControl2(cid, jid, 
                                controlMode = p.VELOCITY_CONTROL,
                                targetVelocity = m.get_output(),
                                force=5)
    pos,orn = p.getBasePositionAndOrientation(cid)
    c.update_position(pos)
    print(c.get_distance_travelled())
    time.sleep(0.1)