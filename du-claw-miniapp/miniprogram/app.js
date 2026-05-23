// du-claw 个人 AI 助手 - 小程序入口
App({
  globalData: {
    userInfo: null,
    token: '',
    baseUrl: 'https://www.mahong.tech/api/duclaw'
  },

  onLaunch() {
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.token = token
      this.checkTokenAndLogin()
    }
  },

  // 检查 token 有效性并获取用户信息
  checkTokenAndLogin() {
    this.request({
      url: '/user/profile',
      method: 'GET'
    }).then(res => {
      if (res.code === 0) {
        this.globalData.userInfo = res.data
        wx.setStorageSync('userInfo', res.data)
      }
    }).catch(() => {
      // token 失效，重新登录
      this.doLogin()
    })
  },

  // 微信登录换取后端 token
  doLogin() {
    return new Promise((resolve, reject) => {
      wx.login({
        success: (loginRes) => {
          if (loginRes.code) {
            wx.request({
              url: this.globalData.baseUrl + '/auth/login',
              method: 'POST',
              data: { code: loginRes.code },
              success: (res) => {
                if (res.data.code === 0 && res.data.data && res.data.data.token) {
                  const token = res.data.data.token
                  this.globalData.token = token
                  wx.setStorageSync('token', token)
                  this.globalData.userInfo = res.data.data.userInfo || null
                  wx.setStorageSync('userInfo', this.globalData.userInfo)
                  resolve(token)
                } else {
                  reject(res.data)
                }
              },
              fail: reject
            })
          } else {
            reject(new Error('wx.login 失败'))
          }
        },
        fail: reject
      })
    })
  },

  // 封装网络请求，自动带 Authorization header
  request(options) {
    const that = this
    return new Promise((resolve, reject) => {
      const header = {
        'Content-Type': 'application/json',
        ...options.header
      }
      if (this.globalData.token) {
        header['Authorization'] = 'Bearer ' + this.globalData.token
      }

      wx.request({
        url: this.globalData.baseUrl + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: header,
        success(res) {
          if (res.statusCode === 401) {
            // token 过期，重新登录后重试
            that.doLogin().then(() => {
              // 重新执行原请求
              header['Authorization'] = 'Bearer ' + that.globalData.token
              wx.request({
                url: that.globalData.baseUrl + options.url,
                method: options.method || 'GET',
                data: options.data || {},
                header: header,
                success(retryRes) {
                  resolve(retryRes.data)
                },
                fail: reject
              })
            }).catch(reject)
            return
          }
          resolve(res.data)
        },
        fail(err) {
          wx.showToast({ title: '网络异常', icon: 'none' })
          reject(err)
        }
      })
    })
  }
})