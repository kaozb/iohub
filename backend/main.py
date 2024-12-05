import json
import httpx
import os
from datetime import datetime
from typing import List, Dict, Any

async def fetch_weekly_issues() -> List[Dict[str, Any]]:
    """获取阮一峰的 weekly issues 数据"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.github.com/repos/ruanyf/weekly/issues",
                params={
                    "state": "all",
                    "per_page": 100,
                    "sort": "created",
                    "direction": "desc"
                }
            )
            response.raise_for_status()
            issues = response.json()
            
            articles = []
            for issue in issues:
                article = {
                    "id": issue["number"],
                    "title": issue["title"],
                    "content": issue["body"],
                    "created_at": issue["created_at"],
                    "labels": [label["name"] for label in issue["labels"]],
                    "url": issue["html_url"]
                }
                articles.append(article)
                
            return sorted(articles, key=lambda x: x["created_at"], reverse=True)
                
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return []

def save_articles(articles: List[Dict[str, Any]]) -> None:
    """保存文章数据到 JSON 文件"""
    output_dir = "../frontend/src/data"
    output_file = os.path.join(output_dir, "articles.json")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved {len(articles)} articles to {output_file}")
    except Exception as e:
        print(f"Error saving articles: {e}")

async def main():
    """主函数"""
    print("Fetching articles...")
    articles = await fetch_weekly_issues()
    if articles:
        save_articles(articles)
        print("Done!")
    else:
        print("No articles found or error occurred")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 