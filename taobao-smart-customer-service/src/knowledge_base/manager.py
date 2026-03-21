#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库管理
"""

from typing import Dict, Any, List, Optional
import json
import os


class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        """初始化知识库管理器"""
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """加载知识库"""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": []}
    
    def _save_knowledge_base(self):
        """保存知识库"""
        with open(self.knowledge_base_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
    
    def add_entry(self, title: str, content: str, tags: List[str] = None):
        """添加知识条目"""
        entry = {
            "id": len(self.knowledge_base["entries"]) + 1,
            "title": title,
            "content": content,
            "tags": tags or [],
            "created_at": "2026-03-21"
        }
        self.knowledge_base["entries"].append(entry)
        self._save_knowledge_base()
    
    def search_entries(self, query: str) -> List[Dict[str, Any]]:
        """搜索知识条目"""
        results = []
        for entry in self.knowledge_base["entries"]:
            if query in entry["title"] or query in entry["content"]:
                results.append(entry)
        return results
    
    def get_entry_by_id(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取知识条目"""
        for entry in self.knowledge_base["entries"]:
            if entry["id"] == entry_id:
                return entry
        return None
    
    def update_entry(self, entry_id: int, title: str = None, content: str = None, 
                    tags: List[str] = None):
        """更新知识条目"""
        for entry in self.knowledge_base["entries"]:
            if entry["id"] == entry_id:
                if title is not None:
                    entry["title"] = title
                if content is not None:
                    entry["content"] = content
                if tags is not None:
                    entry["tags"] = tags
                self._save_knowledge_base()
                return True
        return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """删除知识条目"""
        new_entries = [entry for entry in self.knowledge_base["entries"] 
                      if entry["id"] != entry_id]
        if len(new_entries) < len(self.knowledge_base["entries"]):
            self.knowledge_base["entries"] = new_entries
            self._save_knowledge_base()
            return True
        return False
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """获取所有知识条目"""
        return self.knowledge_base["entries"]
