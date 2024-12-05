<template>
  <div class="container">
    <header>
      <h1>GitHub Weekly 分享站点</h1>
      <div class="search">
        <input v-model="searchQuery" placeholder="搜索文章...">
      </div>
    </header>

    <main>
      <div class="articles">
        <article v-for="article in paginatedArticles" :key="article.id">
          <h2>
            <router-link :to="{ name: 'article', params: { id: article.id }}">
              {{ article.title }}
            </router-link>
          </h2>
          <div class="preview-image" v-if="getFirstImage(article.content)">
            <img :src="getFirstImage(article.content)" :alt="article.title">
          </div>
          <div class="labels">
            <span v-for="label in article.labels" :key="label" class="label">
              {{ label }}
            </span>
          </div>
          <div class="content">
            <p>{{ getArticleExcerpt(article.content) }}</p>
            <div class="content-fade"></div>
          </div>
          <div class="article-footer">
            <span class="date">{{ formatDate(article.created_at) }}</span>
            <a :href="article.url" target="_blank">阅读更多</a>
          </div>
        </article>
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          上一页
        </button>
        
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        
        <button 
          class="page-btn" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          下一页
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { marked } from 'marked'
import articles from '../data/articles.json'

const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 6 // 每页显示的文章数量

const filteredArticles = computed(() => {
  if (!searchQuery.value) return articles
  
  const query = searchQuery.value.toLowerCase()
  return articles.filter(article => 
    article.title.toLowerCase().includes(query) ||
    article.content.toLowerCase().includes(query)
  )
})

const totalPages = computed(() => 
  Math.ceil(filteredArticles.value.length / pageSize)
)

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredArticles.value.slice(start, end)
})

watch(searchQuery, () => {
  currentPage.value = 1
})

const getFirstImage = (content: string) => {
  const imgMatch = content.match(/!\[.*?\]\((.*?)\)/)
  if (imgMatch && imgMatch[1]) {
    const imgUrl = imgMatch[1]
    if (imgUrl.includes('assets/')) {
      return imgUrl
    }
  }
  return null
}

const getArticleExcerpt = (content: string) => {
  const textContent = content
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/\[.*?\]\(.*?\)/g, '')
    .replace(/#+ /g, '')
    .replace(/\*\*/g, '')
    .trim()
  
  const paragraphs = textContent
    .split('\n')
    .filter(p => p.trim().length > 0)
    .filter(p => !p.includes('---'))
    .filter(p => p.length > 30)
  
  const keywords = ['介绍', '简介', '概述', '背景', '主要', '核心', '特点', '功能']
  const importantParagraph = paragraphs.find(p => 
    keywords.some(keyword => p.includes(keyword))
  )
  
  const selectedParagraph = importantParagraph || paragraphs[0] || ''
  
  return selectedParagraph.length > 120 
    ? selectedParagraph.slice(0, 120) + '...'
    : selectedParagraph
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 40px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.search input {
  width: 100%;
  max-width: 600px;
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.search input:focus {
  border-color: #3498db;
  outline: none;
}

.articles {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

article {
  padding: 25px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}

article:hover {
  transform: translateY(-3px);
}

article h2 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.labels {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
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

.content {
  position: relative;
  color: #666;
  line-height: 1.6;
  margin: 15px 0;
  min-height: 48px;
  max-height: 72px;
  overflow: hidden;
}

.content p {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  color: #666;
}

.content-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 24px;
  background: linear-gradient(transparent, white);
  pointer-events: none;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.date {
  color: #999;
  font-size: 0.9rem;
}

a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

.preview-image {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%;
  margin-bottom: 15px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.preview-image:hover img {
  transform: scale(1.05);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
  padding: 20px 0;
}

.page-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #3498db;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
}

.page-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}

@media (max-width: 768px) {
  .pagination {
    gap: 10px;
  }

  .page-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style> 