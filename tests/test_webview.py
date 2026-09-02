import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from librian.librian本體 import webview窗口
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


class 假窗口:
    def __init__(self):
        self.events = SimpleNamespace(loaded=假事件())
        self.執行過的腳本 = []
        self.載入過的網址 = []
        self.已全屏 = False
        self.已關閉 = False

    def run_js(self, script):
        self.執行過的腳本.append(script)

    def evaluate_js(self, script):
        return script

    def load_url(self, url):
        self.載入過的網址.append(url)

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
        self.window.events.loaded.觸發()


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


class WebViewTests(unittest.TestCase):
    def test_api_returns_serializable_values_without_callbacks(self):
        api = 山彥API(假山彥())

        self.assertEqual(api.取檔(), [{'path': '/tmp/game'}])
        self.assertEqual(api.狀態回調(True), {'步進': True})
        self.assertEqual(api.初始化(), {'path': '/tmp/game'})
        self.assertFalse(hasattr(api, '讀者'))

    def test_windows_and_linux_share_the_public_pywebview_adapter(self):
        for system in ('Windows', 'Linux'):
            with self.subTest(system=system):
                fake_webview = 假WebView模塊()
                with patch('platform.system', return_value=system), patch.dict(
                    sys.modules,
                    webview=fake_webview,
                ):
                    window = self._create_window()
                    window.運行()
                    window.載入('file:///tmp/adv.html?入口=讀檔#start')

                self.assertEqual(fake_webview.create_kwargs['width'], 800)
                self.assertEqual(fake_webview.create_kwargs['height'], 600)
                self.assertEqual(
                    fake_webview.create_kwargs['url'],
                    'file:///tmp/custom-title.html?_librian_webview=1',
                )
                self.assertEqual(
                    fake_webview.window.載入過的網址,
                    ['file:///tmp/adv.html?%E5%85%A5%E5%8F%A3=%E8%AE%80%E6%AA%94&_librian_webview=1#start'],
                )
                self.assertNotIn('gui', fake_webview.start_kwargs)
                self._assert_bridge_was_injected(fake_webview)

    def test_macos_preserves_content_size_without_private_webkit_apis(self):
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
        fake_webview = 假WebView模塊()

        with patch('platform.system', return_value='Darwin'), patch.dict(
            sys.modules,
            AppKit=appkit,
            webview=fake_webview,
        ):
            window = self._create_window()
            window.運行()

        self.assertEqual(fake_webview.create_kwargs['width'], 800)
        self.assertEqual(fake_webview.create_kwargs['height'], 628)
        self.assertNotIn('gui', fake_webview.start_kwargs)
        self._assert_bridge_was_injected(fake_webview)

    def _create_window(self):
        window = webview窗口.創建窗口(
            url='file:///tmp/custom-title.html',
            icon=None,
            title='Librian',
            size=(800, 600),
            storage_path='/tmp/librian-test-cache',
        )
        window.綁定(假山彥())
        return window

    def _assert_bridge_was_injected(self, fake_webview):
        self.assertIsInstance(fake_webview.create_kwargs['js_api'], 山彥API)
        self.assertEqual(len(fake_webview.window.執行過的腳本), 1)
        source = fake_webview.window.執行過的腳本[0]
        self.assertIn('window.山彥', source)
        self.assertIn("傳輸: 'promise'", source)
        self.assertNotIn('回調', source)


if __name__ == '__main__':
    unittest.main()
