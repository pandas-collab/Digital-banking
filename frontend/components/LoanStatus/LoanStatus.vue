<template>
  <div class="loan-status-card">
    <h3>{{ loan.loanNumber }}</h3>
    <div class="status-grid">
      <div class="status-item">
        <span class="label">Remaining Balance:</span>
        <span class="value">${{ loan.remainingBalance.toFixed(2) }}</span>
      </div>
      <div class="status-item">
        <span class="label">Monthly Payment:</span>
        <span class="value">${{ loan.monthlyPayment.toFixed(2) }}</span>
      </div>
      <div class="status-item">
        <span class="label">Interest Rate:</span>
        <span class="value">{{ loan.interestRate }}%</span>
      </div>
      <div class="status-item">
        <span class="label">Status:</span>
        <span class="value status-badge" :class="loan.status">{{ loan.status }}</span>
      </div>
    </div>
    <div class="buttons">
      <button @click="$emit('make-payment')" class="btn-primary">Make Payment</button>
      <button @click="$emit('view-details')" class="btn-secondary">View Details</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoanStatus',
  props: {
    loan: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.loan-status-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 10px 0;
  background: white;
}

.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 15px 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
}

.label {
  font-weight: bold;
  color: #666;
}

.value {
  font-weight: 500;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  text-transform: uppercase;
}

.status-badge.active {
  background: #4CAF50;
  color: white;
}

.status-badge.paid {
  background: #2196F3;
  color: white;
}

.buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn-primary, .btn-secondary {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style>
