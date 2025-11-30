import pkgutil
import importlib

#Gets every .py file inside app/tools/
#Imports them automatically

# Auto-discover and import all modules in this package
for module_info in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_info.name}")

###################################
# if you don't do above, you have to import all files like following.
# import app.tools.math_tools
# import app.tools.weather_tools
# import app.tools.bing_tools
# import app.tools.google_tools
###################################
