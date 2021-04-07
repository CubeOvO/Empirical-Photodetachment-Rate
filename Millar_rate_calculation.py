import pandas as pd



'''
@authors: Zeqi Zhang (zeqi.zhang17@imperial.ac.uk), Xinni Wu
This code calculates the photodetachment rate for a negative ion subjected to 
either the quiet or active solar photon spectrum, as descibed in the publication:

Desai, RT, Zhang, Z., Wu, X., Lue, C., (2021) Photodetachment and Test-Particles Simlations Constraints on Negative Ions in Solar System Plasmas, Planetary Science Journal, doi:XXXX

The code requires the Electron Affinity in eV and Assymptotic cross-section in cm^2
as inputs and uses the method described in Huebner et al. (1992) and Millar et al. (2007)
'''

# active sun flux is used if the following variable is set to true, otherwise the quite sun flux is used
active_Sun_Flux = True
Electron_Affinity = 3.019        # Unit: eV
Asymptotic_Cross_Section = 8.8*10**-18        # Unit: cm^-2


def length_ev(w):
    # convert wavelength in A to eV
    ev = []
    for i in range(len(w)):
        if w[i] == 0:
            k= 0
        k = ((6.63*10**-34)*3*10**8)/((w[i]*10**-10)*1.6*10**-19)
        ev.append(k)
    return ev

# millar cross section
def sigma(sigin, ea, wavelength):
    energy = length_ev(wavelength)
    sigma = []
    for i in range(len(energy)):
        if energy[i] >= ea:
            y = sigin*(1-ea/energy[i])**0.5
            sigma.append(y)
        else:
            sigma.append(0)
    return sigma


def width(w):
    '''
    :param w: a list containing increasing numbers
    :return: a list denoting the difference between each number
    '''
    d_w = []
    for i in range(len(w)):
        if i < len(w)-1:
            d_w.append(abs(w[i+1]-w[i]))
    return d_w

def main():
    # import solar flux
    if active_Sun_Flux:
        df = pd.read_csv('active_flux.csv')
    else:
        df = pd.read_csv('quiet_flux.csv')
    wlength = list(df['Wavelength'])
    flux = list(df['Flux'])
 
    wlength = list(wlength)
    wwidth = width(wlength)

    # calculate the cross section

    csc = sigma(Asymptotic_Cross_Section,Electron_Affinity,wlength)
    k_rate = [x*y for x,y in zip(csc,flux)]
    print('The total reaction rate is :',sum(k_rate),'s^-1')






if __name__ == '__main__':
    main()







# set sigma infinity and electron affinity
# some example sigin_data and EA data used in the paper are listed below

# chem = ['H-','O-','OH-','c']
# sigin_data = [1.0*10**-17,1.2*10**-17,3.3*10**-17,2*10**-17]
# ea_data = [0.75,1.5,1.8,1.26]
# CnN 1,3,5
# sigin_data = [2.84*10**-17,5.19*10**-17,1*10**-17]
# ea_data = [3.862,4.305,5.5]
# CnH 2,4,6
# sigin_data = [8.8*10**-18,7.7*10**-18,4.8*10**-18]
# ea_data = [3.019,3.561,3.796]

# f, cl, br
# sigin_data = [1.0*10**-17,4.0*10**-17,5.0*10**-17]
# ea_data = [3.4, 3.61, 3.36]