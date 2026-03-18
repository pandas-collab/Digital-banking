import React, { useState } from "react";
import { policyApi } from "../api/policyApi";

interface Props {
  onPurchased?: () => void;
}

export const PolicyPurchaseForm: React.FC<Props> = ({ onPurchased }) => {
  const [coverageType, setCoverageType] = useState("");
  const [coverageAmount, setCoverageAmount] = useState<number>(0);
  const [premium, setPremium] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await policyApi.purchasePolicy({ coverageType, coverageAmount, premiumMonthly: premium });
      onPurchased?.();
      setCoverageType("");
      setCoverageAmount(0);
      setPremium(0);
    } catch (err) {
      alert(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Purchase Insurance Policy</h2>
      <label>
        Coverage Type
        <input
          type="text"
          value={coverageType}
          onChange={(e) => setCoverageType(e.target.value)}
          required
        />
      </label>
      <label>
        Coverage Amount (USD)
        <input
          type="number"
          value={coverageAmount}
          onChange={(e) => setCoverageAmount(+e.target.value)}
          required
          min={0}
          step={0.01}
        />
      </label>
      <label>
        Monthly Premium (USD)
        <input
          type="number"
          value={premium}
          onChange={(e) => setPremium(+e.target.value)}
          required
          min={0}
          step={0.01}
        />
      </label>
      <button type="submit" disabled={loading}>
        {loading ? "Purchasing..." : "Purchase"}
      </button>
    </form>
  );
};
