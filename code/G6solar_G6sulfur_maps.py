#!/usr/bin/env python
# coding: utf-8
from __future__ import division
import glob
import numpy as np
import iris
from iris.util import unify_time_units
from iris.experimental.equalise_cubes import equalise_attributes
import iris.coord_categorisation as icc
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt

    
# find data
models = ["UKESM1-0-LL"]
exps = ["G6solar", "G6sulfur"]

# options
syrs = [2020, 2050, 2090]
eyrs = [2030, 2060, 2100]
# seasons: jja | djf | all
season = "djf"
    
# loop models
for m in models:
    # loop exps
    results = []
    for e in exps:
        # monthly near surface air temps
        files = glob.glob("/badc/cmip6/data/CMIP6/GeoMIP/*/"+m+"/"+e+"/*/Amon/tas/*/latest/*.nc")
        cubelist = iris.load(files)
        unify_time_units(cubelist)
        equalise_attributes(cubelist)
        # each cube is one ensemble member
        cubes = cubelist.concatenate()
       
        if season=="all": 
            # annual means
            cubes_annual = iris.cube.CubeList()
            for c in cubes:
                icc.add_year(c, coord="time")
                cubes_annual.append(c.aggregated_by('year', iris.analysis.MEAN))
        else:
            cubes_annual = iris.cube.CubeList()
            for c in cubes:
                icc.add_year(c, coord="time")
                icc.add_season(c, coord="time")
                icc.add_season_year(c, coord="time")
                seasonal_means = c.aggregated_by(["season", "season_year"], iris.analysis.MEAN)
                # extract the season
                season_cons = iris.Constraint(season=season)
                cubes_annual.append(seasonal_means.extract(season_cons))

        # extract decade
        decades = iris.cube.CubeList()
        for (syr, eyr) in zip(syrs, eyrs):
            decade = iris.Constraint(time=lambda cell: syr <= cell.point.year <= eyr)
            cubes_decade = cubes_annual.extract(decade) 
            cubes_decade_means = iris.cube.CubeList()
            for c in cubes_decade:
                cubes_decade_means.append(c.collapsed("time", iris.analysis.MEAN))
            # ensemble mean
            enmean_decade = sum(cubes_decade_means, 0.0)/len(cubes_decade_means)
            decades.append(enmean_decade)
        
        # save results
        results.append(decades)

    # plot diff between G6sulfur and G6solar, by decade
    brewer_cmap = mpl_cm.get_cmap('brewer_RdBu_11')
    levels = np.linspace(-5, 5, 11)

    n = 1
    for y in range(len(syrs)):
        plt.figure(n, (12,8))
        cplot = iplt.contourf(results[1][y]-results[0][y], cmap=brewer_cmap, levels=levels)
        plt.gca().coastlines()
        if season=="all":
            plt.title("G6sulfur-G6solar, "+str(syrs[y])+"-"+str(eyrs[y])+" annual mean tas")
        elif season=="jja":
            plt.title("G6sulfur-G6solar, "+str(syrs[y])+"-"+str(eyrs[y])+" JJA mean tas")
        elif season=="djf":
            plt.title("G6sulfur-G6solar, "+str(syrs[y])+"-"+str(eyrs[y])+" DJF mean tas")
        cbar_axes = plt.gcf().add_axes([0.11, 0.1, 0.8, 0.05])
        cbar = plt.colorbar(cplot, cbar_axes, orientation="horizontal", extend="both", label="K")
        
        if season=="all":
            plt.savefig("/home/users/eunicelo/plots/CMIP6Hackathon/G6sulfur-G6solar_"+str(syrs[y])+"-"+str(eyrs[y])+"_annual_mean_tas.png")
        elif season=="jja":
            plt.savefig("/home/users/eunicelo/plots/CMIP6Hackathon/G6sulfur-G6solar_"+str(syrs[y])+"-"+str(eyrs[y])+"_jja_mean_tas.png")
        elif season=="djf":
            plt.savefig("/home/users/eunicelo/plots/CMIP6Hackathon/G6sulfur-G6solar_"+str(syrs[y])+"-"+str(eyrs[y])+"_djf_mean_tas.png")

        print("Saved graph!")
        #plt.show()
    
