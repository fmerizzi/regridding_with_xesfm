  # Regridding with xESMF
  
  This repository contains code for regridding weather data using xESMF, a powerful tool built on top of Xarray and ESMPy for geospatial data processing.
  
  ### Installation
  
  xESMF has several dependencies and is best installed via Conda for ease of management.
  
  1. Create and activate a new Conda environment:
     ```bash
     $ conda create -n xesmf_env
     $ conda activate xesmf_env
     ```
  
  2. Install xESMF and its core dependencies:
     ```bash
     $ conda install -c conda-forge xesmf
     ```
  
  3. To enable all xESMF features, install additional dependencies:
     ```bash
     $ conda install -c conda-forge dask netCDF4
     ```
  
  4. (Optional) For running all notebook examples, install these visualization and interface tools:
     ```bash
     $ conda install -c conda-forge matplotlib cartopy jupyterlab
     ```
  
  ### Regridding Data: Example from ERA5 to CARRA
  
  In this example, we regrid ERA5 data onto the CARRA East grid. We use `CARRA_East_grid.nc` as the target grid, which provides the necessary LLC projection information.
  
  ```python
  import xarray as xr
  import xesmf as xe
  
  # Load source and target datasets
  era5_data = xr.open_dataset("ERA5_wind_speed_subset.nc")
  target_grid = xr.open_dataset("CARRA_East_grid.nc")
  
  # Define the regridding function using bilinear interpolation
  regridder = xe.Regridder(era5_data, target_grid, method="bilinear", periodic=False)
  
  # Perform regridding
  output = regridder(era5_data)
  
  # Save the result to a NetCDF file
  output.to_netcdf("output.nc")
  ```
  
  ### Using Dask for Memory-Efficient Regridding
  
  Regridding large datasets can be memory-intensive. Dask allows for chunked, lazy computation to reduce memory usage. With careful tuning, Dask can process large datasets without overwhelming system memory, though this increases computation time.
  
  ```python
  import xarray as xr
  import xesmf as xe
  import dask
  
  # Load ERA5 data with Dask chunking for memory efficiency
  era5_data = xr.open_dataset("ERA5_wind_speed_1991_2000.nc", chunks={"time": 40, "latitude": 70, "longitude": 70})
  target_grid = xr.open_dataset("CARRA_East_grid.nc")
  
  # Define the regridding function
  regridder = xe.Regridder(era5_data, target_grid, method="bilinear", periodic=False)
  
  # Perform lazy regridding
  output = regridder(era5_data)
  
  # Save the output to a NetCDF file with chunked write, managed by Dask
  output.to_netcdf("/mnt/DATA2/regriddedERA5_wind_speed_1991_2000.nc", compute=True)
  ```
  
  This setup should now allow efficient regridding of large datasets while keeping memory usage in check.
