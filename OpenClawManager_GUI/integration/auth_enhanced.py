#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的授权系统
"""

import hashlib
import uuid
import time
import json
import os


class AuthEnhanced:
    """增强的授权系统"""
    
    def __init__(self):
        """初始化"""
        self.license_file = "license.json"
        self.license_codes_file = "license_codes.json"
    
    def get_machine_code(self):
        """获取机器码"""
        # 模拟获取机器码
        import platform
        machine_info = platform.uname()
        machine_code = hashlib.md5(
            f"{machine_info.system}{machine_info.node}{machine_info.processor}".encode()
        ).hexdigest()
        return machine_code
    
    def generate_batch_license_codes(self, count):
        """批量生成授权码"""
        codes = []
        for _ in range(count):
            # 生成唯一的授权码
            code = str(uuid.uuid4()).replace('-', '').upper()[:20]
            codes.append(code)
        
        # 保存生成的授权码
        self._save_license_codes(codes)
        
        return codes
    
    def _save_license_codes(self, codes):
        """保存授权码到文件"""
        try:
            # 读取现有授权码
            existing_codes = []
            if os.path.exists(self.license_codes_file):
                with open(self.license_codes_file, 'r', encoding='utf-8') as f:
                    existing_codes = json.load(f)
            
            # 添加新生成的授权码
            existing_codes.extend(codes)
            
            # 去重
            existing_codes = list(set(existing_codes))
            
            # 保存回文件
            with open(self.license_codes_file, 'w', encoding='utf-8') as f:
                json.dump(existing_codes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存授权码失败: {str(e)}")
    
    def verify_activation_code(self, activation_code):
        """验证激活码"""
        # 模拟验证逻辑
        # 实际应用中，这里应该与服务器验证或使用加密算法验证
        if len(activation_code) == 20 and activation_code.isalnum():
            # 保存激活信息
            self._save_license(activation_code)
            return True, "激活成功"
        else:
            return False, "激活码格式错误"
    
    def check_authorization(self):
        """检查授权状态"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    license_data = json.load(f)
                return True, f"授权到期时间: {license_data.get('expire_time', '永久')}"
            except Exception as e:
                return False, f"授权文件损坏: {str(e)}"
        else:
            return False, "未激活"
    
    def _save_license(self, activation_code):
        """保存授权信息"""
        license_data = {
            "activation_code": activation_code,
            "activate_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "expire_time": "永久"
        }
        with open(self.license_file, 'w', encoding='utf-8') as f:
            json.dump(license_data, f, indent=2, ensure_ascii=False)