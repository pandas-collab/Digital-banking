import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

const TransferList = () => {
  const { data } = useQuery({ queryKey: ['transfers'], queryFn: () => api.transfers.list() })
  return (
    <div>
      <h3>History</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
export default TransferList
