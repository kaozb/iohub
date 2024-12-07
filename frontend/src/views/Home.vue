<template>
  <div class="container">
    <header>
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
  // 匹配 Markdown 图片语法
  const mdMatches = content.match(/!\[.*?\]\((.*?)\)/g)
  if (mdMatches) {
    for (const match of mdMatches) {
      const imgUrl = match.match(/!\[.*?\]\((.*?)\)/)[1]
      if (imgUrl.includes('assets/') || imgUrl.startsWith('http')) {
        return imgUrl
      }
    }
  }

  // 匹配 HTML img 标签
  const htmlMatches = content.match(/<img[^>]+src="([^">]+)"/g)
  if (htmlMatches) {
    for (const match of htmlMatches) {
      const imgUrl = match.match(/src="([^">]+)"/)[1]
      if (imgUrl.includes('assets/') || imgUrl.startsWith('http')) {
        return imgUrl
      }
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
  
  const keywords = ['介���', '简介', '概述', '背景', '主要', '核心', '特点', '功能']
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
  padding: 24px;
  min-height: calc(100vh - 64px);
}

header {
  margin-bottom: 24px;
  text-align: center;
}

.search {
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.search input {
  width: 100%;
  padding: 12px 20px;
  font-size: 0.875rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  transition: all 0.2s ease;
  color: #374151;
}

.search input:focus {
  border-color: #2563eb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search input::placeholder {
  color: #9ca3af;
}

.articles {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 12px;
}

article {
  padding: 20px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #f0f0f0;
}

article:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

article h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 12px;
  line-height: 1.4;
  color: #111827;
}

article h2 a {
  color: inherit;
  text-decoration: none;
}

.labels {
  margin: 12px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.label {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: #16a34a;
  background: #dcfce7;
  transition: all 0.2s ease;
  cursor: default;
  display: inline-flex;
  align-items: center;
  line-height: 1.2;
}

.label:hover {
  background: #bbf7d0;
}

.content {
  position: relative;
  margin: 12px 0;
  min-height: 40px;
}

.content p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #4b5563;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.date {
  color: #6b7280;
  font-size: 0.875rem;
}

.article-footer a {
  font-size: 0.875rem;
  color: #2563eb;
  font-weight: 500;
  text-decoration: none;
}

.article-footer a:hover {
  text-decoration: underline;
}

.preview-image {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%;
  margin-bottom: 12px;
  border-radius: 12px;
  overflow: hidden;
  background: #f9fafb;
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
  gap: 16px;
  margin-top: 48px;
  padding: 24px 0;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 100px;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #d1d5db;
  color: #111827;
}

.page-btn:disabled {
  background: #f9fafb;
  border-color: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  padding: 0 8px;
}

@media (max-width: 768px) {
  .container {
    padding: 16px;
  }

  .search input {
    padding: 10px 16px;
    font-size: 0.875rem;
  }

  .articles {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 8px;
  }

  article {
    padding: 16px;
  }

  article h2 {
    font-size: 1.125rem;
  }

  .preview-image {
    padding-bottom: 52.25%;
  }

  .pagination {
    gap: 12px;
    margin-top: 24px;
    padding: 16px 0;
  }

  .page-btn {
    padding: 6px 12px;
    min-width: 80px;
    font-size: 0.813rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 12px;
  }

  .search {
    max-width: 100%;
  }

  .articles {
    padding: 4px;
  }

  .content p {
    font-size: 0.875rem;
  }

  .article-footer {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
}
</style> 