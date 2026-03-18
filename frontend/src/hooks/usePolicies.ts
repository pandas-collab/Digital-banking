import { useQuery } from "./useQuery";
import { policyApi, Policy } from "../api/policyApi";

export function usePolicy(id: number) {
  return useQuery<Policy>(["policy", id], () => policyApi.getPolicy(id));
}
