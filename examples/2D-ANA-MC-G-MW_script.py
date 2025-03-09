#Importing relevant packages
from boldswimsuite import BOLDsequence, BOLDspins, BOLDgeometry, BOLDvessel
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    position_file = os.path.join(dir_path, 'axonfiles', 'positions_1000.csv')
    radii_file = os.path.join(dir_path, 'axonfiles', 'radii_1000.csv')
    
    CBV = 0.01

    # B0 field direction for axons
    axon_B0_phi=np.pi/2
    axon_B0_theta=np.pi/2

    blood_vessel_dchi = 3e-8 #cgs
    axon_dchi = -1.5e-8 #cgs
    nsteps = 600

    # used to pick the blood vessels from the packed axons
    seed = 1

    # get the axon data generated from the AxonPacking package
    axon_positions = np.loadtxt(position_file, delimiter=',')
    axon_radii = np.loadtxt(radii_file, delimiter=',')
    _, num_axons = axon_positions.shape
    
    max_pos_x = np.max(axon_positions[0, :])
    max_pos_y = np.max(axon_positions[1, :])
    min_pos_x = np.min(axon_positions[0, :])
    min_pos_y = np.min(axon_positions[1, :])

    # we need to crop the voxel because only the center of the voxel has properly packed axons (sparse at the edges)
    crop_factor = 0.5

    size_x = crop_factor*(max_pos_x - min_pos_x)/1000 # convert from micrometers to millimeters
    size_y = crop_factor*(max_pos_y - min_pos_y)/1000
    size = np.max([size_x, size_y])

    # initialize empty continuous voxel 
    continuous_voxel = BOLDgeometry.ContinuousVoxel2D(
        size=size,
        B0=3
    )

    rng = np.random.default_rng(seed)

    # computing the number of axons to turn into blood vessels
    num_vessels = int(CBV*num_axons)

    # randomly choosing axons to become blood vessels
    vessel_indices = rng.choice(np.arange(num_axons), num_vessels, replace=False)
    
    perturber_counter = 0

    text = 'Populating Voxel'
    for i in tqdm(range(0, num_axons), desc=text):
        
        # normalize to voxel size
        origin_x = (axon_positions[0, i] - (min_pos_x + max_pos_x)/2 )/1000 ## units of um converted to mm and centred at zero
        origin_y = (axon_positions[1, i] - (min_pos_y + max_pos_y)/2 )/1000 ## units of um converted to mm and centred at zero
        
        # skip any vessels outside the cropped voxel
        if (origin_x > size/2) or (origin_x < -size/2):
            continue
        if (origin_y > size/2) or (origin_y < -size/2):
            continue

        diameter = axon_radii[i] / 1000 # units of um convert to mm

        # if the cylinder has been picked to be a blood vessel, use the blood vessel parameters and a random B0
        if perturber_counter in vessel_indices:
            vessel = BOLDvessel.InfiniteCylinder2D(
                diameter=2*diameter,
                B0_theta=np.arccos(2*rng.random() - 1),
                B0_phi=2*np.pi*rng.random(),
                origin = np.array([origin_x, origin_y]), 
                dchi=blood_vessel_dchi,
                permeation_probability=0,
                label='blood vessel'
            )
        # otherwise the cylinder is an axon, so use the axon parameters and a fixed B0      
        else:
            #generate vessel
            vessel = BOLDvessel.InfiniteCylinder2D(
                diameter=2*diameter,
                B0_theta=axon_B0_theta,
                B0_phi=axon_B0_phi,
                origin = np.array([origin_x, origin_y]), 
                dchi=axon_dchi,
                permeation_probability=0,
                label='axon'
            )                        

        perturber_counter += 1

        # adding the vessel to the voxel
        continuous_voxel.add_vessel(vessel)

    continuous_voxel.show()
    
    discrete_voxel = BOLDgeometry.DiscreteVoxel2D.from_continuous_analytical(
    N=500, ## grid resolution
    voxel=continuous_voxel
    )

    discrete_voxel.show(show_dBz=True)

    # show the voxel dBz and vessels and differentiate the blood vessels from axons
    is_IV_grid = 1*(discrete_voxel.vessel_index_grid.T > 0)
    
    for vind in vessel_indices:
        is_IV_grid[discrete_voxel.vessel_index_grid.T == (vind+1)] = 2
    
    plt.imshow(is_IV_grid, origin='lower')
    plt.show()

    # create spins object for simulation
    spins = BOLDspins.Spins2D(
        ADC=0.001,
        num_spins=10_000,
        geometry=discrete_voxel,
        dt=0.2,
        IV=True,
        seed=1
    )

    # here we use a sequence object because we want to partition the EV/IV space using only the blood vessels, so we need more control over how the signal is calculated
    sequence = BOLDsequence.Sequence(
        sample_shape=spins.num_spins,
        pulse_time_indices=[0, 175],
        pulse_angles=[np.pi/2, np.pi],
        pulse_axes=[[np.pi/2, np.pi/2], [np.pi/2, 0]]      
    )

    eviv = np.zeros(nsteps) 
    ev = np.zeros(nsteps)
    iv = np.zeros(nsteps)

    text = 'Walking Through'
    for j in tqdm(range(nsteps), desc=text):
        
        phase, vessel_index, dt = spins.get_phase_vessel_indices_dt()

        for i in range(np.max(discrete_voxel.vessel_index_grid)):
            if i in vessel_indices:
                continue
            vessel_index[vessel_index == i] = 0 

        sequence.step(phase, vessel_index != 0, dt)

        eviv[j], ev[j], iv[j] = sequence.get_signals()
    
    time_range = np.arange(0, nsteps * spins.dt, spins.dt)

    #printing number of vessels
    print('Number of vessels:', len(continuous_voxel.vessels))

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
