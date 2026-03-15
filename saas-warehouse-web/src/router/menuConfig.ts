export interface MenuItem {
  path: string
  icon: string
  title: string
  meta: {
    roles: string[]
  }
  children?: MenuItem[]
}

export const menuConfig: MenuItem[] = [
  {
    path: '/dashboard',
    icon: 'DataAnalysis',
    title: '首页',
    meta: { roles: ['admin', 'dispatcher', 'manager'] }
  },
  {
    path: '/orders',
    icon: 'Document',
    title: '订单管理',
    meta: { roles: ['admin', 'dispatcher', 'manager'] },
    children: [
      { path: '/orders/list', icon: 'Document', title: '订单列表', meta: { roles: ['admin', 'dispatcher', 'manager'] } },
      { path: '/orders/create', icon: 'Plus', title: '新建订单', meta: { roles: ['admin', 'dispatcher'] } },
      { path: '/orders/import', icon: 'Upload', title: '批量导入', meta: { roles: ['admin', 'dispatcher'] } }
    ]
  },
  {
    path: '/dispatch',
    icon: 'Position',
    title: '调度排单',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/warehouse',
    icon: 'Box',
    title: '仓储管理',
    meta: { roles: ['admin', 'dispatcher'] },
    children: [
      { path: '/warehouse/inventory', icon: 'Goods', title: '库存管理', meta: { roles: ['admin', 'dispatcher'] } },
      { path: '/warehouse/unload', icon: 'Box', title: '卸货管理', meta: { roles: ['admin', 'dispatcher'] } }
    ]
  },
  {
    path: '/delivery',
    icon: 'Van',
    title: '配送管理',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/install',
    icon: 'Tools',
    title: '安装管理',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/fees',
    icon: 'Money',
    title: '费用管理',
    meta: { roles: ['admin', 'manager'] }
  },
  {
    path: '/reports',
    icon: 'TrendCharts',
    title: '报表分析',
    meta: { roles: ['admin', 'manager'] },
    children: [
      { path: '/reports/orders', icon: 'Document', title: '订单报表', meta: { roles: ['admin', 'manager'] } },
      { path: '/reports/workers', icon: 'User', title: '人员报表', meta: { roles: ['admin', 'manager'] } },
      { path: '/reports/fees', icon: 'Money', title: '费用报表', meta: { roles: ['admin', 'manager'] } }
    ]
  },
  {
    path: '/users',
    icon: 'User',
    title: '用户管理',
    meta: { roles: ['admin'] }
  },
  {
    path: '/settings',
    icon: 'Setting',
    title: '系统设置',
    meta: { roles: ['admin'] }
  }
]
