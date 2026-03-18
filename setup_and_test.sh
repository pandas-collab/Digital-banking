cd /workspace

# Install dependencies
pip install -r requirements.txt

# Make test executable
chmod +x test_deduction.py

# Create logs directory
mkdir -p logs

# Run syntax validation
python -c "import ast; ast.parse(open('main.py').read())" && echo " main.py syntax valid"
python -c "import ast; ast.parse(open('test_deduction.py').read())" && echo " test_deduction.py syntax valid"

# Basic functionality test
python test_deduction.py

echo "Setup complete. Run 'python main.py' to start the scheduled task."
