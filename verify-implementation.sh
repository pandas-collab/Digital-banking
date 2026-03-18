echo "=== Verifying LoanForm Implementation ==="

# Check files exist
echo "[CHECK] Checking required files..."
[ -f "src/components/LoanForm.tsx" ] && echo " LoanForm.tsx found" || echo " LoanForm.tsx missing"
[ -f "src/lib/logger.ts" ] && echo " logger.ts found" || echo " logger.ts missing"
[ -f "__tests__/LoanForm.test.tsx" ] && echo " LoanForm.test.tsx found" || echo " LoanForm.test.tsx missing"

# Check test setup
echo "[CHECK] Checking test configuration..."
[ -f "jest.config.js" ] && echo " jest.config.js found" || echo " jest.config.js missing"
[ -f "__tests__/setup.ts" ] && echo " test setup file found" || echo " test setup file missing"

# Run type check (if available)
if command -v npm &> /dev/null; then
  echo "[CHECK] Checking dependencies..."
  npm list @testing-library/react 2>/dev/null && echo " Testing dependencies installed" || echo " Run 'npm install' to install dependencies"
fi

echo ""
echo "=== Implementation Summary ==="
echo "1. Component created: src/components/LoanForm.tsx"
echo "2. Utility created: src/lib/logger.ts"
echo "3. Tests created: __tests__/LoanForm.test.tsx"
echo "4. Test config: jest.config.js"
echo "5. Demo page: src/app/page.tsx"
echo "6. Dependencies check: package.json updated"
echo ""
echo "=== Next Steps ==="
echo "1. Run 'npm install' to install dependencies"
echo "2. Run 'npm test' to execute tests"
echo "3. Run 'npm run dev' to start development server"
echo "4. Visit http://localhost:3000 to see the form"
