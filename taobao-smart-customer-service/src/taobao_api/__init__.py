#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝开放平台API封装
"""

from .client import TaobaoAPIClient
from .webhook import TaobaoWebhookReceiver

__all__ = ["TaobaoAPIClient", "TaobaoWebhookReceiver"]
