# changed environment to cw_envt

import pybullet as p
from multiprocessing import Pool
from cw_envt import make_arena

class Simulation: 
    def __init__(self, sim_id=0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr, iterations=2400):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId=pid)
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid)
        p.setGravity(0, 0, -10, physicsClientId=pid)

        # make arena
        arena_size = 20
        arena_position = (0, 0, 0)  # Arena center position
        make_arena(arena_size=arena_size, position=arena_position)
        mountain_position = (0, 0, -1)  # Adjust as needed
        mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
        p.setAdditionalSearchPath('shapes/')
        mountain = p.loadURDF("gaussian_pyramid.urdf",
                              mountain_position,
                              mountain_orientation,useFixedBase=1)


        xml_file = 'temp' + str(self.sim_id) + '.urdf'
        xml_str = cr.to_xml()
        with open(xml_file, 'w') as f:
            f.write(xml_str)
        
        cid = p.loadURDF(xml_file, physicsClientId=pid)
        
        # Check if creature loaded successfully (loadURDF returns -1 on failure)
        if cid < 0:
            # If creature failed to load, set a very poor position (far from mountain)
            cr.update_position([1000, 1000, 1000])
            return  # Exit early, creature is invalid

# !! changed
        p.resetBasePositionAndOrientation(cid, [5, -5, 2.5], [0, 0, 0, 1])


        for step in range(iterations):
            p.stepSimulation(physicsClientId=pid)
            if step % 24 == 0:
                self.update_motors(cid=cid, cr=cr)

            # Check if body still exists before getting position
            try:
                pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
                cr.update_position(pos)
            except:
                # If body was removed or invalid, set poor position and exit
                cr.update_position([1000, 1000, 1000])
                break
        
    
    def update_motors(self, cid, cr):
        """
        cid is the id in the physics engine
        cr is a creature object
        """
        # Check if creature ID is valid
        if cid < 0:
            return
        
        try:
            num_joints = p.getNumJoints(cid, physicsClientId=self.physicsClientId)
            motors = cr.get_motors()
            
            for jid in range(num_joints):
                if jid < len(motors):
                    m = motors[jid]
                    p.setJointMotorControl2(cid, jid, 
                            controlMode=p.VELOCITY_CONTROL, 
                            targetVelocity=m.get_output(), 
                            force = 5, 
                            physicsClientId=self.physicsClientId)
        except:
            # If there's an error updating motors, just skip this update
            pass
        
    def eval_population(self, pop, iterations):
        for cr in pop.creatures:
            self.run_creature(cr, 2400) 


class ThreadedSim():
    def __init__(self, pool_size):
        self.sims = [Simulation(i) for i in range(pool_size)]

    @staticmethod
    def static_run_creature(sim, cr, iterations):
        sim.run_creature(cr, iterations)
        return cr
    
    def eval_population(self, pop, iterations):
        pool_args = [] 
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.creatures):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.creatures):
                    break
                sim_ind = i % len(self.sims)
                this_pool_args.append([
                            self.sims[sim_ind], 
                            pop.creatures[i], 
                            iterations]   
                )
            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size

        new_creatures = []
        for pool_argset in pool_args:
            with Pool(pool_size) as p:
                creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
                new_creatures.extend(creatures)
        pop.creatures = new_creatures
