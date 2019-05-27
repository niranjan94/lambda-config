
`lambda-config` makes it easy to load lambda configuration stored on SSM parameter store.

### Installation

`lambda-config` is listed on [PyPI](https://pypi.org/project/lambda-config/) and can be installed with pip:

```bash
pip install lambda-config
```

### Example

1. Add the config as either json/yaml/ini to a path in the SSM parameter store
2. Add the following env variables to the lambda
    1. `SSM_PARAMETER_PATH` - the path to parameter
    2. `SSM_CONFIG_TYPE` - `json`/`yaml`/`ini`
3. Import and use the config

   ```python
   from lambda_config import config
   
   # now you can use the config. config is a dictionary
   ```

### License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

```
MIT License

Copyright (c) 2019 Niranjan Rajendran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

