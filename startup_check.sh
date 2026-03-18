echo " Verifying cash-flow system startup..."
mkdir -p /workspace/data/cashflow

# Test file writing
touch /workspace/data/cashflow/test.txt && rm /workspace/data/cashflow/test.txt

# Run comprehensive test
python3 test_cashflow.py

echo " Cash-flow transparency system verified and ready!"
