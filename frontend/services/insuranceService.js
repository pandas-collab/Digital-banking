const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class InsuranceService {
  async getProducts() {
    try {
      const response = await fetch(`${API_BASE_URL}/insurance/products`);
      if (!response.ok) throw new Error('Failed to fetch products');
      const data = await response.json();
      return data.products;
    } catch (error) {
      console.error('Error fetching products:', error);
      return [];
    }
  }

  async purchasePolicy(productCode, userId = 'test-user-123') {
    try {
      const response = await fetch(`${API_BASE_URL}/insurance/purchase`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': userId,
        },
        body: JSON.stringify({
          product_code: productCode,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to purchase policy');
      }

      return await response.json();
    } catch (error) {
      console.error('Error purchasing policy:', error);
      throw error;
    }
  }

  async getUserPolicies(userId = 'test-user-123') {
    try {
      const response = await fetch(`${API_BASE_URL}/insurance/policies/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch policies');
      const data = await response.json();
      return data.policies || [];
    } catch (error) {
      console.error('Error fetching policies:', error);
      return [];
    }
  }
}

export default new InsuranceService();
