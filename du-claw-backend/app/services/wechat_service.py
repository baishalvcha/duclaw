"""微信服务 —— 登录、access_token、模板消息、支付。"""

import hashlib
import uuid
from typing import Any, Dict, Optional

import httpx
from loguru import logger

from app.config import (
    WECHAT_APPID,
    WECHAT_AES_KEY,
    WECHAT_MCH_ID,
    WECHAT_NOTIFY_URL,
    WECHAT_PAY_KEY,
    WECHAT_SECRET,
    WECHAT_TOKEN,
)


class WechatService:
    def __init__(self):
        self.appid = WECHAT_APPID
        self.secret = WECHAT_SECRET
        self.token = WECHAT_TOKEN
        self.aes_key = WECHAT_AES_KEY
        self.mch_id = WECHAT_MCH_ID
        self.pay_key = WECHAT_PAY_KEY
        self._access_token: Optional[str] = None
        self._access_token_expires: int = 0
        logger.info("WechatService initialized")

    async def get_access_token(self) -> str:
        """获取并缓存微信公众号/小程序 access_token。"""
        import time

        if self._access_token and time.time() < self._access_token_expires:
            return self._access_token

        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            data = resp.json()

        if "access_token" in data:
            self._access_token = data["access_token"]
            self._access_token_expires = time.time() + data.get("expires_in", 7200) - 300
            logger.info("Access token refreshed")
            return self._access_token
        else:
            logger.error(f"Failed to get access_token: {data}")
            raise RuntimeError(f"获取 access_token 失败: {data}")

    async def code2session(self, code: str) -> Dict[str, Any]:
        """微信小程序登录：code 换取 openid 和 unionid。"""
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            data = resp.json()

        if "errcode" in data and data["errcode"] != 0:
            logger.error(f"code2session failed: {data}")
            raise RuntimeError(f"微信登录失败: {data.get('errmsg', '未知错误')}")

        logger.info(f"code2session success, openid={data.get('openid')}")
        return data

    async def send_template_message(
        self,
        openid: str,
        template_id: str,
        data: Dict[str, Dict[str, str]],
        page: str = "",
    ) -> bool:
        """发送微信模板消息。"""
        access_token = await self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"

        body = {
            "touser": openid,
            "template_id": template_id,
            "page": page,
            "data": data,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=body)
            result = resp.json()

        if result.get("errcode") == 0:
            logger.info(f"Template message sent to {openid}")
            return True
        else:
            logger.error(f"Template message failed: {result}")
            return False

    async def send_reminder(
        self, openid: str, title: str, description: Optional[str] = None
    ) -> bool:
        """发送日程提醒模板消息。"""
        data = {
            "thing1": {"value": title[:20]},
            "thing2": {"value": (description or "无")[:20]},
            "time3": {"value": "请及时查看"},
        }
        # template_id 需要在小程序后台申请
        template_id = "YOUR_REMINDER_TEMPLATE_ID"
        return await self.send_template_message(openid, template_id, data)

    def unified_order(
        self, openid: str, out_trade_no: str, total_fee: int, body: str
    ) -> Dict[str, str]:
        """微信支付统一下单（JSAPI）。"""
        # 生成随机字符串
        nonce_str = uuid.uuid4().hex[:32]

        params = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "nonce_str": nonce_str,
            "body": body,
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "spbill_create_ip": "8.159.152.197",
            "notify_url": WECHAT_NOTIFY_URL,
            "trade_type": "JSAPI",
            "openid": openid,
        }

        # 生成签名
        sign = self._generate_sign(params)
        params["sign"] = sign

        logger.info(f"Unified order created: {out_trade_no}, fee={total_fee}")
        return params

    def verify_callback_sign(self, params: Dict[str, str]) -> bool:
        """验证微信支付回调签名。"""
        received_sign = params.pop("sign", "")
        expected_sign = self._generate_sign(params)
        params["sign"] = received_sign
        return received_sign == expected_sign

    def _generate_sign(self, params: Dict[str, str]) -> str:
        """生成微信支付 MD5 签名。"""
        # 按 key 排序
        sorted_items = sorted(
            (k, v) for k, v in params.items() if v and k != "sign"
        )
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_items)
        sign_str += f"&key={self.pay_key}"
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()


# 全局单例
wechat_service = WechatService()