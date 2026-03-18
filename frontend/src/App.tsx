import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import TransferForm from './components/transfer-form'
import TransferList from './components/transfer-list'
import LoanDashboard from './components/loan-dashboard'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/transfers" element={<><TransferForm /><TransferList /></>} />
        <Route path="/loans" element={<LoanDashboard />} />
      </Routes>
    </Router>
  )
}
export default App
