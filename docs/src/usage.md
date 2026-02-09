
### Usage

While the library attempts to catch all read and write operations performed by the python script, some unsupported libraries might not be visible. To this end, the user can call the `log_input` and `log_output` directives after the `start_run`, to manually flag files as relevant to the execution. 

```python
import yprov4dv
yprov4dv.start_run()
# To track a file as input
yprov4dv.log_input(path_to_untracked_file)

# To track a file as output
yprov4dv.log_output(path_to_untracked_file)
```

The behaviour of yProv4DV can be changed passing parameters to the `start_run` function. 
All the parameters for the `start_run` function are listed below: 

- `provenance_directory`: (str) changes where the inputs, outputs and code directory are stored; 
- `prefix`: (str) changes the prefix given to fields in the provenance document; 
- `run_name`: (str) changes the run name inside the provenance file; 
- `create_json_file`: (`True` or `False`) whether the json file is created or not; 
- `create_dot_file`: (`True` or `False`) whether the dot file is created or not, cannot be `True` if `YPROV4DV_CREATE_JSON_FILE` is `False`; 
- `create_svg_file`: (`True` or `False`) whether the svg file is created or not, cannot be `True` if `YPROV4DV_CREATE_JSON_FILE` or `YPROV4DV_CREATE_DOT_FILE` are `False`; 
- `create_rocrate`: (`True` or `False`) whether the ro-crate zip is created or not; 
- `default_namespace`: (str) changes the default namespace inside the provenance file
- `save_input_files_full`: (str) decides whether input files are saved in full
- `save_input_files_subset`: (str) decides whether inputs are saved as a subset (only the plotted data)
- `skip_files_larger_than`: (int) In Mb, files larger than the threshold will not be copied;
- `verbose`: (`True` or `False`), 



# Current Compatibilities

Currently, the yProv4DV library is able to track input files which are opened by the following libraries: 
 - [pandas](https://pandas.pydata.org/) (read_csv, read_parquet, read_excel, read_json)
 - [xarray](https://docs.xarray.dev/en/stable/index.html) (open_dataset, open_mfdataset)
 - [geopandas](https://geopandas.org/en/stable/getting_started/introduction.html) (read_file)
 - [numpy](https://numpy.org/) (load)
 - [torch](https://pytorch.org/) (load)
 - [rasterio](https://rasterio.readthedocs.io/en/latest/index.html) (open)
 - As well as the standard python calls (such as open())

Additionally, if data is plotted using: 
 - [matplotlib](https://matplotlib.org/) (plot, bar, ...)
 - [seaborn](https://seaborn.pydata.org/) (scatterplot, lineplot, barplot, histplot, boxplot)
Then the subset of data used only for visualization can be saved in an isolated file (by setting the `save_input_files_subset` option to `True`). 

Any type of output files generated during the execution of the program will also be logged, indipendently of file type. 


<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="examples.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>
