import React, { useState, useEffect } from 'react';
import insuranceService from '../../services/insuranceService';

const InsurancePurchaseForm = () => {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [userPolicies, setUserPolicies] = useState([]);

  useState(() => {
    loadProducts();
    loadUserPolicies();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await insuranceService.getProducts();
      setProducts(data);
    } catch (err) {
      setError('Failed to load insurance products');
    }
  };

  const loadUserPolicies = async () => {
    try {
      const policies = await insuranceService.getUserPolicies();
      setUserPolicies(policies);
    } catch (err) {
      console.error('Failed to load user policies:', err);
    }
  };

  const handlePurchase = async () => {
    if (!selectedProduct) {
      setError('Please select an insurance product');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await insuranceService.purchasePolicy(selectedProduct.product_code);
      setSuccess(`Successfully purchased ${result.policy.product.name}! Policy #: ${result.policy.policy_number}`);
      setSelectedProduct(null);
      await loadUserPolicies();
    } catch (err) {
      setError(err.message || 'Failed to purchase policy');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Purchase Insurance</h1>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
          <p className="text-green-700">{success}</p>
        </div>
      )}

      <div className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Available Plans</h2>
        <div className="space-y-4">
          {products.map((product) => (
            <div
              key={product.product_code}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedProduct?.product_code === product.product_code
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
              onClick={() => setSelectedProduct(product)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-lg">{product.name}</h3>
                  <p className="text-gray-600 text-sm">{product.description}</p>
                  <div className="mt-2 space-y-1">
                    <p className="text-sm">Monthly: ${product.premium}</p>
                    <p className="text-sm">Coverage: ${product.coverage_amount.toLocaleString()}</p>
                    <p className="text-sm">Deductible: ${product.deductible}</p>
                  </div>
                </div>
                <div className="ml-4">
                  <input
                    type="radio"
                    name="product"
                    checked={selectedProduct?.product_code === product.product_code}
                    onChange={() => setSelectedProduct(product)}
                    className="w-5 h-5 text-blue-600"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={handlePurchase}
          disabled={loading || !selectedProduct}
          className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-700 transition"
        >
          {loading ? 'Processing...' : 'Purchase Selected Policy'}
        </button>
      </div>

      {userPolicies.length > 0 && (
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-4">Your Active Policies</h3>
          <div className="space-y-3">
            {userPolicies.map((policy) => (
              <div key={policy.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <h4 className="font-medium">{policy.product.name}</h4>
                <p className="text-sm text-gray-600">Policy #: {policy.policy_number}</p>
                <p className="text-sm text-gray-600">Coverage: ${policy.coverage_amount.toLocaleString()}</p>
                <p className="text-sm text-gray-600">Expires: {new Date(policy.end_date).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InsurancePurchaseForm;
