@echo off
echo ============================================
echo   Building Chicken Kitchen HR Forms App
echo ============================================
echo.

cd /d "%~dp0"

python -m PyInstaller --noconfirm --onefile --windowed ^
    --name "CK_HR_Forms" ^
    --hidden-import "pypdf" ^
    --hidden-import "pypdf._reader" ^
    --hidden-import "pypdf._writer" ^
    --hidden-import "pypdf._page" ^
    --hidden-import "PyPDF2" ^
    --hidden-import "reportlab" ^
    --hidden-import "reportlab.pdfgen" ^
    --hidden-import "reportlab.pdfgen.canvas" ^
    --hidden-import "reportlab.lib.colors" ^
    --hidden-import "reportlab.lib.pagesizes" ^
    --hidden-import "reportlab.lib.units" ^
    --hidden-import "reportlab.rl_config" ^
    --hidden-import "fitz" ^
    --hidden-import "pymupdf" ^
    --hidden-import "PIL" ^
    --hidden-import "PIL.Image" ^
    --hidden-import "PIL.ImageTk" ^
    --add-data "app\translations.py;." ^
    --add-data "app\pdf_overlay.py;." ^
    --add-data "app\field_help.py;." ^
    --add-data "app\us_data.py;." ^
    --add-data "app\templates\DDAuth_template.pdf;templates" ^
    --add-data "app\templates\EmployeeApp_template.pdf;templates" ^
    --add-data "app\templates\I9_template.pdf;templates" ^
    --add-data "app\templates\PayrollAction_template.pdf;templates" ^
    --add-data "app\templates\W4_template.pdf;templates" ^
    "app\main.py"

echo.
echo ============================================
echo   Build complete!
echo   EXE location: dist\CK_HR_Forms.exe
echo ============================================
pause
