import { apiFetch } from './client'

export function getHealth() {
  return apiFetch('/health/')
}