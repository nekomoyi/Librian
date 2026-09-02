(function () {
    'use strict';

    var api就緒 = new Promise(function (resolve) {
        if (window.pywebview && window.pywebview.api) {
            resolve(window.pywebview.api);
            return;
        }
        window.addEventListener('pywebviewready', function () {
            resolve(window.pywebview.api);
        }, { once: true });
    });

    window.山彥 = new Proxy({ 傳輸: 'promise' }, {
        get: function (目標, 方法) {
            if (方法 in 目標) {
                return 目標[方法];
            }
            return function () {
                var 參數 = Array.prototype.slice.call(arguments);
                return api就緒.then(function (api) {
                    return api[方法].apply(api, 參數);
                });
            };
        }
    });
})();
