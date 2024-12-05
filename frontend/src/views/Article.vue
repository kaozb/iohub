<template>
  <div class="container">
    <div class="article-detail" v-if="article">
      <header>
        <router-link to="/" class="back-link">← 返回首页</router-link>
        <h1>{{ article.title }}</h1>
        <div class="meta">
          <span class="date">{{ formatDate(article.created_at) }}</span>
          <div class="labels">
            <span v-for="label in article.labels" :key="label" class="label">
              {{ label }}
            </span>
          </div>
        </div>
      </header>
      <main>
        <div class="markdown-body" v-html="markdownToHtml(article.content)"></div>
        <div class="source">
          <a :href="article.url" target="_blank">查看原文</a>
        </div>
      </main>
      <div class="image-preview" v-if="previewImage" @click="closePreview">
        <img :src="previewImage" alt="preview">
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { marked } from 'marked'
import articles from '../data/articles.json'

const props = defineProps<{
  id: string
}>()

const article = computed(() => 
  articles.find(a => a.id === parseInt(props.id))
)

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const previewImage = ref<string | null>(null)

const handleImageClick = (event: MouseEvent) => {
  const target = event.target as HTMLImageElement
  if (target.tagName === 'IMG') {
    previewImage.value = target.src
    document.body.style.overflow = 'hidden'
  }
}

const closePreview = () => {
  previewImage.value = null
  document.body.style.overflow = ''
}

const markdownToHtml = (content: string) => {
  marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: true,
    mangle: false,
    sanitize: false,
  })
  
  const html = marked(content)
  return html.replace(
    /<img\s+src="([^"]+)"/g, 
    '<div class="article-img-wrapper"><div class="img-container"><img src="$1" loading="lazy" onclick="window.handleImageClick(event)"'
  )
}

window.handleImageClick = handleImageClick
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

main {
  width: 100%;
  overflow: hidden;  /* 防止图片溢出 */
}

.back-link {
  display: inline-block;
  margin-bottom: 20px;
  color: #666;
  text-decoration: none;
}

.back-link:hover {
  color: #3498db;
}

.meta {
  margin: 20px 0;
  color: #666;
}

.date {
  display: block;
  margin: 15px 0;
}

.labels {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
img {
  width: 600px;
  height: auto;
}

.label {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  line-height: 1;
}

.label:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.source {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.source a {
  color: #3498db;
  text-decoration: none;
}

.source a:hover {
  text-decoration: underline;
}

/* Markdown 样式 */
.markdown-body {
  color: #24292e;
  line-height: 1.8;
  padding: 20px 0;
  font-size: 16px;
}

.markdown-body p {
  margin-bottom: 1.5em;
  letter-spacing: 0.02em;
}

.markdown-body >>> img{
    width: 100%;
}

/* 图片容器和图片样式 */
.markdown-body .article-img-wrapper {
  width: 100%;
  max-width: 600px;
  margin: 1.5rem auto;
}

.markdown-body .img-container {
  position: relative;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.markdown-body .img-container img {
  width: 100%;
  height: auto;
  object-fit: contain;
  background-color: #f5f5f5;
  transition: transform 0.3s ease;
  cursor: zoom-in;
  display: block;
}

.markdown-body .img-container:hover img {
  transform: scale(1.05);
}

/* 预览模式时显示完整图片 */
.image-preview img {
  width: auto;
  height: auto;
  max-width: 90%;
  max-height: 90vh;
  position: relative;
  object-fit: contain;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .markdown-body .article-img-wrapper {
    max-width: 100%; /* 移动端占满宽度 */
    margin: 1rem 0;
  }
  
  .markdown-body .img-container {
    padding-bottom: 66.67%; /* 3:2 比例，可以根据需要调整 */
    border-radius: 8px;
  }
}

/* 优化代码块显示 */
.markdown-body pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  margin-bottom: 16px;
  border: 1px solid #eaecef;
}

.markdown-body pre code {
  padding: 0;
  background: none;
  border-radius: 0;
  font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
}

/* 优化引用块样式 */
.markdown-body blockquote {
  padding: 0.5em 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
  margin: 1em 0;
  background-color: #f6f8fa;
  border-radius: 0 4px 4px 0;
}

/* 标题样式 */
.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body h1 { font-size: 2em; }
.markdown-body h2 { font-size: 1.5em; }
.markdown-body h3 { font-size: 1.25em; }

/* 适配移动端 */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }

  .markdown-body {
    padding: 15px;
  }

  .markdown-body img {
    max-width: 100%;
    border-radius: 8px;
  }

  .markdown-body p:has(img) {
    margin: 20px auto;
  }

  .label {
    padding: 4px 12px;
    font-size: 12px;
    font-weight: normal;
  }

  .image-preview img {
    max-width: 95%;
    max-height: 95vh;
  }
}

/* 优化图片说明文字 */
.markdown-body p:has(img) + p {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: -20px;
  margin-bottom: 30px;
}

/* 图片预览遮罩层 */
.image-preview {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  cursor: zoom-out;
  animation: fadeIn 0.3s ease;
}

.image-preview img {
  max-width: 90%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
  animation: zoomIn 0.3s ease;
  transition: transform 0.1s ease;
  cursor: move;
  transform-origin: center center;
  user-select: none;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style> 