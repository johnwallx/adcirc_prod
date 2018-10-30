




import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import netCDF4 as nc4
import matplotlib as mpl
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import FancyArrowPatch
from PIL import Image
import glob
import os
import scipy.interpolate

class swan:

    def __init__(self,path, file):
        self.path = path
        self.file = file
        self.fp   = os.path.join(self.path,self.file)
        
        
    
    def swan_HS(global_path,netcdf_file,title,hours1,levels,lon1,lon2,lat1,lat2,start=None):
        start_date = datetime.strptime(start,'%Y%m%d%H')
        wl=[]
        xx = netcdf_file.variables['x'][:]
        yy = netcdf_file.variables['y'][:]
        gridvars = netcdf_file.variables      
        var_element = 'element'
        elems = gridvars[var_element][:,:]-1
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,
                    llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
        #data2 = netcdf_file.variables['zeta'][:]
        for i in range(0,hours1):
            i=i+1
            data1 = netcdf_file.variables['swan_HS'][i,:]
            file_number = '%05d'%i
            triang = tri.Triangulation(xx,yy, triangles=elems)
            m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=100, verbose= False)
            m.drawcoastlines(color='k')
            if data1.mask.any():
                point_mask_indices = np.where(data1.mask)
                tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
                triang.set_mask(tri_mask)
            plt.xlim([lon1, lon2])
            plt.ylim([lat1, lat2])    
            plt.tricontourf(triang, data1, levels=levels,alpha=0.75,
                            vmin=np.min(levels), vmax=np.max(levels), aspect='auto',cmap='jet')
            wl.append('WL{}.png'.format(file_number))
            cb = plt.colorbar(cmap='jet',fraction=0.026,pad=0.04) 
            cb.set_label('Wave Height at MSL (meters)',fontsize=10)
            plt.title(title + '\n')
            plt.xlabel('\nDate:{}'.format(start_date+ timedelta(hours=i)))
            plt.savefig('WL{}.png'.format(file_number),dpi=300,
                        bbox_inches = 'tight', pad_inches = 0.1)
            plt.close()
        images = []
        for ii in range(0,len(wl)):
            frames = Image.open(wl[ii])
            images.append(frames)
        images[0].save('gifs\\swan_waves.gif',
           save_all=True,
           append_images=images[1:],
           delay=.1,
           duration=300,
           loop=0)
        for f in glob.glob('WL*'):
            os.remove(f)    
        return    
    
    def swan(global_path,netcdf_file,netcdf_file2,title,hours1,levels,lon1,lon2,lat1,lat2,grid_space,start=None):
        start_date = datetime.strptime(start,'%Y%m%d%H')
        wl=[]
        xx = netcdf_file.variables['x'][:]
        yy = netcdf_file.variables['y'][:]
        xx2 = netcdf_file2.variables['x'][:]
        yy2 = netcdf_file2.variables['y'][:]
        xx = netcdf_file.variables['x'][:]
        yy = netcdf_file.variables['y'][:]
        xg = np.linspace(lon1+0.5,lon2-0.5,grid_space)
        yg = np.linspace(lat1+0.5,lat2-0.5,grid_space)
        xgrid,ygrid = np.meshgrid(xg,yg)
        gridvars = netcdf_file.variables      
        var_element = 'element'
        elems = gridvars[var_element][:,:]-1
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,
                    llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
        #data2 = netcdf_file.variables['zeta'][:]
        for i in range(0,hours1):
            i=i+1
            data1 = netcdf_file.variables['swan_HS'][i,:]
            data2 = netcdf_file2.variables['swan_DIR'][i,:]
            u = data1*np.cos(data2)
            v = data1*np.sin(data2)
            ugrid = scipy.interpolate.griddata((xx2,yy2),u,(xgrid,ygrid),method='nearest')
            vgrid = scipy.interpolate.griddata((xx2,yy2),v,(xgrid,ygrid),method='nearest')
            file_number = '%05d'%i
            u_norm = ugrid / np.sqrt(ugrid ** 2.0 + vgrid ** 2.0)
            v_norm = vgrid / np.sqrt(ugrid ** 2.0 + vgrid ** 2.0)
            triang = tri.Triangulation(xx,yy, triangles=elems)
            m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=300, verbose= False)
            m.drawcoastlines(color='k')
            if data1.mask.any():
                point_mask_indices = np.where(data1.mask)
                tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
                triang.set_mask(tri_mask)
            plt.xlim([lon1, lon2])
            plt.ylim([lat1, lat2])    
            plt.tricontourf(triang, data1, levels=levels,alpha=0.75,
                            vmin=np.min(levels), vmax=np.max(levels), aspect='auto',cmap='jet')
            wl.append('WL{}.png'.format(file_number))
            cb = plt.colorbar(cmap='jet',fraction=0.026,pad=0.04) 
            cb.set_label('Wave Height at MSL (meters)',fontsize=10)
            plt.quiver(xgrid,ygrid,u_norm,v_norm, pivot='mid', scale = 100, color='w')
            plt.title(title + '\n')
            plt.xlabel('\nDate:{}'.format(start_date+ timedelta(hours=i)))
            plt.savefig('WL{}.png'.format(file_number),dpi=300,
                        bbox_inches = 'tight', pad_inches = 0.1)
            plt.close()
        images = []
        for ii in range(0,len(wl)):
            frames = Image.open(wl[ii])
            images.append(frames)
        images[0].save('gifs\\swan.gif',
           save_all=True,
           append_images=images[1:],
           delay=.1,
           duration=300,
           loop=0)
        for f in glob.glob('WL*'):
            os.remove(f)    
        return        
    
    def max_swan_HS(global_path,netcdf_file,ax,title,levels,lon1,lon2,lat1,lat2):
        xx = netcdf_file.variables['x'][:]
        yy = netcdf_file.variables['y'][:]
        gridvars = netcdf_file.variables      
        var_element = 'element'
        elems = gridvars[var_element][:,:]-1
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,urcrnrlon=lon2,resolution='h', epsg = 4269)
        data1 = netcdf_file.variables['swan_HS_max'][:]
        triang = tri.Triangulation(xx,yy, triangles=elems)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=600, verbose= False)
        m.drawcoastlines(color='k')
        if data1.mask.any():
            point_mask_indices = np.where(data1.mask)
            tri_mask = np.any(np.in1d(elems, point_mask_indices).reshape(-1, 3), axis=1)
            triang.set_mask(tri_mask)
        plt.xlim([lon1, lon2])
        plt.ylim([lat1, lat2])    
        plt.tricontourf(triang, data1, levels=levels,alpha=0.75,vmin=np.min(levels), vmax=np.max(levels), aspect='auto',cmap='jet')
        cb=plt.colorbar(cmap='jet',fraction=0.026,pad=0.04) 
        cb.set_label('Wave Height at MSL (m)')
        plt.title(title + '\n')
        #plt.savefig('max_WL.png',dpi=500, bbox_inches = 'tight', pad_inches = 0.1)
        #plt.close()
        return plt.show()
        
        
        
        
        
        

