# RESTful API module

## `app` sub-module folder structure

<!-- TODO: Write a short description for all the modules and sub-modules in this way -->

```bash
.
│   ├── apis                            # High level layer (for example data layer apis). All the sub-module for data layer will be listed here as folder.
│   │   ├── api_a                       # This will be a sub-module in the data layer (For example this can be data layer --> validation sub-module)
│   │   │   ├── __init__.py             # All the end points of data-layer/validation will be aggregated in this file/sub-module
│   │   │   ├── mainmod.py              # All the functions can be listed here in this function file which will be used in the main module. Note there can be multiple files of this type. Also settings, config and utils can of this type,
│   │   │   └── submod.py               # submodule of api_a package
│   │   └── api_b                       # api_b package
│   │       ├── __init__.py             # empty init file to make the api_b folder a package
│   │       ├── mainmod.py              # main module of api_b package
│   │       └── submod.py               # submodule of api_b package
│   ├── core                            # this is where the configs live
│   │   ├── auth.py                     # authentication with OAuth2
│   │   ├── config.py                   # sample config file
│   │   └── __init__.py                 # empty init file to make the config folder a package
│   ├── __init__.py                     # empty init file to make the app folder a package
│   ├── main.py                         # main file where the fastAPI() class is called
│   ├── routes                          # this is where all the routes live
│   │   └── views.py                    # file containing the endpoints of api_a and api_b
│   └── tests                           # test package
│       ├── __init__.py                 # empty init file to make the tests folder a package
│       ├── test_api.py                 # functional testing the API responses
│       └── test_functions.py           # unit testing the underlying functions
```
