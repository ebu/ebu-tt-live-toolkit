"""
This subpackage is meant to contain configuration directives of validation and and normalization as well as defaults.
The current plan is to use configobj but there may be a better tool. Ultimately there is one goal there. Avoid any
runtime errors because of a broken configuration value being used at a later stage in execution at which point due to
not having been validated would cause the system to break. Validation and normalization eliminates this problem
completely. This means At startup time we can be sure that all of the configuration values match the requirements
of successful operation.

TODO: implement this when we have more understanding of the parameters one would want to control.
"""