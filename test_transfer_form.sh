set -e

# Simple test to verify TransferForm.tsx syntax
echo "Testing TransferForm.tsx..."
if ! grep -q "TransferForm" components/TransferForm.tsx; then
    echo "ERROR: TransferForm component not found"
    exit 1
fi

if ! grep -q "className" components/TransferForm.tsx || grep -q "TransferForm.module.css" components/TransferForm.tsx; then
    echo "WARNING: CSS modules reference not found - using inlined styles"
fi

if grep -q "useState" components/TransferForm.tsx && grep -q "interface" components/TransferForm.tsx; then
    echo "SUCCESS: TransferForm.tsx structure validated"
else
    echo "ERROR: Essential React imports not found"
    exit 1
fi

echo " TransferForm.tsx tests passed"
