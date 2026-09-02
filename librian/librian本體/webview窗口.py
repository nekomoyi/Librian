from pathlib import Path

from .前端API import 山彥API


橋腳本 = Path(__file__).parent / '前端/pywebview橋.js'


class WebView窗口:
    def __init__(self, webview, appkit, webkit, url, icon, title, size, storage_path):
        self._webview = webview
        self._appkit = appkit
        self._webkit = webkit
        self._url = str(url)
        self._icon = str(icon) if icon else None
        self._title = title
        self._size = tuple(size)
        self._storage_path = str(storage_path) if storage_path else None
        self._api = None
        self._window = None

    def 綁定(self, 山彥):
        self._api = 山彥API(山彥)

    def 執行js(self, script):
        return self._window.evaluate_js(script)

    def 切換全屏(self):
        return self._window.toggle_fullscreen()

    def 關閉(self):
        return self._window.destroy()

    def 運行(self):
        if self._api is None:
            raise RuntimeError('啓動窗口前必須綁定山彥')

        width, height = self._外框尺寸()
        self._window = self._webview.create_window(
            title=self._title,
            url=self._url,
            js_api=self._api,
            width=width,
            height=height,
        )
        self._window.events.before_show += self._注入橋
        self._webview.start(
            gui='cocoa',
            private_mode=False,
            storage_path=self._storage_path,
            icon=self._icon,
        )

    def _外框尺寸(self):
        內容寬, 內容高 = self._size
        樣式 = (
            self._appkit.NSWindowStyleMaskTitled
            | self._appkit.NSWindowStyleMaskClosable
            | self._appkit.NSWindowStyleMaskMiniaturizable
            | self._appkit.NSWindowStyleMaskResizable
        )
        內容矩形 = self._appkit.NSMakeRect(0, 0, 內容寬, 內容高)
        外框矩形 = self._appkit.NSWindow.frameRectForContentRect_styleMask_(內容矩形, 樣式)
        return round(外框矩形.size.width), round(外框矩形.size.height)

    def _注入橋(self):
        user_script = self._webkit.WKUserScript.alloc().initWithSource_injectionTime_forMainFrameOnly_(
            橋腳本.read_text(encoding='utf8'),
            self._webkit.WKUserScriptInjectionTimeAtDocumentStart,
            True,
        )
        self._內容控制器().addUserScript_(user_script)

    def _內容控制器(self):
        """pywebview 6 尚未公開 WKUserScript hook，將其 Cocoa 內部依賴限制在此。"""
        渲染窗口 = self._window.gui.BrowserView.instances[self._window.uid]
        return 渲染窗口.webview.configuration().userContentController()


def 創建窗口(url, icon, title, size, storage_path):
    import AppKit
    import WebKit
    import webview

    return WebView窗口(webview, AppKit, WebKit, url, icon, title, size, storage_path)
