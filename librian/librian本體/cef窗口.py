from .前端API import 山彥API


class CEF山彥API(山彥API):
    """把 CEF 的異步 callback 傳輸適配到 Librian API。"""

    def 取檔(self, callback):
        callback.Call(super().取檔())

    def 狀態回調(self, 步進, callback):
        callback.Call(super().狀態回調(步進))

    def 初始化(self, callback):
        callback.Call(super().初始化())


class CEF窗口:
    def __init__(self, app, browser):
        self._app = app
        self._browser = browser

    def 綁定(self, 山彥):
        self._app.frame.set_browser_object('山彥', CEF山彥API(山彥))

    def 執行js(self, script):
        return self._browser.ExecuteJavascript(script)

    def 切換全屏(self):
        return self._app.frame.toggleFullScreen()

    def 關閉(self):
        return self._app.frame.Close()

    def 運行(self):
        return self._app.MainLoop()


def 創建窗口(url, icon, title, size, storage_path):
    from rimo_utils.cef_tools import wxcef

    app, browser = wxcef.group(
        url=url,
        icon=icon,
        title=title,
        size=size,
        cache_path=storage_path,
    )
    return CEF窗口(app, browser)
