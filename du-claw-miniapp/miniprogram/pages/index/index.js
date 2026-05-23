// 首页逻辑
const api = require('../../utils/api')

Page({
  data: {
    scenes: [
      {
        type: 'self_media',
        icon: '📱',
        title: '自媒体内容创作',
        desc: '爆款文案、短视频脚本、公众号推文一站式生成'
      },
      {
        type: 'official_doc',
        icon: '📄',
        title: '公文写作',
        desc: '通知、报告、请示等公文智能起草与格式规范'
      },
      {
        type: 'medical_paper',
        icon: '🔬',
        title: '医学论文写作',
        desc: '文献综述、研究方案、统计分析辅助'
      },
      {
        type: 'marketing_plan',
        icon: '📊',
        title: '营销方案策划',
        desc: '市场分析、策略制定、活动全案策划'
      },
      {
        type: 'teaching_design',
        icon: '📚',
        title: '教师课件设计',
        desc: '教案编写、课件大纲、教学资源整合'
      }
    ],
    todayScheduleCount: 0
  },

  onShow() {
    this.fetchTodayScheduleCount()
  },

  // 获取今日提醒数量
  fetchTodayScheduleCount() {
    api.getTodaySchedules().then(res => {
      if (res.data && Array.isArray(res.data)) {
        this.setData({ todayScheduleCount: res.data.length })
      }
    }).catch(() => {
      // 静默失败
    })
  },

  // 点击场景卡片 → 跳转对话页
  onTapScene(e) {
    const type = e.currentTarget.dataset.type
    if (!type) return

    wx.navigateTo({
      url: '/pages/chat/chat?scene=' + type
    })
  },

  // 点击日程入口 → 跳转日程页
  onTapSchedule() {
    wx.switchTab({
      url: '/pages/schedule/schedule'
    })
  }
})