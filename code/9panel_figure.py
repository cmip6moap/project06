import cartopy.crs as ccrs
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import nc_time_axis
import cftime
import xclim as xc

# INPUT DATA HERE!

######### 9-panel graph ##########
fig1, axs1 = plt.subplots(nrows=3, ncols=3, figsize=(16, 10), subplot_kw={'projection': ccrs.EckertIII()})
# annual
# SSP585-G6sulfur
cf1 = axs1[0,0].contourf(rx_sulfur.lon, rx_sulfur.lat, rx_585.mean('time')-rx_sulfur.mean('time'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf1, ax=axs1[0,0], orientation='vertical', fraction=0.02, label="mm")
axs1[0,0].coastlines()
axs1[0,0].set_global()
axs1[0,0].set_title("SSP585-G6sulfur, annual")
# SSP245-G6sulfur
cf2 = axs1[0,1].contourf(rx_sulfur.lon, rx_sulfur.lat, rx_245.mean('time')-rx_sulfur.mean('time'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf2, ax=axs1[0,1], orientation='vertical',fraction=0.02, label="mm")
axs1[0,1].coastlines()
axs1[0,1].set_global()
axs1[0,1].set_title("SSP245-G6sulfur, annual")
# G6solar-G6sulfur
cf3 = axs1[0,2].contourf(rx_sulfur.lon, rx_sulfur.lat, rx_solar.mean('time')-rx_sulfur.mean('time'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf3, ax=axs1[0,2], orientation='vertical',fraction=0.02, label="mm")
axs1[0,2].coastlines()
axs1[0,2].set_global()
axs1[0,2].set_title("G6solar-G6sulfur, annual")
# DJF
# SSP585-G6sulfur
cf4 = axs1[1,0].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_585-rx_sulfur).groupby('time.month').mean('time').sel(month=[1,2,12]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf4, ax=axs1[1,0], orientation='vertical', fraction=0.02, label="mm")
axs1[1,0].coastlines()
axs1[1,0].set_global()
axs1[1,0].set_title("SSP585-G6sulfur, DJF")
# SSP545-G6sulfur
cf5 = axs1[1,1].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_245-rx_sulfur).groupby('time.month').mean('time').sel(month=[1,2,12]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf5, ax=axs1[1,1], orientation='vertical', fraction=0.02, label="mm")
axs1[1,1].coastlines()
axs1[1,1].set_global()
axs1[1,1].set_title("SSP245-G6sulfur, DJF")
# G6solar-G6sulfur
cf6 = axs1[1,2].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_solar-rx_sulfur).groupby('time.month').mean('time').sel(month=[1,2,12]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap="BrBG")
fig1.colorbar(cf6, ax=axs1[1,2], orientation='vertical', fraction=0.02, label="mm")
axs1[1,2].coastlines()
axs1[1,2].set_global()
axs1[1,2].set_title("G6solar-G6sulfur, DJF")
# JJA
# SSP585-G6sulfur
cf7 = axs1[2,0].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_585-rx_sulfur).groupby('time.month').mean('time').sel(month=[6,7,8]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap='BrBG')
fig1.colorbar(cf7, ax=axs1[2,0], orientation='vertical', fraction=0.02, label="mm")
axs1[2,0].coastlines()
axs1[2,0].set_global()
axs1[2,0].set_title("SSP585-G6sulfur, JJA")
# SSP245-G6sulfur
cf8 = axs1[2,1].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_245-rx_sulfur).groupby('time.month').mean('time').sel(month=[6,7,8]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap='BrBG')
fig1.colorbar(cf8, ax=axs1[2,1], orientation='vertical', fraction=0.02, label="mm")
axs1[2,1].coastlines()
axs1[2,1].set_global()
axs1[2,1].set_title("SSP245-G6sulfur, JJA")
# G6solar-G6sulfur
cf9 = axs1[2,2].contourf(rx_sulfur.lon, rx_sulfur.lat, (rx_solar-rx_sulfur).groupby('time.month').mean('time').sel(month=[6,7,8]).mean('month'), \
                        transform=ccrs.PlateCarree(), levels=np.linspace(-50,50,11), cmap='BrBG')
fig1.colorbar(cf9, ax=axs1[2,2], orientation='vertical', fraction=0.02, label="mm")
axs1[2,2].coastlines()
axs1[2,2].set_global()
axs1[2,2].set_title("G6solar-G6sulfur, JJA")
fig1.suptitle("RX5day differences, 2090-2100", fontsize=16)
fig1.tight_layout()
plt.savefig("plots/CMIP6Hackathon/diff_G6_SSP_rx5day_2090-2100_annual_djf_jja_dpi300.png", format="png", dpi=300)