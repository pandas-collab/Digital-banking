import { create } from 'zustand'
type State = { role: string|null, login: (role:string)=>void }
const useAuth = create<State>(set=>({ role: null, login: role=>set({role}) }))
export default useAuth
