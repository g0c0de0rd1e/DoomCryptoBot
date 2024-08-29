echo "Activating virtual environment"
.\venv\Scripts\Activate
echo "Uninstalling all libraries"
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y
echo "All libraries uninstalled"
echo "Deactivating virtual environment"
deactivate
echo "Virtual environment deactivated"
pause
