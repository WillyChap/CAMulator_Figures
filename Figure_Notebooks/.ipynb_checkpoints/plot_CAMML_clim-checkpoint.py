import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import numpy as np
import argparse

def parseArguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, help="CESM Variable")
    args = parser.parse_args()

    return args.var_name
    
def define_plot_convention(var_name):

    if var_name=='CLDTOT':
        label_name='Total Cloud Fraction'
        rescale_factor=1.0

    elif var_name=='CLDLOW':
        label_name='Low Cloud Fraction'
        rescale_factor=1.0

    elif var_name=='CLDMED':
        label_name='Midlevel Cloud Fraction'
        rescale_factor=1.0
        
    elif var_name=='CLDHGH':
        label_name='High Cloud Fraction'
        rescale_factor=1.0
        
    elif var_name=='LHFLX':
        label_name='Surface Latent Heat FLux [W/(m2)]'
        rescale_factor=1.0    
        
    elif var_name=='PREC':
        label_name='Total Precipitation [mm/day]'
        rescale_factor=24 * 1000 * 3600

    elif var_name=='RELHUM':
        label_name='Relative Humidity [%]'
        rescale_factor=1.0

    elif var_name=='T':
        label_name='Temperature [K]'
        rescale_factor=1.0

    elif var_name=='U':
        label_name='Zonal Wind [m/s]'
        rescale_factor=1.0                        

    elif var_name=='AWNC':
        label_name='Avg. Cloud Water Number Conc. [10*6/(m3)]'
        rescale_factor=1.e-6                        
        
    elif var_name=='AWNI':
        label_name='Avg. Cloud Ice Number Conc. [10*4/(m3)]'        
        rescale_factor=1.e-4   
        
    elif var_name=='FSNS':
        label_name='Net Solar Flux at Surface [W/(m2)]'
        rescale_factor=1.0

    elif var_name=='FLNS':
        label_name='Net Longwave Flux at Surface [W/(m2)]'
        rescale_factor=1.0                

    elif var_name=='FLNT':
        label_name='Net Longwave Flux at TOA [W/(m2)]'
        rescale_factor=1.0

    elif var_name=='FSNT':
        label_name='Net Solar Flux at TOA [W/(m2)]'
        rescale_factor=1.0
        
    else:
        label_name=''
        rescale_factor=1.0
    
        
    return label_name, rescale_factor

def compute_compound_var(var_name,data):

    if var_name=='PREC':
        var_data = data['PRECL'] + data['PRECC']        
    else:        
        var_data = data[var_name]

    return var_data


if __name__ == "__main__":

    var_name = parseArguments()
    print(var_name)
    
    yog_path="/glade/derecho/scratch/jatkinson/archive/aquaplanet_CAM-ML/atm/hist/"
    zm_path="/glade/derecho/scratch/jatkinson/archive/aquaplanet_ZM/atm/hist/"
            
    file_yog_prefix="aquaplanet_CAM-ML.cam.h0.0001-"
    file_zm_prefix="aquaplanet_ZM.cam.h0.0001-"

    # create climatology
    num_month=3
    yog_file_list=[]; zm_file_list=[]
    for n in np.arange(3,num_month+1,1):
        yog_file_name=yog_path+file_yog_prefix+str(n).zfill(2)+'.nc'
        zm_file_name=zm_path+file_zm_prefix+str(n).zfill(2)+'.nc'        
        yog_file_list.append(yog_file_name)
        zm_file_list.append(zm_file_name)        
    yog_data_month = xr.open_mfdataset(yog_file_list)
    zm_data_month = xr.open_mfdataset(zm_file_list)    
    yog_data = yog_data_month.mean(dim="time")
    zm_data = zm_data_month.mean(dim="time")        

    # select domain
    yog_data = yog_data.sel(lat=slice(-90, 90))
    zm_data = zm_data.sel(lat=slice(-90, 90))     
    
    var_yog = compute_compound_var(var_name,yog_data)
    var_zm = compute_compound_var(var_name,zm_data)    
    
    lat=var_yog['lat'].values
    try:
        var_yog.coords["lev"].values
        print("3D variable")
        lev=var_yog['lev'].values
        keydim=2
    except KeyError:
        print("2D variable")
        keydim=1

    var_yog_val=var_yog.values
    var_zm_val=var_zm.values

    # produce hemispherically symmetric plots
    if keydim==2:
        var_yog_val_flipped=var_yog_val[:,::-1,:]       
        var_zm_val_flipped=var_zm_val[:,::-1,:]       

    elif keydim==1:
        var_yog_val_flipped=var_yog_val[::-1,:]       
        var_zm_val_flipped=var_zm_val[::-1,:]        
        
    var_yog_val = (var_yog_val + var_yog_val_flipped) / 2
    var_zm_val = (var_zm_val + var_zm_val_flipped) / 2        

    # compute time & zonal mean
    var_yog_zmean = np.nanmean(var_yog_val,axis=keydim)
    var_zm_zmean = np.nanmean(var_zm_val,axis=keydim)    

    [label_name, rescale_factor] = define_plot_convention(var_name)
    var_yog_zmean=var_yog_zmean*rescale_factor; var_zm_zmean=var_zm_zmean*rescale_factor
    var_diff_zmean = np.subtract(var_yog_zmean,var_zm_zmean)

    if keydim==1:

        # Zonal-mean Surface Variable 
        fig = plt.figure(figsize=(10, 6))
        plt.plot(lat, var_yog_zmean, 'g', label="YOG (NN)")
        plt.plot(lat, var_zm_zmean, 'r', label="ZM (original)")
        plt.ylabel(label_name)
        plt.xlabel('Latitude [deg]')
        plt.xlim((-90,90))
        plt.legend()
        fig.savefig(var_name + '.png')        
        plt.show()

    if keydim==2:

        if var_name=='RELHUM':
            var_min_val=0
            var_max_val=100.0

        elif var_name=='T':
            var_min_val=190.0
            var_max_val=300.0

        elif var_name=='U':
            var_min_val=-15.0
            var_max_val= 60.0            
            
        else:
            var_min_val=var_zm_zmean.min()
            var_max_val=var_zm_zmean.max()

        delvar_min_val = round(var_diff_zmean.min())
        delvar_max_val = round(var_diff_zmean.max())
        delvar_abs_val = np.absolute([delvar_min_val,delvar_max_val]).max()
        num_levels=7
        levels_n=np.linspace(-delvar_abs_val,-delvar_abs_val/(num_levels+1),num_levels+1)
        levels_p=np.linspace( delvar_abs_val/(num_levels+1),delvar_abs_val,num_levels+1)
        
        # Define number of colors by setting levels
        num_colors = 12
        levels = np.linspace(var_min_val, var_max_val, num_colors + 1)
        
        # Zonal-mean Atmosphere Variable
        fig = plt.figure(figsize=(10, 6))
        CF = plt.contourf(lat,lev,var_zm_zmean,levels=levels,cmap='Wistia')
        CSp = plt.contour(lat,lev,var_diff_zmean,levels=levels_p,linestyles='solid',colors='k')                   
        plt.clabel(CSp, inline=True, fontsize=10)                
        CSn = plt.contour(lat,lev,var_diff_zmean,levels=levels_n,linestyles='dashed',colors='k')
        plt.clabel(CSn, inline=True, fontsize=10)                
        plt.gca().invert_yaxis()
        plt.colorbar(CF)        
        plt.ylabel('Level [hPa]')        
        plt.xlabel('Latitude [deg]')
        plt.title(label_name)
        fig.savefig(var_name + '.png')
        plt.show()
