
const KEYS = {
  ATTACK_LOGS: 'padp_attack_logs',
  DEFENSE_LOGS: 'padp_defense_logs',
  TARGETS: 'padp_targets',
  ALGORITHMS: 'padp_algorithms',
  AI_MODELS: 'padp_ai_models',
  ATTACK_CONFIG: 'padp_attack_config',
  DEFENSE_CONFIG: 'padp_defense_config',
  USERS: 'padp_users',
  ROLE_PERMISSIONS: 'padp_role_permissions'
}

export const Storage = {
  // Get all data for a key
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (e) {
      console.error(`Error reading ${key} from storage`, e)
      return defaultValue
    }
  },

  // Set data for a key
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value))
      // Dispatch event for local updates
      window.dispatchEvent(new CustomEvent('local-storage-update', { detail: { key, value } }))
    } catch (e) {
      console.error(`Error writing ${key} to storage`, e)
    }
  },

  // Add item to a list stored at key
  add(key, item) {
    const list = this.get(key, [])
    list.unshift(item) // Add to beginning
    this.set(key, list)
  },

  // Update an item in a list by id
  update(key, id, updates) {
    const list = this.get(key, [])
    const index = list.findIndex(i => i.id === id)
    if (index !== -1) {
      list[index] = { ...list[index], ...updates }
      this.set(key, list)
    }
  },
  
  // Clear all platform data
  clearAll() {
    Object.values(KEYS).forEach(k => localStorage.removeItem(k))
  },

  KEYS
}

