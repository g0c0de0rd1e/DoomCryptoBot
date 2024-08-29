echo "Creating virtual environment"
python -m venv venv
echo "Virtual environment created"
.\venv\Scripts\activate
echo "Installing all libraries"
pip install -r requirements.txt 
echo "All libraries installed"
pause