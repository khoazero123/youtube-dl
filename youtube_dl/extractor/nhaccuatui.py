# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_xpath
from ..utils import (
    xpath_text,
)

class NhacCuaTuiIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?nhaccuatui\.com/(?:bai-hat|album|playlist|video)/[^\.]+\.(?P<id>\w+)\.html'
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

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title = self._og_search_title(webpage)
        page_type = self._search_regex(r'https?://(?:www\.)?nhaccuatui\.com/([^\/]+)', url, 'page type', fatal=False)
        
        player_xml_url = self._search_regex([
            r'player.peConfig.xmlURL\s*=\s*"([^"]+)',
        ], webpage, 'player xml url')

        player_xml = self._download_xml(player_xml_url, video_id, 'Downloading file XML')
        item_element = player_xml.findall('./track')

        formats = []

        for item in item_element:
            creator = item.find('creator').text.strip()
            location = item.find('location').text.strip()
            f = {
                'format_id': '128',
                'url': location,
            }

            f.update({
                'abr': 128,
                'ext': 'mp3',
            })
            formats.append(f)
            
        return {
            'id': video_id,
            'title': title,
            'description': self._og_search_description(webpage),
            'formats': formats,
            'thumbnail': self._og_search_thumbnail(webpage),
        }