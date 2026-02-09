# yProv4DV

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

yProv4DV (Data Visualization) is a python utility which allows for packaging of code, inputs and outputs of data visualization scripts. Once integrated, it will produce a zip file which includes all information necessary for reproducibility of the current script, including a copy of the files used. This library is part of the [yProv](https://github.com/HPCI-Lab/yProv) framework, which means it can also produce W3C-prov compliant files useful for interpretability and reproducibility.

### Features

The library allows for the automatic collection of inputs, outputs and source code used during the programs execution. 
If a file is too large, the user can specify to save only the information necessary to the creation of the chart. 
Additionally, a provenance graph of the program can also be created, along with its visual representation and the ro-create package for the script's reproducibility. 

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
