from qvgdm.server import app

DEBUG = False
app.run(debug=DEBUG, dev_tools_ui=DEBUG, dev_tools_hot_reload=DEBUG)
