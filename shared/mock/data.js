
import { Storage } from '../utils/storage'

// Initial Mock Data
const INITIAL_TARGETS = [
  { id: 1, name: 'Admin_User', algorithm: 'SM4', version: 'V1.0', defenseLevel: 'High', status: 'secure', history: 0, isVulnerable: true, vulnerabilities: ['SM4算法版本过低'] },
  { id: 2, name: 'Finance_System', algorithm: 'AES-256', version: 'V2.1', defenseLevel: 'Medium', status: 'secure', history: 2, isVulnerable: false, vulnerabilities: [] },
  { id: 3, name: 'Guest_Wifi', algorithm: 'MD5', version: 'Legacy', defenseLevel: 'Low', status: 'vulnerable', history: 5, isVulnerable: true, vulnerabilities: ['算法已废弃', '密码强度不足'] },
  { id: 4, name: 'HR_Portal', algorithm: 'RSA-1024', version: 'V1.0', defenseLevel: 'Medium', status: 'secure', history: 1, isVulnerable: true, vulnerabilities: ['密钥长度不足'] }
]

const INITIAL_ALGORITHMS = [
  { id: 1, name: 'SM4', type: 'Symmetric', version: 'V1.0', status: 'vulnerable', desc: '国密分组密码算法', fix: '升级至V2.0并开启动态密钥' },
  { id: 2, name: 'AES', type: 'Symmetric', version: 'V2.1', status: 'secure', desc: '高级加密标准', fix: '' },
  { id: 3, name: 'RSA', type: 'Asymmetric', version: '1024-bit', status: 'vulnerable', desc: '公钥加密算法', fix: '升级密钥长度至2048位以上' },
  { id: 4, name: 'MD5', type: 'Hash', version: 'Legacy', status: 'vulnerable', desc: '消息摘要算法', fix: '建议替换为SM3或SHA-256' },
  { id: 5, name: 'SM3', type: 'Hash', version: 'V1.1', status: 'secure', desc: '国密杂凑算法', fix: '' }
]

const INITIAL_USERS = [
  { id: 1, username: 'admin', role: 'admin', status: 'active', department: '安全部', lastLogin: '2024-01-04 09:30:00' },
  { id: 2, username: 'user1', role: 'user', status: 'active', department: '研发部', lastLogin: '2024-01-03 14:20:00' },
  { id: 3, username: 'audit', role: 'auditor', status: 'inactive', department: '审计部', lastLogin: '2023-12-25 10:00:00' }
]

const INITIAL_ROLE_PERMISSIONS = {
  admin: [
    'scenario_edit',
    'attack_simulate',
    'defense_simulate',
    'view_reports',
    'manage_users',
    'manage_targets',
    'manage_vulnerabilities',
    'system_config'
  ],
  user: [
    'scenario_edit',
    'attack_simulate',
    'view_reports',
    'manage_targets'
  ],
  auditor: [
    'view_reports',
    'manage_vulnerabilities'
  ]
}

export const initMockData = () => {
  if (!Storage.get(Storage.KEYS.TARGETS)) {
    Storage.set(Storage.KEYS.TARGETS, INITIAL_TARGETS)
  }
  if (!Storage.get(Storage.KEYS.ALGORITHMS)) {
    Storage.set(Storage.KEYS.ALGORITHMS, INITIAL_ALGORITHMS)
  }
  if (!Storage.get(Storage.KEYS.USERS)) {
    Storage.set(Storage.KEYS.USERS, INITIAL_USERS)
  }
  const existingPerms = Storage.get(Storage.KEYS.ROLE_PERMISSIONS)
  if (!existingPerms) {
    Storage.set(Storage.KEYS.ROLE_PERMISSIONS, INITIAL_ROLE_PERMISSIONS)
  } else {
    // ensure labs_manage permission available to admin and user
    const ensure = (role) => {
      const arr = existingPerms[role] || []
      if (!arr.includes('labs_manage')) arr.push('labs_manage')
      existingPerms[role] = arr
    }
    ensure('admin')
    ensure('user')
    Storage.set(Storage.KEYS.ROLE_PERMISSIONS, existingPerms)
  }
  
  // Initialize empty logs if not present
  if (!Storage.get(Storage.KEYS.ATTACK_LOGS)) {
    Storage.set(Storage.KEYS.ATTACK_LOGS, [])
  }
  if (!Storage.get(Storage.KEYS.DEFENSE_LOGS)) {
    Storage.set(Storage.KEYS.DEFENSE_LOGS, [])
  }
  
  console.log('Mock Data Initialized')
}

