// 我的页面逻辑
const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    userInfo: {},
    remainCounts: {},

    plans: [
      {
        type: 'single_trial',
        name: '单次体验',
        tag: '尝鲜',
        price: '9.9',
        unit: '次',
        recommended: false,
        features: ['1 次 AI 对话', '全场景可用', '24 小时内有效']
      },
      {
        type: 'pack_10',
        name: '10 次包',
        tag: '热门',
        price: '69',
        unit: '10次',
        recommended: true,
        features: ['10 次 AI 对话', '全场景可用', '30 天内有效', '优先响应']
      },
      {
        type: 'pack_30',
        name: '30 次包',
        tag: '超值',
        price: '149',
        unit: '30次',
        recommended: false,
        features: ['30 次 AI 对话', '全场景可用', '90 天内有效', '优先响应', '专属客服']
      },
      {
        type: 'monthly_unlimited',
        name: '月无限',
        tag: '畅享',
        price: '99',
        unit: '月',
        recommended: false,
        features: ['无限次 AI 对话', '全场景可用', '按月订阅', '自动续费可关闭']
      },
      {
        type: 'schedule_pro',
        name: '日程 Pro',
        tag: '增值',
        price: '19.9',
        unit: '月',
        recommended: false,
        features: ['无限日程提醒', '智能时间解析', '短信/微信提醒', '日历同步']
      }
    ]
  },

  onShow() {
    this.loadUserProfile()
    this.loadRemainCounts()
  },

  // 加载用户信息
  loadUserProfile() {
    const cached = wx.getStorageSync('userInfo')
    if (cached) {
      this.setData({ userInfo: cached })
    }

    api.getUserProfile().then(res => {
      if (res.data) {
        this.setData({ userInfo: res.data })
        wx.setStorageSync('userInfo', res.data)
      }
    }).catch(() => {})
  },

  // 加载剩余次数
  loadRemainCounts() {
    api.getRemainCount().then(res => {
      if (res.data) {
        this.setData({ remainCounts: res.data })
      }
    }).catch(() => {})
  },

  // 编辑资料
  onEditProfile() {
    wx.showToast({ title: '功能开发中', icon: 'none' })
  },

  // 购买套餐
  onBuyPlan(e) {
    const planType = e.currentTarget.dataset.type
    if (!planType) return

    const plan = this.data.plans.find(p => p.type === planType)
    if (!plan) return

    wx.showModal({
      title: '确认购买',
      content: `确定购买「${plan.name}」套餐？\n金额：￥${plan.price}/${plan.unit}`,
      success: (res) => {
        if (res.confirm) {
          this.doPurchase(planType)
        }
      }
    })
  },

  // 执行购买流程
  doPurchase(planType) {
    wx.showLoading({ title: '创建订单...' })

    api.createOrder({ plan_type: planType }).then(res => {
      wx.hideLoading()

      if (res.code === 0 && res.data) {
        const payParams = res.data.payParams || res.data

        // 调用微信支付
        wx.requestPayment({
          timeStamp: String(payParams.timeStamp || ''),
          nonceStr: payParams.nonceStr || '',
          package: payParams.package || '',
          signType: payParams.signType || 'MD5',
          paySign: payParams.paySign || '',
          success: () => {
            wx.showToast({ title: '购买成功', icon: 'success' })
            this.loadRemainCounts()
          },
          fail: (err) => {
            if (err.errMsg.indexOf('cancel') < 0) {
              wx.showToast({ title: '支付失败', icon: 'none' })
            }
          }
        })
      } else {
        wx.showToast({ title: res.msg || '创建订单失败', icon: 'none' })
      }
    }).catch(() => {
      wx.hideLoading()
      wx.showToast({ title: '网络异常', icon: 'none' })
    })
  },

  // 使用记录
  onUsageHistory() {
    wx.showToast({ title: '功能开发中', icon: 'none' })
  }
})