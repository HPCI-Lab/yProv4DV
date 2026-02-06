
<table align="center">
  <tr>
    <td><img src="./assets/HPCI-Lab.png" alt="HPCI Lab Logo" width="100"></td>
    <td><h1>yProv4DA</h1></td>
  </tr>
</table>

[![Contributors](https://img.shields.io/github/contributors/HPCI-Lab/yProv4DV?style=for-the-badge)](https://github.com/HPCI-Lab/yProv4DV/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/HPCI-Lab/yProv4DV?style=for-the-badge)](https://github.com/HPCI-Lab/yProv4DV/network/members)
[![Stars](https://img.shields.io/github/stars/HPCI-Lab/yProv4DV?style=for-the-badge)](https://github.com/HPCI-Lab/yProv4DV/stargazers)
[![Issues](https://img.shields.io/github/issues/HPCI-Lab/yProv4DV?style=for-the-badge)](https://github.com/HPCI-Lab/yProv4DV/issues)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

# yProv4DV

yProv4DV (Data Visualization) is a python utility which allows for packaging of code, inputs and outputs of data visualization scripts. Once integrated, it will produce a zip file which includes all information necessary for reproducibility of the current script, including a copy of the files used. This library is part of the [yProv](https://github.com/HPCI-Lab/yProv) framework, which means it can also produce W3C-prov compliant files useful for interpretability and reproducibility. 

# Installation

```bash
pip install yprov4dv
```

# Example

Inside the `examples` folder is contained an example of a simple data visualization script in python. It is already integrated with the yProv4DV library, and can be run with the prompt: 

```bash
python ./examples/simple.py
```

This execution will create: 
- The `prov` directory (which is customizable) and will hold all the information for the current execution, so `inputs`, `outputs` and source code (`src`), all in their respective folders. Additionally, in the same directory, the library creates a set of provenance files, containing a description of the current execution (in `.json`, `dot` and `svg` formats). 
- `prov.zip`: containining all the aforementioned information in a zipped [RO-Crate](https://www.researchobject.org/ro-crate/).  

# Customization

To keep the number of yprov4dv calls to a minimum, the customization of the library behaviour can be changed using environment variables. 
All possible fields are listed below: 

- `YPROV4DS_PROVENANCE_DIRECTORY`: (str) changes where the inputs, outputs and code directory are stored; 
- `YPROV4DS_PREFIX`: (str) changes the prefix given to fields in the provenance document; 
- `YPROV4DS_RUN_NAME`: (str) changes the run name inside the provenance file; 
- `YPROV4DS_CREATE_JSON_FILE`: (`True` or `False`) whether the json file is created or not; 
- `YPROV4DS_CREATE_DOT_FILE`: (`True` or `False`) whether the dot file is created or not, cannot be `True` if `YPROV4DS_CREATE_JSON_FILE` is `False`; 
- `YPROV4DS_CREATE_SVG_FILE`: (`True` or `False`) whether the svg file is created or not, cannot be `True` if `YPROV4DS_CREATE_JSON_FILE` or `YPROV4DS_CREATE_DOT_FILE` are `False`; 
- `YPROV4DS_CREATE_RO_CRATE`: (`True` or `False`) whether the ro-crate zip is created or not; 
- `YPROV4DS_DEFAULT_NAMESPACE`: (str) changes the default namespace inside the provenance file
- `YPROV4DS_VERBOSE`: (`True` or `False`), 

For an example, run: 

```bash
python ./examples/customized.py
```
