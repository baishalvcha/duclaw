// 对话页逻辑
const api = require('../../utils/api')
const util = require('../../utils/util')

// 场景名称映射
const SCENE_NAME_MAP = {
  self_media: '自媒体内容创作',
  official_doc: '公文写作',
  medical_paper: '医学论文写作',
  marketing_plan: '营销方案策划',
  teaching_design: '教师课件设计'
}

// 时间关键词模式（用于识别 AI 回复中的时间信息）
const TIME_PATTERN = /(\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2}|\d{1,2}:\d{2}|[明后今]天|下周[一二三四五六日]|周[一二三四五六日]|上午|下午|晚上|早晨|中午)/

Page({
  data: {
    sceneType: '',
    sceneName: '对话',
    conversationId: '',
    messages: [],
    inputValue: '',
    remainCount: -1,
    loading: false,
    scrollToId: ''
  },

  onLoad(options) {
    const scene = options.scene || ''
    this.setData({
      sceneType: scene,
      sceneName: SCENE_NAME_MAP[scene] || '自由对话'
    })
    this.checkRemain()
  },

  onShow() {
    this.checkRemain()
  },

  // 用户输入绑定
  onInput(e) {
    this.setData({ inputValue: e.detail.value })
  },

  // 发送消息
  onSend() {
    const { inputValue, loading } = this.data
    if (!inputValue.trim() || loading) return

    const userMessage = {
      id: util.generateId(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: Date.now()
    }

    const messages = [...this.data.messages, userMessage]
    this.setData({
      messages: messages,
      inputValue: '',
      loading: true,
      scrollToId: 'msg-' + userMessage.id
    })

    // 调用后端发送消息
    const payload = {
      content: userMessage.content,
      scene_type: this.data.sceneType,
      conversation_id: this.data.conversationId || undefined
    }

    api.sendMessage(payload).then(res => {
      if (res.code === 0 && res.data) {
        const assistantMessage = {
          id: util.generateId(),
          role: 'assistant',
          content: res.data.content || res.data.reply || '',
          timestamp: Date.now(),
          conversationId: res.data.conversation_id || '',
          hasTimeHint: false,
          remindHandled: false
        }

        // 检测时间关键词
        if (TIME_PATTERN.test(assistantMessage.content)) {
          assistantMessage.hasTimeHint = true
        }

        // 生成 Markdown HTML
        assistantMessage.richHtml = util.markdownToHtml(assistantMessage.content)

        const newMessages = [...this.data.messages, assistantMessage]
        this.setData({
          messages: newMessages,
          conversationId: res.data.conversation_id || this.data.conversationId,
          loading: false,
          scrollToId: 'msg-' + assistantMessage.id
        })

        this.checkRemain()
      } else {
        wx.showToast({ title: res.msg || 'AI 响应失败', icon: 'none' })
        this.setData({ loading: false })
      }
    }).catch(() => {
      this.setData({ loading: false })
    })
  },

  // 新建对话
  onNewChat() {
    if (this.data.loading) return

    wx.showModal({
      title: '新建对话',
      content: '确定要清空当前对话吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            conversationId: '',
            messages: [],
            inputValue: '',
            scrollToId: ''
          })
        }
      }
    })
  },

  // 查询剩余次数
  checkRemain() {
    api.getRemainCount().then(res => {
      if (res.data && typeof res.data.remain !== 'undefined') {
        this.setData({ remainCount: res.data.remain })
      }
    }).catch(() => {})
  },

  // 设置提醒
  onScheduleRemind(e) {
    const text = e.currentTarget.dataset.text || ''
    const msgId = e.currentTarget.dataset.id

    // 提取时间信息
    const match = text.match(TIME_PATTERN)
    const timeHint = match ? match[0] : ''

    wx.showModal({
      title: '设置提醒',
      content: '你想在"' + timeHint + '"设置提醒吗？请输入提醒标题',
      editable: true,
      placeholderText: '请输入提醒事项...',
      success: (res) => {
        if (res.confirm && res.content) {
          const scheduleData = {
            title: res.content,
            description: text.substring(0, 200),
            remind_time: timeHint,
            scene_type: this.data.sceneType
          }

          api.createSchedule(scheduleData).then(() => {
            wx.showToast({ title: '提醒已设置', icon: 'success' })

            // 标记该消息已处理提醒
            const messages = this.data.messages.map(m => {
              if (m.id === msgId) {
                return { ...m, remindHandled: true }
              }
              return m
            })
            this.setData({ messages })
          }).catch(() => {
            wx.showToast({ title: '设置失败', icon: 'none' })
          })
        }
      }
    })
  },

  // 忽略提醒
  onDismissRemind(e) {
    const msgId = e.currentTarget.dataset.id
    const messages = this.data.messages.map(m => {
      if (m.id === msgId) {
        return { ...m, remindHandled: true }
      }
      return m
    })
    this.setData({ messages })
  },

  // 返回
  onBack() {
    wx.navigateBack({ delta: 1 })
  }
})