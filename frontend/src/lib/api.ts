import z from 'zod'
import { Decimal } from 'decimal.js'

const api = {
  transfers: {
    create: async (body: {from_account_id:number,to_account_id:number,amount:number|string}) => {
      const res = await fetch('/api/transfers', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)})
      return res.json()
    },
    list: async () => {
      const res = await fetch('/api/transfers')
      return res.json()
    }
  }
}
export default api
