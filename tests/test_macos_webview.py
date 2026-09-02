import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from librian.librian本體 import webview窗口


class 假事件:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self


class 假窗口:
    def __init__(self):
        self.events = SimpleNamespace(loaded=假事件())


class 假山彥:
    def __init__(self):
        self.vue = SimpleNamespace(_內容={'path': Path('/tmp/game')})

    def 狀態回調(self, 步進, callback):
        callback.Call({'步進': 步進})

    def 初始化(self, callback):
        callback.Call()

    def __getattr__(self, 名稱):
        def 方法(*參數):
            return 名稱, 參數
        return 方法


class MacOSWebViewTests(unittest.TestCase):
    def test_path_values_are_json_serializable(self):
        value = {
            'path': Path('/tmp/game'),
            'nested': [Path('/tmp/image.png')],
        }
        self.assertEqual(
            webview窗口._可序列化(value),
            {'path': '/tmp/game', 'nested': ['/tmp/image.png']},
        )

    def test_javascript_api_only_delegates_supported_methods(self):
        api = webview窗口.山彥API(假山彥())
        self.assertEqual(api.狀態回調(True), {'步進': True})
        self.assertEqual(api.初始化(), {'path': '/tmp/game'})
        self.assertFalse(hasattr(api, '讀者'))

    def test_bundle_reuses_packaged_source_assets(self):
        frontend = Path(__file__).parents[1] / 'librian/librian本體/前端'
        bundle = (frontend / 'dist/bundle.js').read_text()
        for path in (
            '../素材/NotoSerifSC-SemiBold.otf',
            '../素材/t0.png',
            '../黑科技/synthetic_css/紙背景花紋.webp',
            '../黑科技/synthetic_css/紙背景花紋模糊.webp',
        ):
            self.assertIn(path, bundle)
        self.assertEqual([path.name for path in (frontend / 'dist').iterdir()], ['bundle.js'])

    def test_app_starts_cocoa_with_marker_user_agent(self):
        fake_window = 假窗口()
        app = webview窗口.WebViewApp(
            url='file:///tmp/index.html',
            icon=None,
            title='Librian',
            size=(800, 600),
            cache_path='/tmp/librian-test-cache',
        )
        app.frame.set_browser_object('山彥', 假山彥())

        with patch.object(webview窗口, '_外框尺寸', return_value=(800, 628)) as 外框尺寸, \
                patch.object(webview窗口.webview, 'create_window', return_value=fake_window) as create, \
                patch.object(webview窗口.webview, 'start') as start:
            app.MainLoop()

        self.assertIs(app.frame.window, fake_window)
        self.assertIs(app.frame.browser.window, fake_window)
        self.assertIsInstance(create.call_args.kwargs['js_api'], webview窗口.山彥API)
        外框尺寸.assert_called_once_with((800, 600))
        self.assertEqual(create.call_args.kwargs['width'], 800)
        self.assertEqual(create.call_args.kwargs['height'], 628)
        self.assertEqual(start.call_args.kwargs['gui'], 'cocoa')
        self.assertEqual(start.call_args.kwargs['user_agent'], webview窗口.用戶代理標記)
        self.assertEqual(fake_window.events.loaded.handlers, [])
        self.assertEqual(
            os.fspath(start.call_args.kwargs['storage_path']),
            '/tmp/librian-test-cache',
        )


if __name__ == '__main__':
    unittest.main()
