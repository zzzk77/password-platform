<template>
  <div class="deepseek-chat">
    <div class="chat-header">
      <h3>🤖 DeepSeek AI 助手</h3>
      <el-button 
        type="primary" 
        size="small" 
        @click="clearChat"
        :disabled="messages.length === 0"
      >
        清空对话
      </el-button>
    </div>
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="message-content">
          <div class="message-role">{{ msg.role === 'user' ? '你' : 'DeepSeek AI' }}</div>
          <div class="message-text">{{ msg.content }}</div>
        </div>
      </div>
      <div v-if="loading" class="loading-message">
        <el-icon class="is-loading"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 1024a512 512 0 1 1 512-512a512 512 0 0 1-512 512zm0-896a384 384 0 1 0 384 384a384 384 0 0 0-384-384z" opacity=".3"></path><path fill="currentColor" d="M716.8 512a204.8 204.8 0 1 1-409.6 0a204.8 204.8 0 0 1 409.6 0z" opacity=".3"></path><path fill="currentColor" d="M870.4 512a358.4 358.4 0 1 1-716.8 0a358.4 358.4 0 0 1 716.8 0z"></path></svg></el-icon> 思考中...
      </div>
    </div>
    <div class="chat-input">
      <el-input
        v-model="inputMessage"
        placeholder="输入你的问题，例如：如何防御密码破解攻击？"
        @keyup.enter="sendMessage"
        type="textarea"
        :rows="2"
        :disabled="loading"
      ></el-input>
      <el-button 
        type="primary" 
        @click="sendMessage"
        :disabled="!inputMessage.trim() || loading"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { ElMessage, ElIcon } from 'element-plus'

const props = defineProps({
  context: {
    type: String,
    default: '密码虚拟攻防平台'
  }
})

const messages = ref([
  {
    role: 'assistant',
    content: '你好！我是DeepSeek AI助手，专注于密码学安全和攻防演练。有什么我可以帮助你的吗？'
  }
])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message) return

  messages.value.push({ role: 'user', content: message })
  inputMessage.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const apiBaseUrl = window.__API_BASE_URL__ || 'http://localhost:4000/api';
    const response = await fetch(`${apiBaseUrl}/ai/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        context: props.context
      })
    })

    if (!response.ok) {
      throw new Error('AI服务暂时不可用')
    }

    const data = await response.json()
    messages.value.push({ role: 'assistant', content: data.content })
  } catch (error) {
    ElMessage.error(error.message || 'AI服务暂时不可用，请稍后再试')
    messages.value.push({ 
      role: 'assistant', 
      content: '抱歉，AI服务暂时不可用，请稍后再试。' 
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const clearChat = () => {
  messages.value = [
    {
      role: 'assistant',
      content: '你好！我是DeepSeek AI助手，专注于密码学安全和攻防演练。有什么我可以帮助你的吗？'
    }
  ]
}
</script>

<style scoped>
.deepseek-chat {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-dark);
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.5;
}

.message.user {
  align-self: flex-end;
  background: var(--primary-color);
  color: white;
  border-bottom-right-radius: 2px;
}

.message.assistant {
  align-self: flex-start;
  background: var(--bg-dark);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-bottom-left-radius: 2px;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.message-role {
  font-size: 12px;
  font-weight: 600;
  opacity: 0.8;
}

.message-text {
  font-size: 14px;
}

.loading-message {
  align-self: flex-start;
  padding: 12px 16px;
  background: var(--bg-dark);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-input {
  padding: 15px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 10px;
  background: var(--bg-dark);
}

.chat-input .el-input {
  flex: 1;
}

.chat-input .el-input textarea {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  resize: none;
}

.chat-input .el-input__wrapper {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  box-shadow: none;
}

.chat-input .el-input__wrapper:hover {
  box-shadow: none;
  border-color: var(--primary-color);
}

.chat-input .el-input__wrapper.is-focus {
  box-shadow: none;
  border-color: var(--primary-color);
}

.chat-input .el-input__inner {
  color: var(--text-color);
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: var(--bg-light);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
}

.is-loading {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>