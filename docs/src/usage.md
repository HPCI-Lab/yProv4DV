
### Usage

While the library attempts to catch all read and write operations performed by the python script, some unsupported libraries might not be visible. To this end, the user can call the `log_input` and `log_output` directives, to manually flag files as relevant to the execution. 

```python
import yprov4dv
# To track a file as input
yprov4dv.log_input(path_to_untracked_file)

# To track a file as output
yprov4dv.log_output(path_to_untracked_file)
```


<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="examples.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>
