(function () {
    'use strict';

    var 是PyWebView = navigator.userAgent.indexOf('LibrianPyWebView/') !== -1;
    if (!是PyWebView || window.山彥) {
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

    function 調用(方法, 參數, 回調) {
        api就緒
            .then(function (api) {
                if (typeof api[方法] !== 'function') {
                    throw new Error('山彥沒有方法「' + 方法 + '」');
                }
                return api[方法].apply(api, 參數 || []);
            })
            .then(function (結果) {
                if (回調) {
                    回調(結果);
                }
            })
            .catch(function (錯誤) {
                console.error('調用山彥.' + 方法 + '失敗', 錯誤);
            });
    }

    function 合併Vue狀態(狀態) {
        if (!狀態 || !window.v) {
            return;
        }
        Object.keys(狀態).forEach(function (鍵) {
            window.v[鍵] = 狀態[鍵];
        });
    }

    var 山彥 = {};
    [
        '存檔', '讀檔', '快速存檔', '快速讀檔', '切換全屏', '退出',
        'vue更新', '回標題', '步進', '更新', '選', '開始', '讀檔畫面',
        '從劇本開始', '更新終態'
    ].forEach(function (方法) {
        山彥[方法] = function () {
            調用(方法, Array.prototype.slice.call(arguments));
        };
    });

    山彥.取檔 = function (回調) {
        調用('取檔', [], 回調);
    };

    山彥.狀態回調 = function (步進, 回調) {
        調用('狀態回調', [步進], 回調);
    };

    山彥.vue連接初始化 = function (回調) {
        調用('vue連接初始化', [], function (狀態) {
            合併Vue狀態(狀態);
            if (回調) {
                回調(狀態);
            }
        });
    };

    山彥.初始化 = function (回調) {
        調用('初始化', [], function (狀態) {
            合併Vue狀態(狀態);
            if (回調) {
                回調();
            }
        });
    };

    window.山彥 = 山彥;
})();
