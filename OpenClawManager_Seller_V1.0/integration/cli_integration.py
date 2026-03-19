#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 命令调用模块
"""

import subprocess
import threading
import queue
import time


class CLIIntegration:
    """CLI 命令调用模块"""
    
    def __init__(self):
        """初始化"""
        self.process = None
        self.output_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.is_running = False
    
    def execute_command(self, command, callback=None):
        """执行命令"""
        try:
            # 执行命令
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            # 处理结果
            output = result.stdout
            error = result.stderr
            returncode = result.returncode
            
            if callback:
                callback(output, error, returncode)
            
            return output, error, returncode
        except Exception as e:
            error = str(e)
            if callback:
                callback("", error, -1)
            return "", error, -1
    
    def execute_command_async(self, command, output_callback=None, error_callback=None, done_callback=None):
        """异步执行命令"""
        def run_command():
            try:
                # 执行命令
                process = subprocess.Popen(
                    command, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                self.process = process
                self.is_running = True
                
                # 读取输出
                for line in process.stdout:
                    line = line.strip()
                    if output_callback:
                        output_callback(line)
                
                # 读取错误
                for line in process.stderr:
                    line = line.strip()
                    if error_callback:
                        error_callback(line)
                
                # 等待进程结束
                returncode = process.wait()
                
                if done_callback:
                    done_callback(returncode)
            except Exception as e:
                error = str(e)
                if error_callback:
                    error_callback(error)
                if done_callback:
                    done_callback(-1)
            finally:
                self.is_running = False
                self.process = None
        
        # 创建并启动线程
        thread = threading.Thread(target=run_command)
        thread.daemon = True
        thread.start()
    
    def stop_command(self):
        """停止当前运行的命令"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception as e:
                print(f"停止命令失败: {str(e)}")
            finally:
                self.is_running = False
                self.process = None
    
    def is_command_running(self):
        """检查命令是否正在运行"""
        return self.is_running
    
    def execute_openclaw_command(self, subcommand, callback=None):
        """执行 OpenClaw 命令"""
        command = f"openclaw {subcommand}"
        return self.execute_command(command, callback)
    
    def execute_openclaw_command_async(self, subcommand, output_callback=None, error_callback=None, done_callback=None):
        """异步执行 OpenClaw 命令"""
        command = f"openclaw {subcommand}"
        self.execute_command_async(command, output_callback, error_callback, done_callback)