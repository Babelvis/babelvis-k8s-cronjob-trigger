# Babelvis kubernetes cronjob trigger

Simple application to trigger Cronjobs in Kubernetes as Job

## Techniques used

Brief description of techniques used for this application

### Qt Widgets Designer

To quickly put together a GUI.

- [link](https://doc.qt.io/qtcreator/)
- [download](https://download.qt.io/official_releases/qtcreator/latest/)

### Python

Python with the kubernetes module

### PyInstaller

So we can create a single executable for Windows/Linux/Mac

## Development

### Directories uses

- app/assets: For assets like icons
- app/desktopfiles: Desktopfiles for Linux packages
- app/generated: Generated python files from the *.ui files
- app/interaction: python files with screen interaction, inherits a generated window
- app/ui: window description, files created with Qt Widgets Designer

### Compile / Run

Windows only (LongPathsEnabled has to be enabled, one time setup):

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

```bash
# install the packages through your linux distribution or use pip (windows/mac)
cd app
pip install -r requirements.txt
```

After making GUI changes in Qt Designer, you can easily generate the python code with:

```bash
pyuic6  app/ui/main.ui -o app/generated/main.py
```

Run the application with:

```bash
python app/app.py
```
