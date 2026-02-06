# yProv4DV

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

yProv4DV (Data Visualization) is a python utility which allows for packaging of code, inputs and outputs of data visualization scripts. Once integrated, it will produce a zip file which includes all information necessary for reproducibility of the current script, including a copy of the files used. This library is part of the [yProv](https://github.com/HPCI-Lab/yProv) framework, which means it can also produce W3C-prov compliant files useful for interpretability and reproducibility.

### Features

To keep the number of yprov4dv calls to a minimum, the customization of the library behaviour can be changed using environment variables. 
All possible fields are listed below: 

- `YPROV4DV_PROVENANCE_DIRECTORY`: (str) changes where the inputs, outputs and code directory are stored; 
- `YPROV4DV_PREFIX`: (str) changes the prefix given to fields in the provenance document; 
- `YPROV4DV_RUN_NAME`: (str) changes the run name inside the provenance file; 
- `YPROV4DV_CREATE_JSON_FILE`: (`True` or `False`) whether the json file is created or not; 
- `YPROV4DV_CREATE_DOT_FILE`: (`True` or `False`) whether the dot file is created or not, cannot be `True` if `YPROV4DV_CREATE_JSON_FILE` is `False`; 
- `YPROV4DV_CREATE_SVG_FILE`: (`True` or `False`) whether the svg file is created or not, cannot be `True` if `YPROV4DV_CREATE_JSON_FILE` or `YPROV4DV_CREATE_DOT_FILE` are `False`; 
- `YPROV4DV_CREATE_RO_CRATE`: (`True` or `False`) whether the ro-crate zip is created or not; 
- `YPROV4DV_DEFAULT_NAMESPACE`: (str) changes the default namespace inside the provenance file
- `YPROV4DV_VERBOSE`: (`True` or `False`), 

For an example, run: 

```bash
python ./examples/customized.py
```


### Example

Inside the examples folder is contained an example of a simple data visualization script in python. It is already integrated with the yProv4DV library, and can be run with the prompt:

python ./examples/simple.py

This execution will create:

 - The prov directory (which is customizable) and will hold all the information for the current execution, so inputs, outputs and source code (src), all in their respective folders. Additionally, in the same directory, the library creates a set of provenance files, containing a description of the current execution (in .json, dot and svg formats).
 - prov.zip: containining all the aforementioned information in a zipped RO-Crate.


<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>
