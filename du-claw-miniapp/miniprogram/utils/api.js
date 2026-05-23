// du-claw API 工具类 - 封装所有后端请求

const app = getApp()

// 基础请求
function request(options) {
  if (app && app.request) {
    return app.request(options)
  }
  return new Promise((resolve, reject) => {
    const header = { 'Content-Type': 'application/json' }
    const token = wx.getStorageSync('token')
    if (token) header['Authorization'] = 'Bearer ' + token

    wx.request({
      url: app.globalData.baseUrl + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: header,
      success(res) {
        const data = res.data
        if (res.statusCode === 401) {
          app.doLogin().then(() => {
            header['Authorization'] = 'Bearer ' + app.globalData.token
            wx.request({
              url: app.globalData.baseUrl + options.url,
              method: options.method || 'GET',
              data: options.data || {},
              header: header,
              success(r) { resolve(r.data) },
              fail: reject
            })
          }).catch(reject)
          return
        }
        if (data.code === 0) {
          resolve(data)
        } else {
          wx.showToast({ title: data.msg || '请求失败', icon: 'none' })
          reject(data)
        }
      },
      fail(err) {
        wx.showToast({ title: '网络异常', icon: 'none' })
        reject(err)
      }
    })
  })
}

/* ===== 认证模块 ===== */

// 微信登录换取后端 token
function login(code) {
  return request({ url: '/auth/login', method: 'POST', data: { code } })
}

// 获取用户信息
function getUserProfile() {
  return request({ url: '/user/profile', method: 'GET' })
}

/* ===== 用户模块 ===== */

// 获取剩余次数
function getRemainCount() {
  return request({ url: '/user/remain', method: 'GET' })
}

/* ===== 对话模块 ===== */

// 发送消息（普通响应）
function sendMessage(data) {
  return request({ url: '/chat/send', method: 'POST', data })
}

// 发送消息（SSE 流式响应 - 返回 requestTask 供外部监听）
function sendMessageStream(data) {
  const app = getApp()
  const header = { 'Content-Type': 'application/json' }
  const token = wx.getStorageSync('token')
  if (token) header['Authorization'] = 'Bearer ' + token

  return wx.request({
    url: app.globalData.baseUrl + '/chat/send',
    method: 'POST',
    data: data,
    header: header,
    enableChunked: true
  })
}

// 获取对话列表
function getConversations(params) {
  return request({ url: '/chat/conversations', method: 'GET', data: params })
}

// 获取对话消息
function getMessages(conversationId) {
  return request({ url: '/chat/messages/' + conversationId, method: 'GET' })
}

// 删除对话
function deleteConversation(conversationId) {
  return request({ url: '/chat/conversations/' + conversationId, method: 'DELETE' })
}

/* ===== 日程模块 ===== */

// 获取今日提醒
function getTodaySchedules() {
  return request({ url: '/schedule/today', method: 'GET' })
}

// 获取全部提醒
function getAllSchedules() {
  return request({ url: '/schedule/all', method: 'GET' })
}

// 创建提醒
function createSchedule(data) {
  return request({ url: '/schedule', method: 'POST', data })
}

// 更新提醒（标记完成等）
function updateSchedule(id, data) {
  return request({ url: '/schedule/' + id, method: 'PUT', data })
}

// 删除提醒
function deleteSchedule(id) {
  return request({ url: '/schedule/' + id, method: 'DELETE' })
}

/* ===== 订单模块 ===== */

// 创建订单
function createOrder(data) {
  return request({ url: '/order/create', method: 'POST', data })
}

module.exports = {
  login,
  getUserProfile,
  getRemainCount,
  sendMessage,
  sendMessageStream,
  getConversations,
  getMessages,
  deleteConversation,
  getTodaySchedules,
  getAllSchedules,
  createSchedule,
  updateSchedule,
  deleteSchedule,
  createOrder
}