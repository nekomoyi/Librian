(function () {
    'use strict';

    if (new URLSearchParams(window.location.search).get('_librian_webview') !== '1') {
        return;
    }
    if (window.山彥 && window.山彥.傳輸 === 'promise') {
        return;
    }

    var api就緒 = new Promise(function (resolve) {
        if (window.pywebview && window.pywebview.api) {
            resolve(window.pywebview.api);
            return;
        }
        window.addEventListener('pywebviewready', function () {
            resolve(window.pywebview.api);
        }, { once: true });
    });
    var 調用隊列 = Promise.resolve();

    window.山彥 = new Proxy({ 傳輸: 'promise' }, {
        get: function (目標, 方法) {
            if (方法 in 目標) {
                return 目標[方法];
            }
            return function () {
                var 參數 = Array.prototype.slice.call(arguments);
                var 結果 = 調用隊列.then(function () {
                    return api就緒.then(function (api) {
                        return api[方法].apply(api, 參數);
                    });
                });
                調用隊列 = 結果.catch(function () {});
                return 結果;
            };
        }
    });
})();
