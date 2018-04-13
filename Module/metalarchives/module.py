# -*- coding: utf-8 -*-

# Copyright(C) 2018  -  Quentin Def & Maxime G
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals
from weboob.capabilities.bands import CapBands, BandNotFound
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import Value, ValueBackendPassword
from weboob.capabilities.base import find_object

from .browser import MetalarchivesBrowser

__all__ = ['MetalarchivesModule']

class MetalarchivesModule(Module, CapBands):
    NAME = 'metalarchives'
    DESCRIPTION = 'Metal Archives: Encyclopedia Metallum'
    MAINTAINER = 'qdef'
    EMAIL = 'quentin.defenouillere@gmail.com'
    LICENSE = 'AGPLv3+'
    VERSION = '1.4'
    BROWSER = MetalarchivesBrowser
    
    CONFIG = BackendConfig(
        Value('login', label='Metal archives ID'),
        ValueBackendPassword('password', label='Metal archives password')
    )

    #Login credentials
    def create_default_browser(self, *args, **kwargs):
        return self.create_browser(self.config['login'].get(), self.config['password'].get(), *args, **kwargs)

    # Method to search for a band pattern:
    def iter_band_search(self, pattern):
        self.bands = list(self.browser.iter_band_search(pattern))
        # In case the city search returns no results:
        if not self.bands:
            raise BandNotFound('Sorry, no result matched your query.')
        return self.bands
    
    # Get the discography of a band:
    def get_albums(self, id):
        return self.browser.get_albums(id)
    
    # Method to retrieve the weather data for one specific city: 
    def get_info(self, id):
        return self.browser.get_info(id)
    
    # Method to retrieve you favorite bands:
    def get_favorites(self):
        return self.browser.get_favorites()
    
    def suggestions(self):
        return self.browser.suggestions(self.get_bands())
  
    def get_bands(self):
        bands = list(self.get_favorites())
        band_ids = []
        for band in bands:
            band_ids.append(band.id)
        return band_ids


    



    





