#Importing relevant packages
from boldswimsuite import BOLDgeometry, BOLDsequence, BOLDspins
import matplotlib.pyplot as plt
import numpy as np

def main():

    vessel_diameter = 0.002
    nsteps = 600
    
    voxel = BOLDgeometry.ContinuousVoxel2D.from_random(
        num_vessels=50,
        CBV=0.02,
        B0=3,
        labels=['vesselGroup1'],
        weights={'vesselGroup1': 1},
        diameter_distributions={'vesselGroup1': [vessel_diameter]},
        dchis={'vesselGroup1': 3e-8},
        permeation_probabilities={'vesselGroup1': 0},
        vessel_type='cylinder',
        allow_vessel_intersection=True,
        seed=1,
        progressbar=True
    )
    
    print(voxel)

    voxel.show() 
        
    spins = BOLDspins.Spins2D(
        ADC=0.001,
        num_spins=10_000,
        geometry=voxel,
        dt=0.2,
        IV=True,
        seed=1
    )

    sequence = BOLDsequence.SpinSequence(
        spins=spins,
        pulse_time_indices=[0, 175],
        pulse_angles=[np.pi/2, np.pi],
        pulse_axes=[[np.pi/2, np.pi/2], [np.pi/2, 0]]      
    )

    eviv, ev, iv = sequence.walk(
        dt=0.2,
        num_steps=nsteps,
        progressbar=True
    )

    time_range = np.arange(0, nsteps * spins.dt, spins.dt)

    #plotting
    f, (ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15,5))

    ax1.plot(time_range, eviv)
    ax1.set_title('Total')
    ax2.plot(time_range, ev)
    ax2.set_title('EV')
    ax3.plot(time_range, iv)
    ax3.set_title('IV')
    f.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()