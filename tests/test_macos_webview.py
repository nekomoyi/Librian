import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from librian.librian本體 import webview窗口
from librian.librian本體.cef窗口 import CEF山彥API
from librian.librian本體.前端API import 山彥API


class 假事件:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def 觸發(self):
        for handler in self.handlers:
            handler()


class 假內容控制器:
    def __init__(self):
        self.scripts = []

    def addUserScript_(self, script):
        self.scripts.append(script)


class 假原生WebView:
    def __init__(self, 內容控制器):
        self._配置 = SimpleNamespace(userContentController=lambda: 內容控制器)

    def configuration(self):
        return self._配置


class 假窗口:
    def __init__(self):
        self.uid = 'window-1'
        self.events = SimpleNamespace(before_show=假事件())
        self.內容控制器 = 假內容控制器()
        渲染窗口 = SimpleNamespace(webview=假原生WebView(self.內容控制器))
        self.gui = SimpleNamespace(
            BrowserView=SimpleNamespace(instances={self.uid: 渲染窗口}),
        )
        self.執行過的腳本 = []
        self.已全屏 = False
        self.已關閉 = False

    def evaluate_js(self, script):
        self.執行過的腳本.append(script)

    def toggle_fullscreen(self):
        self.已全屏 = True

    def destroy(self):
        self.已關閉 = True


class 假WebView模塊:
    def __init__(self):
        self.window = 假窗口()
        self.create_kwargs = None
        self.start_kwargs = None

    def create_window(self, **kwargs):
        self.create_kwargs = kwargs
        return self.window

    def start(self, **kwargs):
        self.start_kwargs = kwargs
        self.window.events.before_show.觸發()


class 假山彥:
    def 取檔(self):
        return [{'path': Path('/tmp/game')}]

    def 狀態回調(self, 步進):
        return {'步進': 步進}

    def 初始化(self):
        return {'path': Path('/tmp/game')}

    def __getattr__(self, 名稱):
        def 方法(*參數):
            return 名稱, 參數
        return 方法


class 假回調:
    def Call(self, 值):
        self.值 = 值


class MacOSWebViewTests(unittest.TestCase):
    def test_api_returns_serializable_values_without_callbacks(self):
        api = 山彥API(假山彥())

        self.assertEqual(api.取檔(), [{'path': '/tmp/game'}])
        self.assertEqual(api.狀態回調(True), {'步進': True})
        self.assertEqual(api.初始化(), {'path': '/tmp/game'})
        self.assertFalse(hasattr(api, '讀者'))

    def test_cef_adapts_result_methods_at_the_transport_boundary(self):
        callback = 假回調()

        CEF山彥API(假山彥()).初始化(callback)

        self.assertEqual(callback.值, {'path': '/tmp/game'})

    def test_every_page_receives_the_bridge_at_document_start(self):
        appkit = SimpleNamespace(
            NSWindowStyleMaskTitled=1,
            NSWindowStyleMaskClosable=2,
            NSWindowStyleMaskMiniaturizable=4,
            NSWindowStyleMaskResizable=8,
            NSMakeRect=lambda *_: object(),
            NSWindow=SimpleNamespace(
                frameRectForContentRect_styleMask_=lambda *_: SimpleNamespace(
                    size=SimpleNamespace(width=800, height=628),
                ),
            ),
        )
        injection_time = object()

        class 假UserScript:
            @classmethod
            def alloc(cls):
                return cls()

            def initWithSource_injectionTime_forMainFrameOnly_(self, source, when, main_only):
                return source, when, main_only

        webkit = SimpleNamespace(
            WKUserScript=假UserScript,
            WKUserScriptInjectionTimeAtDocumentStart=injection_time,
        )
        webview = 假WebView模塊()

        with patch.dict(sys.modules, AppKit=appkit, WebKit=webkit, webview=webview):
            window = webview窗口.創建窗口(
                url='file:///tmp/custom-title.html',
                icon=None,
                title='Librian',
                size=(800, 600),
                storage_path='/tmp/librian-test-cache',
            )
            window.綁定(假山彥())
            window.運行()

        self.assertIsInstance(webview.create_kwargs['js_api'], 山彥API)
        self.assertEqual(webview.create_kwargs['width'], 800)
        self.assertEqual(webview.create_kwargs['height'], 628)
        self.assertEqual(webview.start_kwargs['gui'], 'cocoa')
        self.assertEqual(len(webview.window.內容控制器.scripts), 1)
        source, when, main_only = webview.window.內容控制器.scripts[0]
        self.assertIn('window.山彥', source)
        self.assertIn("傳輸: 'promise'", source)
        self.assertNotIn('回調', source)
        self.assertIs(when, injection_time)
        self.assertTrue(main_only)


if __name__ == '__main__':
    unittest.main()
