#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝客服智能接入系统API服务
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any

from src.taobao_api import TaobaoWebhookReceiver
from src.message_handler import MessageProcessingPipeline, MessageLogger, MessageValidator
from src.intent_engine import IntentRecognizer, IntentContextManager
from src.role_dispatcher import RoleDispatcher
from src.monitoring.performance_monitor import PerformanceMonitor
from src.error_handling.error_handler import ErrorHandler
from src.error_handling.fallback_strategy import FallbackStrategyManager
from src.config.config_manager import ConfigManager
from .models import TaobaoWebhookRequest, ProcessingResponse

app = FastAPI(
    title="淘宝客服智能接入系统",
    description="基于混合模型的淘宝客服智能接入系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化配置管理器
config_manager = ConfigManager()

# 初始化组件
app_key = config_manager.get("taobao.app_key", "test_app_key")
app_secret = config_manager.get("taobao.app_secret", "test_app_secret")
webhook_receiver = TaobaoWebhookReceiver(app_key, app_secret)
message_pipeline = MessageProcessingPipeline()
message_pipeline.add_processor(MessageLogger())
message_pipeline.add_processor(MessageValidator())
intent_recognizer = IntentRecognizer()
intent_context_manager = IntentContextManager()
role_dispatcher = RoleDispatcher()
performance_monitor = PerformanceMonitor()
error_handler = ErrorHandler()
fallback_strategy_manager = FallbackStrategyManager()

# 系统统计信息
stats = {
    "messages_processed": 0,
    "intents_recognized": {},
    "response_times": []
}


@app.get("/")
async def root():
    """根路径"""
    return {"message": "淘宝客服智能接入系统API服务"}


@app.post("/api/v1/webhook/taobao")
async def taobao_webhook(request: Dict[str, Any]):
    """淘宝Webhook回调端点"""
    # 记录开始时间
    start_time = datetime.now()
    
    try:
        # 处理Webhook请求
        print("处理Webhook请求")
        try:
            webhook_result = await webhook_receiver.handle_webhook(request)
            print(f"Webhook处理结果: {webhook_result}")
            
            if "error" in webhook_result:
                # 处理淘宝API错误
                error_response = await error_handler.handle_error(
                    "taobao_api_error", 
                    str(request), 
                    {}
                )
                # 应用淘宝API降级策略
                fallback_response = await fallback_strategy_manager.apply_strategy(
                    "taobao_api_fallback", 
                    message={"content": "淘宝API错误"}
                )
                # 记录响应时间
                end_time = datetime.now()
                performance_monitor.record_response_time(start_time, end_time)
                return ProcessingResponse(
                    success=True,
                    intent="unknown",
                    role="judy",
                    response_content=f"{error_response}\n\n{fallback_response}"
                )
        except Exception as e:
            # 处理淘宝API错误
            error_response = await error_handler.handle_error(
                "taobao_api_error", 
                str(request), 
                {}
            )
            # 应用淘宝API降级策略
            fallback_response = await fallback_strategy_manager.apply_strategy(
                "taobao_api_fallback", 
                message={"content": "淘宝API错误"}
            )
            # 记录响应时间
            end_time = datetime.now()
            performance_monitor.record_response_time(start_time, end_time)
            return ProcessingResponse(
                success=True,
                intent="unknown",
                role="judy",
                response_content=f"{error_response}\n\n{fallback_response}"
            )
        
        # 提取消息内容
        message_dict = webhook_result["message"]
        buyer_id = message_dict.get("buyer_id")
        content = message_dict.get("content")
        print(f"提取的内容: buyer_id={buyer_id}, content={content}")
        
        # 将字典转换为具有content属性的对象
        class Message:
            def __init__(self, content):
                self.content = content
        
        message = Message(content)
        print(f"创建的消息对象: {message}")
        
        # 处理消息
        print("开始处理消息")
        processed_message = await message_pipeline.process(message)
        print(f"消息处理完成: {processed_message}")
        
        # 识别意图
        print("开始识别意图")
        try:
            intent = await intent_recognizer.recognize(content)
            print(f"识别的意图: {intent}")
        except Exception as e:
            # 处理意图识别错误
            error_response = await error_handler.handle_error(
                "intent_recognize_error", 
                content, 
                {}
            )
            # 应用意图识别降级策略
            fallback_response = await fallback_strategy_manager.apply_strategy(
                "intent_fallback", 
                message=message_dict
            )
            # 记录响应时间
            end_time = datetime.now()
            performance_monitor.record_response_time(start_time, end_time)
            return ProcessingResponse(
                success=True,
                intent="unknown",
                role="judy",
                response_content=f"{error_response}\n\n{fallback_response}"
            )
        
        # 更新意图上下文
        print("更新意图上下文")
        intent_context_manager.update_context(buyer_id, intent, content)
        print("意图上下文更新完成")
        
        # 分配角色并处理消息
        print("开始分配角色并处理消息")
        try:
            context = {"buyer_id": buyer_id, "timestamp": message_dict.get("timestamp")}
            response_content = await role_dispatcher.dispatch(intent, message_dict, context)
            print(f"生成的响应: {response_content}")
        except Exception as e:
            # 处理角色处理器错误
            error_response = await error_handler.handle_error(
                "role_handler_error", 
                content, 
                {}
            )
            # 应用角色处理器降级策略
            fallback_response = await fallback_strategy_manager.apply_strategy(
                "role_fallback", 
                message=message_dict, 
                intended_role="judy"
            )
            # 记录响应时间
            end_time = datetime.now()
            performance_monitor.record_response_time(start_time, end_time)
            return ProcessingResponse(
                success=True,
                intent=intent,
                role="judy",
                response_content=f"{error_response}\n\n{fallback_response}"
            )
        
        # 记录响应时间
        end_time = datetime.now()
        performance_monitor.record_response_time(start_time, end_time)
        
        # 更新统计信息
        stats["messages_processed"] += 1
        stats["intents_recognized"][intent] = stats["intents_recognized"].get(intent, 0) + 1
        response_time = (end_time - start_time).total_seconds()
        stats["response_times"].append(response_time)
        print("统计信息更新完成")
        
        # 提取角色名称
        role = "bee"  # 默认角色
        if "【Bee】" in response_content:
            role = "bee"
        elif "【OrderBot】" in response_content:
            role = "order_bot"
        elif "【Judy】" in response_content:
            role = "judy"
        
        return ProcessingResponse(
            success=True,
            intent=intent,
            role=role,
            response_content=response_content
        )
    except Exception as e:
        print(f"发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        # 记录响应时间（即使出错）
        end_time = datetime.now()
        performance_monitor.record_response_time(start_time, end_time)
        # 处理未知错误
        error_response = await error_handler.handle_error(
            "unknown_error", 
            str(request), 
            {}
        )
        return ProcessingResponse(
            success=True,
            intent="unknown",
            role="judy",
            response_content=error_response
        )


@app.get("/api/v1/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": datetime.now()}


@app.get("/api/v1/stats")
async def get_stats():
    """获取系统统计信息"""
    # 获取性能报告
    performance_report = performance_monitor.get_performance_report()
    # 合并统计信息
    combined_stats = {
        **stats,
        "performance": performance_report
    }
    return combined_stats
