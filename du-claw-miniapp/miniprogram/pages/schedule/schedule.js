// 日程提醒中心逻辑
const api = require('../../utils/api')
const util = require('../../utils/util')

Page({
  data: {
    activeTab: 'today',
    todaySchedules: [],
    allSchedules: [],
    completedSchedules: [],

    // 创建弹窗相关
    showCreateModal: false,
    newTitle: '',
    newDesc: '',
    newTimeText: '',
    timeRange: [[], [], []],
    timeIndex: [0, 0, 0],
    selectedTimestamp: 0,

    // 时间缓存
    yearList: [],
    monthList: [],
    dayList: []
  },

  onShow() {
    this.loadSchedules()
    this.initTimeRange()
  },

  // 加载日程数据
  loadSchedules() {
    const tab = this.data.activeTab

    if (tab === 'today') {
      api.getTodaySchedules().then(res => {
        const list = (res.data || []).map(formatSchedule)
        this.setData({ todaySchedules: list })
      }).catch(() => {})
    }

    api.getAllSchedules().then(res => {
      const all = (res.data || []).map(formatSchedule)
      this.setData({
        allSchedules: all,
        completedSchedules: all.filter(s => s.completed)
      })
    }).catch(() => {})
  },

  // 初始化时间选择器数据
  initTimeRange() {
    const now = new Date()
    const yearList = []
    const monthList = []
    const dayList = []

    // 今年 + 明年
    for (let y = now.getFullYear(); y <= now.getFullYear() + 1; y++) {
      yearList.push(`${y}年`)
    }
    for (let m = 1; m <= 12; m++) {
      monthList.push(`${m}月`)
    }
    for (let d = 1; d <= 31; d++) {
      dayList.push(`${d}日`)
    }

    this.setData({
      yearList, monthList, dayList,
      timeRange: [yearList, monthList, dayList],
      timeIndex: [
        now.getFullYear() - now.getFullYear(), // 0-based
        now.getMonth(),
        now.getDate() - 1
      ]
    })
  },

  // 切换 Tab
  onSwitchTab(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ activeTab: tab })
    if (tab === 'today') {
      this.loadSchedules()
    }
  },

  // 切换完成状态
  onToggleComplete(e) {
    const id = e.currentTarget.dataset.id
    if (!id) return

    const findAndUpdate = (list) => {
      const item = list.find(s => s.id === id)
      if (!item) return null
      return { ...item, completed: !item.completed }
    }

    // 乐观更新 UI
    const todayUpdated = findAndUpdate(this.data.todaySchedules)
    const allUpdated = findAndUpdate(this.data.allSchedules)

    const updateData = {}
    if (todayUpdated) {
      updateData.todaySchedules = this.data.todaySchedules.map(s =>
        s.id === id ? todayUpdated : s
      )
    }
    if (allUpdated) {
      updateData.allSchedules = this.data.allSchedules.map(s =>
        s.id === id ? allUpdated : s
      )
    }
    this.setData(updateData)

    // 调后端
    api.updateSchedule(id, { completed: allUpdated ? allUpdated.completed : !item?.completed })
      .catch(() => {
        wx.showToast({ title: '更新失败', icon: 'none' })
        this.loadSchedules()
      })
  },

  // 删除提醒
  onDelete(e) {
    const id = e.currentTarget.dataset.id
    if (!id) return

    wx.showModal({
      title: '删除提醒',
      content: '确定要删除这条提醒吗？',
      success: (res) => {
        if (res.confirm) {
          api.deleteSchedule(id).then(() => {
            wx.showToast({ title: '已删除', icon: 'success' })
            this.loadSchedules()
          }).catch(() => {
            wx.showToast({ title: '删除失败', icon: 'none' })
          })
        }
      }
    })
  },

  // 打开创建弹窗
  onCreateReminder() {
    this.setData({ showCreateModal: true })
  },

  // 关闭弹窗
  onCloseModal() {
    this.setData({
      showCreateModal: false,
      newTitle: '',
      newDesc: '',
      newTimeText: '',
      selectedTimestamp: 0
    })
  },

  // 标题输入
  onTitleInput(e) {
    this.setData({ newTitle: e.detail.value })
  },

  // 描述输入
  onDescInput(e) {
    this.setData({ newDesc: e.detail.value })
  },

  // 时间列变化（联动天数）
  onColumnChange(e) {
    const { column, value } = e.detail
    const { yearList, monthList, dayList, timeIndex } = this.data

    const newIndex = [...timeIndex]
    newIndex[column] = value

    // 联动更新天数列表
    if (column === 0 || column === 1) {
      const year = parseInt(yearList[newIndex[0]]) || new Date().getFullYear()
      const month = parseInt(monthList[newIndex[1]]) || 1
      const maxDay = new Date(year, month, 0).getDate()
      const newDayList = []
      for (let d = 1; d <= maxDay; d++) {
        newDayList.push(`${d}日`)
      }
      // 修正日期索引
      if (newIndex[2] >= maxDay) {
        newIndex[2] = maxDay - 1
      }
      this.setData({
        timeIndex: newIndex,
        timeRange: [yearList, monthList, newDayList]
      })
    } else {
      this.setData({ timeIndex: newIndex })
    }
  },

  // 时间选择确认
  onTimeChange(e) {
    const { yearList, monthList, dayList } = this.data
    const idx = e.detail.value

    const year = parseInt(yearList[idx[0]]) || new Date().getFullYear()
    const month = parseInt(monthList[idx[1]]) || 1
    const day = parseInt(dayList[idx[2]]) || 1

    const ts = new Date(year, month - 1, day).getTime()
    const text = `${year}年${month}月${day}日`

    this.setData({
      selectedTimestamp: ts,
      newTimeText: text,
      timeIndex: idx
    })
  },

  // 确认创建
  onConfirmCreate() {
    const { newTitle, selectedTimestamp } = this.data

    if (!newTitle.trim()) {
      wx.showToast({ title: '请输入标题', icon: 'none' })
      return
    }

    const ts = selectedTimestamp || Math.floor(Date.now() / 1000)

    api.createSchedule({
      title: newTitle.trim(),
      description: this.data.newDesc.trim(),
      remind_time: ts
    }).then(() => {
      wx.showToast({ title: '创建成功', icon: 'success' })
      this.onCloseModal()
      this.loadSchedules()
    }).catch(() => {
      wx.showToast({ title: '创建失败', icon: 'none' })
    })
  }
})

// 格式化日程数据
function formatSchedule(item) {
  return {
    ...item,
    remindTimeText: item.remind_time
      ? util.formatTime(item.remind_time, 'datetime')
      : '',
    completed: !!item.completed
  }
}