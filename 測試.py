import sys
import subprocess
from pathlib import Path

import unittest
from rimo_utils import good_open
import liber.core

from librian.librian本體.librian虛擬機 import 虛擬機環境, 讀者


根 = (Path(__file__)/'../../').resolve()
虛擬機環境.加載配置(根 / 'librian面板/librian面板/模板/潘大爺的模板')


class 全部測試(unittest.TestCase):
    maxDiff = None

    def test_編譯(self):
        with good_open(f'{虛擬機環境.工程路徑}/{虛擬機環境.配置["劇本入口"]}') as f:
            self.assertEqual(
                liber.core.load(f),
                [
                    {'縮進數': 0, '註釋': ' 背景來自pixiv_id=75399001的「無料背景素材[和風縁側]」。', '類型': '註釋'},
                    {'縮進數': 0, '註釋': ' 潘大爺的立繪來自https://k-after.at.webry.info', '類型': '註釋'}, {'縮進數': 0, '註釋': ' 音樂來自https://filmmusic.io，作者Kevin MacLeod，使用CC4條款。', '類型': '註釋', '之後的空白': 1},
                    {'縮進數': 0, '原文': 'BGM call-to-adventure', '函數': 'BGM', '參數表': [{'a': 'call-to-adventure'}], '類型': '函數調用'},
                    {'縮進數': 0, '原文': 'BG 和風縁側', '函數': 'BG', '參數表': [{'a': '和風縁側'}], '類型': '函數調用'},
                    {'縮進數': 0, '名': '潘大爺', '代': None, '特效': None, '顏': None, '語': '今天天氣不錯，\n去散步吧。', '類型': '人物對話'},
                    {'縮進數': 0, '類型': '旁白', '旁白': '潘大爺走了。'}, {'縮進數': 0, '鏡頭符號': '-', '內容': '潘大爺', '類型': '鏡頭'}, {'縮進數': 0, '類型': '旁白', '旁白': '然後就誰也沒有了。'}
                ]
            )

    def test_劇本(self):
        讀者實例 = 讀者.讀者(f'{虛擬機環境.工程路徑}/{虛擬機環境.配置["劇本入口"]}')
        self.assertEqual(
            list(讀者實例.迭代器()),
            [
                {'話語': '今天天氣不錯，\n去散步吧。', '名字': '潘大爺', '立繪': [{'使用png': True, '位置': [300, 0, 1], '特效': [], '名字': '潘大爺'}], '表情': None, '語者': '潘大爺', '背景': ('和風縁側.jpg', 1, '0% 0%', '_淡出'), '背景音樂': ('call-to-adventure.mp3', 1), '效果音': None, '插入圖': None, 'cg': None, '視頻': None, 'js': None, 'html': None, '選項': [], '特效表': {}, '額外信息': (), '源': [{'縮進數': 0, '註釋': ' 背景來自pixiv_id=75399001的「無料背景素材[和風縁側]」。', '類型': '註釋'}, {'縮進數': 0, '註釋': ' 潘大爺的立繪來自https://k-after.at.webry.info', '類型': '註釋'}, {'縮進數': 0, '註釋': ' 音樂來自https://filmmusic.io，作者Kevin MacLeod，使用CC4條款。', '類型': '註釋', '之後的空白': 1}, {'縮進數': 0, '原文': 'BGM call-to-adventure', '函數': 'BGM', '參數表': [{'a': 'call-to-adventure'}], '類型': '函數調用'}, {'縮進數': 0, '原文': 'BG 和風縁側', '函數': 'BG', '參數表': [{'a': '和風縁側'}], '類型': '函數調用'}, {'縮進數': 0, '名': '潘大爺', '代': None, '特效': None, '顏': None, '語': '今天天氣不錯，\n去散步吧。', '類型': '人物對話'}]},
                {'話語': '潘大爺走了。', '名字': '', '立繪': [{'使用png': True, '位置': [300, 0, 1], '特效': [], '名字': '潘大爺'}], '表情': '', '語者': '', '背景': ('和風縁側.jpg', 1, '0% 0%', '_淡出'), '背景音樂': ('call-to-adventure.mp3', 1), '效果音': None, '插入圖': None, 'cg': None, '視頻': None, 'js': None, 'html': None, '選項': [], '特效表': {}, '額外信息': (), '源': [{'縮進數': 0, '類型': '旁白', '旁白': '潘大爺走了。'}]},
                {'話語': '然後就誰也沒有了。', '名字': '', '立繪': [], '表情': '', '語者': '', '背景': ('和風縁側.jpg', 1, '0% 0%', '_淡出'), '背景音樂': ('call-to-adventure.mp3', 1), '效果音': None, '插入圖': None, 'cg': None, '視頻': None, 'js': None, 'html': None, '選項': [], '特效表': {}, '額外信息': (), '源': [{'縮進數': 0, '鏡頭符號': '-', '內容': '潘大爺', '類型': '鏡頭'}, {'縮進數': 0, '類型': '旁白', '旁白': '然後就誰也沒有了。'}]},
            ]
        )

    def test_main(self):
        for 跳過標題畫面 in ['True', 'False']:
            try:
                print([sys.executable, '-m', 'librian', '--project', 根 / 'librian面板/librian面板/模板/潘大爺的模板'])
                subprocess.run([sys.executable, '-m', 'librian', '--project', 根 / 'librian面板/librian面板/模板/潘大爺的模板', '--跳過標題畫面', 跳過標題畫面], timeout=3)
                self.fail()
            except subprocess.TimeoutExpired:
                pass


unittest.main()
