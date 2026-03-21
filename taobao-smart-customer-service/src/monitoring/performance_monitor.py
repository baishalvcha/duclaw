#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能监控器
"""

from typing import Dict, Any, List
from datetime import datetime


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化性能监控器"""
        self.metrics = {
            "response_times": [],
            "intent_accuracy": [],
            "role_effectiveness": []
        }
        self.start_time = datetime.now()
    
    def record_response_time(self, start_time: datetime, end_time: datetime):
        """记录响应时间"""
        response_time = (end_time - start_time).total_seconds()
        self.metrics["response_times"].append(response_time)
        
        # 保持最近1000条记录
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
    
    def record_intent_result(self, expected: str, actual: str):
        """记录意图识别结果"""
        accuracy = 1.0 if expected == actual else 0.0
        self.metrics["intent_accuracy"].append(accuracy)
    
    def record_role_effectiveness(self, effectiveness: float):
        """记录角色有效性"""
        self.metrics["role_effectiveness"].append(effectiveness)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """获取性能报告"""
        # 计算平均响应时间
        avg_response_time = 0
        if self.metrics["response_times"]:
            avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
        
        # 计算平均意图识别准确率
        avg_accuracy = 0
        if self.metrics["intent_accuracy"]:
            avg_accuracy = sum(self.metrics["intent_accuracy"]) / len(self.metrics["intent_accuracy"])
        
        # 计算平均角色有效性
        avg_effectiveness = 0
        if self.metrics["role_effectiveness"]:
            avg_effectiveness = sum(self.metrics["role_effectiveness"]) / len(self.metrics["role_effectiveness"])
        
        return {
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "total_messages": len(self.metrics["response_times"]),
            "avg_response_time": avg_response_time,
            "avg_intent_accuracy": avg_accuracy,
            "avg_role_effectiveness": avg_effectiveness,
            "response_time_stats": {
                "min": min(self.metrics["response_times"]) if self.metrics["response_times"] else 0,
                "max": max(self.metrics["response_times"]) if self.metrics["response_times"] else 0,
                "count": len(self.metrics["response_times"])
            }
        }
