import React, { useState } from 'react';
import { Form, Input, Select, Button, Card, InputNumber, DatePicker, message } from 'antd';
import { useAuth } from '../../hooks/useAuth';
import { loanService } from '../../services/loanService';

const { Option } = Select;

interface LoanApplicationFormProps {
  onSuccess?: () => void;
}

interface FormValues {
  amount: number;
  term_months: number;
  purpose: string;
  annual_income: number;
  employment_status: string;
  employer_name?: string;
  employment_length?: string;
}

export const LoanApplicationForm: React.FC<LoanApplicationFormProps> = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const handleSubmit = async (values: FormValues) => {
    try {
      setLoading(true);
      await loanService.createApplication({
        amount: values.amount,
        term_months: values.term_months,
        purpose: values.purpose,
        annual_income: values.annual_income,
        employment_status: values.employment_status
      });
      message.success('Loan application submitted successfully!');
      form.resetFields();
      onSuccess?.();
    } catch (error) {
      message.error('Failed to submit application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Apply for a Loan">
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{ term_months: 24 }}
      >
        <Form.Item
          label="Loan Amount"
          name="amount"
          rules={[{ required: true, message: 'Please enter loan amount' }]}
        >
          <InputNumber
            style={{ width: '100%' }}
            formatter={(value) => `$ ${value}`}
            parser={(value) => value?.replace(/\$\s?|(,*)/g, '')}
            min={1000}
            max={50000}
          />
        </Form.Item>

        <Form.Item
          label="Loan Term"
          name="term_months"
          rules={[{ required: true, message: 'Please select loan term' }]}
        >
          <Select>
            <Option value={12}>1 year</Option>
            <Option value={24}>2 years</Option>
            <Option value={36}>3 years</Option>
            <Option value={48}>4 years</Option>
            <Option value={60}>5 years</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Purpose"
          name="purpose"
          rules={[{ required: true, message: 'Please state loan purpose' }]}
        >
          <Select placeholder="Select loan purpose">
            <Option value="debt_consolidation">Debt Consolidation</Option>
            <Option value="home_improvement">Home Improvement</Option>
            <Option value="medical">Medical Expenses</Option>
            <Option value="education">Education</Option>
            <Option value="auto">Auto Purchase</Option>
            <Option value="small_business">Small Business</Option>
            <Option value="other">Other</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Annual Income"
          name="annual_income"
          rules={[{ required: true, message: 'Please enter annual income' }]}
        >
          <InputNumber
            style={{ width: '100%' }}
            formatter={(value) => `$ ${value}`}
            parser={(value) => value?.replace(/\$\s?|(,*)/g, '')}
            min={0}
          />
        </Form.Item>

        <Form.Item
          label="Employment Status"
          name="employment_status"
          rules={[{ required: true, message: 'Please select employment status' }]}
        >
          <Select placeholder="Select employment status">
            <Option value="full_time">Full-time Employment</Option>
            <Option value="part_time">Part-time Employment</Option>
            <Option value="self_employed">Self-employed</Option>
            <Option value="unemployed">Unemployed</Option>
            <Option value="retired">Retired</Option>
          </Select>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Submit Application
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};
