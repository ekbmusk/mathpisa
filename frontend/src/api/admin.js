import client from './client'

export const adminAPI = {
  getStats: () => client.get('/users/admin/stats'),
  getUserList: (params) => client.get('/users/admin/list', { params }),
  getUserActivity: (userId) => client.get(`/users/admin/${userId}/activity`),
  exportPrePost: (params = {}) =>
    client.get('/users/admin/export-pre-post', { params, responseType: 'blob' }),
}
