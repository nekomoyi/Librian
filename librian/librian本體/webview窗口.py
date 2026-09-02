"""基於 macOS 原生 WKWebView 的 Librian 窗口後端。

這個模塊保留 rimo_utils.cef_tools 的最小接口，讓上層不需要知道窗口是
CEF 還是 pywebview。pywebview 在 macOS 上使用 PyObjC + WKWebView，原生支持
Apple Silicon。
"""

import os
from pathlib import Path
from typing import Any, Optional

import AppKit
import webview


用戶代理標記 = "LibrianPyWebView/1.0"


def _外框尺寸(內容尺寸):
    """用 Cocoa 當前窗口樣式將目標網頁尺寸換算成初始外框尺寸。"""
    內容寬, 內容高 = 內容尺寸
    樣式 = (
        AppKit.NSWindowStyleMaskTitled
        | AppKit.NSWindowStyleMaskClosable
        | AppKit.NSWindowStyleMaskMiniaturizable
        | AppKit.NSWindowStyleMaskResizable
    )
    內容矩形 = AppKit.NSMakeRect(0, 0, 內容寬, 內容高)
    外框矩形 = AppKit.NSWindow.frameRectForContentRect_styleMask_(內容矩形, 樣式)
    return round(外框矩形.size.width), round(外框矩形.size.height)


def _可序列化(值):
    if isinstance(值, os.PathLike):
        return os.fspath(值)
    if isinstance(值, dict):
        return {鍵: _可序列化(內容) for 鍵, 內容 in 值.items()}
    if isinstance(值, (list, tuple)):
        return [_可序列化(內容) for 內容 in 值]
    return 值


class _回調:
    def Call(self, 值=None):
        self.值 = 值


class 山彥API:
    """只向 JavaScript 暴露前端實際需要的方法。"""

    def __init__(self, 山彥):
        self._山彥 = 山彥

    def vue連接初始化(self):
        return _可序列化(self._山彥.vue._內容)

    def vue更新(self, 內容):
        return self._山彥.vue更新(內容)

    def 取檔(self):
        callback = _回調()
        self._山彥.取檔(callback)
        return _可序列化(callback.值)

    def 存檔(self, 文件名, 描述, 截圖):
        return self._山彥.存檔(文件名, 描述, 截圖)

    def 讀檔(self, 文件名):
        return self._山彥.讀檔(文件名)

    def 快速存檔(self):
        return self._山彥.快速存檔()

    def 快速讀檔(self):
        return self._山彥.快速讀檔()

    def 切換全屏(self):
        return self._山彥.切換全屏()

    def 退出(self):
        return self._山彥.窗口.close()

    def 回標題(self):
        return self._山彥.回標題()

    def 步進(self):
        return self._山彥.步進()

    def 更新(self, 瞬間化=False):
        return self._山彥.更新(瞬間化)

    def 狀態回調(self, 步進):
        callback = _回調()
        self._山彥.狀態回調(步進, callback)
        return _可序列化(callback.值)

    def 初始化(self):
        self._山彥.初始化(_回調())
        return _可序列化(self._山彥.vue._內容)

    def 選(self, 參數):
        return self._山彥.選(參數)

    def 開始(self):
        return self._山彥.開始()

    def 讀檔畫面(self):
        return self._山彥.讀檔畫面()

    def 從劇本開始(self, 劇本):
        return self._山彥.從劇本開始(劇本)

    def 更新終態(self):
        return self._山彥.更新終態()


class 瀏覽器代理:
    def __init__(self):
        self.window: Optional[webview.Window] = None

    def ExecuteJavascript(self, script: str):
        if self.window is None:
            raise RuntimeError("Librian 窗口尚未創建")
        return self.window.evaluate_js(script)


class 主窗口代理:
    def __init__(self, browser: 瀏覽器代理):
        self.browser = browser
        self.window: Optional[webview.Window] = None
        self.js_api: Any = None

    def set_browser_object(self, name: str, obj: Any):
        if name != "山彥":
            raise ValueError(f"pywebview 後端不支持瀏覽器對象「{name}」")
        self.js_api = 山彥API(obj)

    def toggleFullScreen(self):
        if self.window is not None:
            self.window.toggle_fullscreen()

    def close(self):
        if self.window is not None:
            self.window.destroy()


class WebViewApp:
    def __init__(self, url, icon, title, size, **settings):
        self.url = str(url)
        self.icon = str(icon) if icon else None
        self.title = title
        self.size = tuple(size)
        self.storage_path = settings.get("cache_path")
        self.frame = 主窗口代理(瀏覽器代理())

    def MainLoop(self):
        if self.frame.js_api is None:
            raise RuntimeError("啓動窗口前必須綁定山彥")

        width, height = _外框尺寸(self.size)
        window = webview.create_window(
            title=self.title,
            url=self.url,
            js_api=self.frame.js_api,
            width=width,
            height=height,
        )
        self.frame.window = window
        self.frame.browser.window = window

        storage_path = str(Path(self.storage_path)) if self.storage_path else None
        webview.start(
            gui="cocoa",
            private_mode=False,
            storage_path=storage_path,
            icon=self.icon,
            user_agent=用戶代理標記,
        )


def group(url, icon, title, size, **settings):
    app = WebViewApp(url=url, icon=icon, title=title, size=size, **settings)
    return app, app.frame.browser
