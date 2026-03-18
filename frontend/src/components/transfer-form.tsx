import { useState } from 'react'
import api from '../lib/api'

const TransferForm = () => {
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')
  const [amount, setAmount] = useState('')
  const create = async () => {
    await api.transfers.create({ from_account_id: Number(from), to_account_id: Number(to), amount })
  }
  return (
    <div>
      <h2>Transfer</h2>
      <input placeholder="from" value={from} onChange={e=>setFrom(e.target.value)} />
      <input placeholder="to" value={to} onChange={e=>setTo(e.target.value)} />
      <input placeholder="amount" value={amount} onChange={e=>setAmount(e.target.value)} />
      <button onClick={create}>Send</button>
    </div>
  )
}
export default TransferForm
