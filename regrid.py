# regrid_data.py
import xarray as xr
import xesmf as xe
import dask

def regrid_data(source_path, target_path, output_path, chunks=None):
    """
    Regrids data from a source file to a target grid and saves the result.

    Parameters:
    - source_path (str): Path to the source NetCDF file (e.g., ERA5 data).
    - target_path (str): Path to the target grid NetCDF file (e.g., CARRA grid).
    - output_path (str): Path to save the regridded output NetCDF file.
    - chunks (dict, optional): Dictionary defining Dask chunk sizes, e.g., {'time': 40, 'latitude': 70, 'longitude': 70}.
                                Set to None to disable Dask chunking.
    """
    # Load source and target datasets, with optional Dask chunking
    print("Loading datasets...")
    if chunks:
        era5_data = xr.open_dataset(source_path, chunks=chunks)
    else:
        era5_data = xr.open_dataset(source_path)
    
    target_grid = xr.open_dataset(target_path)

    # Define the regridding function with bilinear interpolation
    print("Defining regridding function...")
    regridder = xe.Regridder(era5_data, target_grid, method="bilinear", periodic=False)

    # Perform the regridding
    print("Performing regridding...")
    output = regridder(era5_data)

    # Save the result to a NetCDF file, allowing Dask to handle writing in chunks
    print(f"Saving regridded data to {output_path}...")
    output.to_netcdf(output_path, compute=True)
    print("Regridding complete!")

if __name__ == "__main__":
    # Define file paths
    source_path = "ERA5_wind_speed_1991_2000.nc"
    target_path = "CARRA_East_grid.nc"
    output_path = "regriddedERA5_wind_speed_1991_2000.nc"
    
    # Define Dask chunks for memory-efficient processing, set to None to disable
    chunks = {"time": 40, "latitude": 70, "longitude": 70}

    # Run the regrid function
    regrid_data(source_path, target_path, output_path, chunks)
