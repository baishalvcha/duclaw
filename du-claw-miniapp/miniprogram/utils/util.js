// du-claw 通用工具函数

/**
 * 格式化时间戳为可读字符串
 * @param {number|string} timestamp Unix 时间戳（秒）或 ISO 字符串
 * @param {string} format 格式类型：'datetime' | 'date' | 'time' | 'relative'
 */
function formatTime(timestamp, format = 'datetime') {
  if (!timestamp) return ''

  let date
  if (typeof timestamp === 'number') {
    // 如果小于 10000000000 可能是秒级时间戳，否则是毫秒
    date = new Date(timestamp < 10000000000 ? timestamp * 1000 : timestamp)
  } else {
    date = new Date(timestamp)
  }

  if (isNaN(date.getTime())) return ''

  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hour = date.getHours().toString().padStart(2, '0')
  const minute = date.getMinutes().toString().padStart(2, '0')
  const second = date.getSeconds().toString().padStart(2, '0')

  switch (format) {
    case 'date':
      return `${year}-${month}-${day}`
    case 'time':
      return `${hour}:${minute}`
    case 'datetime':
      return `${year}-${month}-${day} ${hour}:${minute}`
    case 'full':
      return `${year}-${month}-${day} ${hour}:${minute}:${second}`
    case 'relative':
      return formatRelative(date)
    default:
      return `${year}-${month}-${day} ${hour}:${minute}`
  }
}

/**
 * 格式化为相对时间描述
 */
function formatRelative(date) {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const absDiff = Math.abs(diff)

  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (absDiff < minute) return '刚刚'
  if (absDiff < hour) return Math.floor(absDiff / minute) + '分钟前'
  if (absDiff < day) return Math.floor(absDiff / hour) + '小时前'
  if (absDiff < 7 * day) return Math.floor(absDiff / day) + '天前'

  const month = date.getMonth() + 1
  const dayOfMonth = date.getDate()
  return `${month}月${dayOfMonth}日`
}

/**
 * 防抖函数
 * @param {Function} fn 目标函数
 * @param {number} delay 延迟毫秒数
 */
function debounce(fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
      timer = null
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn 目标函数
 * @param {number} interval 间隔毫秒数
 */
function throttle(fn, interval = 300) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= interval) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

/**
 * 简单的 Markdown 转 HTML 解析（支持微信 rich-text 组件）
 * 支持的语法：**加粗**、*斜体*、`代码`、换行、标题、列表、链接
 */
function markdownToHtml(md) {
  if (!md) return ''

  let html = md

  // 转义 HTML 实体
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // 代码块（多行）
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre style="background:#13132a;padding:16rpx;border-radius:8rpx;overflow-x:auto;font-size:24rpx;color:#8b7cff;">$2</pre>')

  // 行内代码
  html = html.replace(/`([^`]+)`/g, '<code style="background:#13132a;color:#6c63ff;padding:2rpx 8rpx;border-radius:4rpx;font-size:24rpx;">$1</code>')

  // 标题
  html = html.replace(/^### (.+)$/gm, '<h3 style="font-size:30rpx;font-weight:600;color:#fff;margin:16rpx 0 8rpx;">$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2 style="font-size:32rpx;font-weight:700;color:#fff;margin:20rpx 0 10rpx;">$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1 style="font-size:36rpx;font-weight:700;color:#fff;margin:24rpx 0 12rpx;">$1</h1>')

  // 加粗
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')

  // 斜体
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>')

  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:#6c63ff;text-decoration:underline;">$1</a>')

  // 无序列表
  html = html.replace(/^- (.+)$/gm, '<li style="margin:4rpx 0;color:#d0d0e0;">$1</li>')
  html = html.replace(/(<li[^>]*>.*<\/li>)/gs, '<ul style="padding-left:32rpx;margin:8rpx 0;">$1</ul>')

  // 有序列表
  html = html.replace(/^\d+\. (.+)$/gm, '<li style="margin:4rpx 0;color:#d0d0e0;">$1</li>')

  // 换行
  html = html.replace(/\n\n/g, '<br/>')
  html = html.replace(/\n/g, '<br/>')

  return html
}

/**
 * 截取字符串（中英文混合）
 */
function truncate(str, len = 50) {
  if (!str) return ''
  if (str.length <= len) return str
  return str.slice(0, len) + '...'
}

/**
 * 生成唯一 ID
 */
function generateId() {
  return 'id_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9)
}

module.exports = {
  formatTime,
  formatRelative,
  debounce,
  throttle,
  markdownToHtml,
  truncate,
  generateId
}