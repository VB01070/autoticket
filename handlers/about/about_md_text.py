from src.app_state import AppState

app_state = AppState()

about_md_text = f"""
### **GOST Admin Shortcut**
Application build by the Global Offensive Security Team of Randstad.

- *Current Version: {app_state.app_version}*
- *[Python 3.13](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)*
- *[Flet 0.28.3](https://flet.dev)*

### **To Do**

- [x]  Ai generate Management summary (from where to load the vulnerabilities? it would be easy probably to fetch them directly from the dashboard.)
- [ ]  Publish migrate vulnerability, delete the migrated vulnerability from the market
- [ ]  List of the most used Asset form GIS (need assistance from the team)
- [ ]  Move presentation and report to drive
- [x] CVSS 4.0 for the vulnerabilities. this should reflect the severity
- [ ] Improve error handling client side


### **BUGS**

- [ ]  The Migrate page does not reload properly
- [x]  Some error when reset button is pushed. Caused by the Update icon that was not yet load in the page when it was called.

### **Problem**

- [ ]  The Desktop auth from google do not allow the application to access Drive. We need to authorize it. So load note from drive and move the report to drive is out of the book for the moment.

### **Ideas**

- [ ]  Logs the event

"""