from src.app_state import AppState

app_state = AppState()

about_md_text = f"""
### **GOST Admin Shortcut**
Application build by the Global Offensive Security Team of Randstad.

- *Current Version: {app_state.app_version}*
- *[Python 3.13](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)*
- *[Flet 0.28.3](https://flet.dev)*

### **To Do**

- [ ] Move presentation and report to drive
- [ ] Improve error handling client side
- [ ] Map of the vulnerability type/GIS asset
- [ ] Improve the searchable Dropdown for vulnerability types


### **BUGS**

- 

### **Problem**

- [ ]  The Desktop auth from google do not allow the application to access Drive. We need to authorize it. So load note from drive and move the report to drive is out of the book for the moment.

### **Ideas**

- 

"""