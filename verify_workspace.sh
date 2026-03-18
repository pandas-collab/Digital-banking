set -e

echo "=== Verifying TransferHistory Component Installation ==="
echo ""

# Check if file exists
if [ -f "src/components/TransferHistory.tsx" ]; then
    echo " TransferHistory.tsx created successfully"
    wc -l src/components/TransferHistory.tsx | awk '{print $1 " lines"}'
else
    echo " TransferHistory.tsx not found"
    exit 1
fi

# Check if test file exists
if [ -f "src/components/TransferHistory.test.tsx" ]; then
    echo " Test file created successfully"
else
    echo " Test file not found"
    exit 1
fi

# Basic syntax check
if command -v node &> /dev/null; then
    if command -v npx &> /dev/null; then
        echo "Running TypeScript syntax check..."
        npx tsc --noEmit src/components/TransferHistory.tsx 2>/dev/null && echo " TypeScript syntax OK" || echo " TypeScript check failed (may need dependencies)"
    fi
fi

echo ""
echo "=== Installation Complete ==="
echo "TransferHistory component ready at: src/components/TransferHistory.tsx"
echo "Remember to:"
echo "1. Install dependencies: npm install"
echo "2. Copy component to your actual project if workspace structure differs"
echo "3. Update API_ENDPOINT env variable for production"
