# coding: utf-8
from __future__ import unicode_literals

import re
import os
from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
    update_url_query,
    urlencode_postdata,
)
class FshareIE(InfoExtractor):
    # password
    _VALID_URL = r'https?://(?:www.)?fshare\.vn/(?:file|folder)/(?P<id>[^\/]+)'
    _TESTS = [{
        'url': 'https://www.fshare.vn/file/VE3W2B39OHZB',
        'info_dict': {
            'id': 'VE3W2B39OHZB',
            'title': 'INF 203 V5.docx',
            'ext': 'docx'
        },
    }, {
        'url': 'https://www.fshare.vn/file/VE3W2B39OHZB',
        'only_matching': True,
    }]
    IE_NAME = 'fshare'
    IE_DESC = 'fshare.vn'

    def _real_extract(self, url):
        fileid = self._match_id(url)
        webpage = self._download_webpage(url, fileid)
        title = self._search_regex(r'<title>([^>]+)</title>', webpage, 'title', fatal=False).replace('Fshare - ', '')
        filename, file_extension = os.path.splitext(title) #[1][1:]
        
        form = self._hidden_inputs(webpage)
        fs_csrf = form.get('fs_csrf', None)
        linkcode = form.get('DownloadForm[linkcode]', None)
        if fs_csrf and linkcode:
            response = self._download_json(
                'https://www.fshare.vn/download/get', None, data=urlencode_postdata({
                    'fs_csrf': fs_csrf,
                    'DownloadForm[pwd]': '',
                    'DownloadForm[linkcode]': linkcode,
                    'ajax': 'download-form',
                }), headers={'Referer': url})
            fileurl = response.get('url', None)
        return {
            'id': fileid,
            'title': filename,
            'url': fileurl,
            'ext': file_extension
        }
