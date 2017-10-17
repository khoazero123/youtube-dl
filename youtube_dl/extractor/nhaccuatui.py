# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_xpath
from ..utils import (
    xpath_text,
    int_or_none,
    str_or_none,
)
"""
python -m youtube_dl http://www.nhaccuatui.com/playlist/bai-hat-yeu-thich-khoazero123-dang-cap-nhat.wEBAgXwNPtMW.html -F --cookies "cookies/nhaccuatui.txt.txt"
python -m youtube_dl http://www.nhaccuatui.com/playlist/bai-hat-yeu-thich-khoazero123-dang-cap-nhat.wEBAgXwNPtMW.html -o "download/%(title)s - %(id)s.%(ext)s" -F --cookies "cookies/nhaccuatui.txt.txt"
"""
class NhacCuaTuiIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?nhaccuatui\.com/(?:bai-hat|album|playlist|video|user)/[^\.]+\.(?P<id>\w+)\.html'
    _TESTS = [{
        'url': 'http://www.nhaccuatui.com/bai-hat/yeu-di-dung-so-yeu-di-dung-so-ost-onlyc.J8kPKRvgBXEK.html',
        'info_dict': {
            'id': 'J8kPKRvgBXEK',
            'ext': 'mp3',
            'title': 'Yêu Đi Đừng Sợ (Yêu Đi Đừng Sợ OST) - OnlyC',
            'description': 'Bài hát: Yêu Đi Đừng Sợ (Yêu Đi Đừng Sợ OST) - OnlyC..Có một quá khứ phải cố quên mỗi khi kề bên.Và có một nỗi nhớ dần lớn lê',
            'thumbnail': r're:^https?://.*\.jpg$',
        }
    }, {
        'url': 'http://www.nhaccuatui.com/playlist/bai-hat-yeu-thich-khoazero123-dang-cap-nhat.wEBAgXwNPtMW.html',
        'info_dict': {
            'id': 'wEBAgXwNPtMW',
            'ext': 'mp3',
            'title': 'Album Bài hát yêu thích khoazero123',
        },
    }, {
        'url': 'http://www.nhaccuatui.com/user/khoazero123.nghe-nhac-cua-tui.html',
        'info_dict': {
            'id': 'nghe-nhac-cua-tui',
            'ext': 'mp3',
            'title': 'Album Bài hát yêu thích khoazero123',
        },
        'only_matching': True,
    }, {
        'url': 'http://www.nhaccuatui.com/video/giot-nuoc-mat-trong-mo-trung-quang.3Wbm11Y4529m5.html',
        'info_dict': {
            'id': '3Wbm11Y4529m5',
            'ext': 'mp4',
            'title': 'Giọt Nước Mắt Trong Mơ - Trung Quang',
            'description': 'Bai hat Giot Nuoc Mat Trong Mo  Trung Quang Cho mot ai trong moi giac mo dem ve Doi hinh Tai bai hat 320 Giọt Nước Mắt Trong Mơ Trung Quang |3Wbm11Y4529m5',
            'thumbnail': r're:^https?://.*\.jpg$',
        },
        'only_matching': True,
    }]
    def _extract_item(self, item, page_type, fatal=True):
        item = item
        formats = []

        title_item = item.find('title').text.strip()
        id_item = item.find('key').text.strip()
        creator_item = item.find('creator').text.strip()
        location_item = item.find('location').text.strip()
        kbit = int_or_none(item.find('kbit').text.strip())
        locationHQ_item = item.find('locationHQ').text.strip() # 320
        lossless_item = str_or_none(item.find('hasHQ').text.strip()) # lossless

        quality_item = 128
        #if kbit and not locationHQ_item:
            #pass
            #quality_item = int_or_none(kbit)

        f = {
            'format_id': str_or_none(quality_item),
            'url': location_item,
        }
        if page_type == 'video':
            f.update({
                'height': quality_item,
                'ext': 'mp4',
            })
        else:
            f.update({
                'abr': quality_item,
                'ext': 'mp3',
            })
        formats.append(f)

        if locationHQ_item:
            f = {
                'format_id': str_or_none(kbit),
                'url': locationHQ_item,
            }
            if page_type == 'video':
                f.update({
                    'height': quality_item,
                    'ext': 'mp4',
                })
            else:
                f.update({
                    'abr': quality_item,
                    'ext': 'mp3',
                })
            formats.append(f)
        if lossless_item == 'true':
            lossless_json = self._download_json('http://www.nhaccuatui.com/download/song/'+id_item+'_lossless', id_item, 'Downloading lossless JSON')
            if 'stream_url' in lossless_json['data']:
                f = {
                    'format_id': 'lossless',
                    'url': lossless_json['data']['stream_url'],
                }
                if page_type == 'video':
                    f.update({
                        'height': quality_item,
                        'ext': 'mp4',
                    })
                else:
                    f.update({
                        'abr': quality_item,
                        'ext': 'mp3',
                    })
                formats.append(f)

        return {
            'title': title_item,
            'id': id_item,
            'formats': formats,
        }


    def _real_extract(self, url):
        id = self._match_id(url)
        webpage = self._download_webpage(url, id)
        title = self._og_search_title(webpage)
        page_type = self._search_regex(r'https?://(?:www\.)?nhaccuatui\.com/([^\/]+)', url, 'page type', fatal=False)
        
        player_xml_url = self._search_regex([
            r'player.peConfig.xmlURL\s*=\s*"([^"]+)',
        ], webpage, 'player xml url')

        player_xml = self._download_xml(player_xml_url, id, 'Downloading file XML')
        items = player_xml.findall('./track')

        entries = []

        for i, item in enumerate(items, 1):
            entry = self._extract_item(item, page_type)
            if page_type == 'playlist':
                entries.append(entry)
            else:
                return entry

        return {
            '_type': 'playlist',
            'id': id,
            'title': title,
            'entries': entries,
        }