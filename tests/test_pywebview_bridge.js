const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const bridgePath = path.join(__dirname, '../librian/librian本體/前端/pywebview橋.js');
const bridge = fs.readFileSync(bridgePath, 'utf8');

function loadBridge(search, api) {
    const window = {
        location: { search },
        pywebview: { api },
        addEventListener() {},
    };
    vm.runInNewContext(bridge, { window, URLSearchParams, Promise, Proxy, Array });
    return window.山彥;
}

async function main() {
    const calls = [];
    const api = {
        slow() {
            calls.push('slow:start');
            return new Promise(resolve => setTimeout(() => {
                calls.push('slow:end');
                resolve();
            }, 10));
        },
        fail() {
            calls.push('fail');
            return Promise.reject(new Error('expected'));
        },
        fast() {
            calls.push('fast');
            return Promise.resolve();
        },
    };
    const 山彥 = loadBridge('?_librian_webview=1', api);

    const results = await Promise.allSettled([山彥.slow(), 山彥.fail(), 山彥.fast()]);

    assert.deepStrictEqual(calls, ['slow:start', 'slow:end', 'fail', 'fast']);
    assert.deepStrictEqual(results.map(result => result.status), ['fulfilled', 'rejected', 'fulfilled']);
    assert.strictEqual(loadBridge('', api), undefined);
    console.log('pywebview bridge tests passed');
}

main().catch(error => {
    console.error(error);
    process.exitCode = 1;
});
