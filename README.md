# GOST Admin Shortcut

A Python application built with [Flet](https://flet.dev).

---

## Requirements

* **[Python 3.13](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)**

---

## Installation (PowerShell)

If your system is already configured correctly, install and run the app with:

```powershell
git clone https://github.com/VB01070/autoticket.git
cd autoticket
python -m venv env
.\env\Scripts\activate
pip install -r .\requirements.txt --no-cache-dir
```

To start the application:

```powershell
$env:PYTHONPATH="."
flet run src/main.py
```

---

## Common Problems & Fixes

### 1. **WeasyPrint Error on Windows**

**Error:**

```
OSError: cannot load library 'libgobject-2.0-0': error 0x7e
```

This means WeasyPrint can't find GTK+ libraries.

**Fix:**

1. **Install [MSYS2](https://www.msys2.org/)**

2. **Update system packages:**

   ```bash
   pacman -Syu
   ```

3. **Install GTK3 libraries:**

   ```bash
   pacman -Sy mingw-w64-x86_64-gtk3
   ```

4. **Add this to your system PATH:**

   ```
   C:\msys64\mingw64\bin
   ```

5. **Restart PowerShell** and reinstall requirements:

   ```powershell
   pip install -r .\requirements.txt --no-cache-dir
   ```

---

### 2. **CFFI / Compiler Error**

This happens when `pip` tries to build a C extension like `cffi`, but no compiler is found.

**Fix:**

1. **Install Microsoft C++ Build Tools:**

   * [Download here](https://aka.ms/vs/17/release/vs_BuildTools.exe)
   * Select **Desktop development with C++** during setup

2. **Reboot after install**

3. **Verify compiler is available (optional):**

   ```powershell
   & "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\<version>\bin\Hostx64\x64\cl.exe"
   ```

4. **Open *Developer PowerShell for VS 2022***

   > **Important:** The next command must be run from this PowerShell, not a regular one.

   ```powershell
   rustup target add i686-pc-windows-msvc
   ```

5. **Then clone and set up the app again:**

   ```powershell
   git clone https://github.com/VB01070/autoticket.git
   cd autoticket
   python -m venv env
   .\env\Scripts\activate
   pip install -r .\requirements.txt --no-cache-dir
   ```

   Start the application:

   ```powershell
   $env:PYTHONPATH="."
   flet run src/main.py
   ```

---

Once everything is installed correctly, you can run the app from any normal PowerShell terminal.

