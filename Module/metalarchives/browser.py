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
from weboob.browser import URL, LoginBrowser, need_login
from .pages import BandPage, SearchBandsPage, LoginPage, FavoritesPage, SuggestionsPage, AlbumPage

__all__ = ['MetalarchivesBrowser']

class MetalarchivesBrowser(LoginBrowser):
    """
    Browsing the Metal Archives website.
    """
    
    BASEURL = 'https://www.metal-archives.com/'
    login = URL('authentication/login', LoginPage)
    bands = URL('search/ajax-band-search/\?field=name&query=(?P<pattern>.*)', SearchBandsPage)
    band = URL('bands/Band/(?P<band_id>.*)', BandPage)
    albums = URL('band/discography/id/(?P<band_id>.*)/tab/all', AlbumPage)
    favorites = URL('bookmark/ajax-list/type/band\?sEcho=1', FavoritesPage)
    suggested = URL('band/ajax-recommendations/id/(?P<band_id>.*)\?showMoreSimilar=1', SuggestionsPage)
    
    
    def iter_band_search(self, pattern):
        return self.bands.go(pattern=pattern).iter_bands()
    
    def get_albums(self, id):
        return self.albums.go(band_id=id).iter_albums()
    
    def get_info(self, id):
        return self.band.go(band_id=id).get_info()
    
    @need_login
    def get_favorites(self):
        return self.favorites.go().iter_favorites()
    
    @need_login
    def get_suggestions(self, bands):
        return self.suggested.go().iter_suggestions()

    @need_login
    def suggestions(self, bandlist):
        """
        Offers band suggestions depending on your music preferences.
        """
        suggestion_list = []
        for band in bandlist:
            # Gets all the similar artists of your favorite bands:
            suggestion_list += self.suggested.go(band_id=band).iter_suggestions()
        
        Suggestions = {}
        Bands = {}
        for suggestion in suggestion_list:
            if suggestion.id not in bandlist:
                # Adds the similar artist to the Suggestions dictionary if it is not already in the favorite bands:
                    if suggestion.url not in Suggestions:
                        # Creates a counter for each new similar artist in the Suggestions:
                        Suggestions[suggestion.url] = 1
                        Bands[suggestion.url] = suggestion
                    else:
                        # Increments '+1' if the similar artist is already in the Suggestions:
                        Suggestions[suggestion.url] += 1

        final_list = []
        while len(final_list) != 13: # This maximum can be modified if you want more or less suggestions
            best_suggestion = max(Suggestions, key = Suggestions.get)
            final_list.append(Bands.get(best_suggestion))
            Suggestions.pop(best_suggestion)
        
        # The top 13 similar artists to your favorite bands!
        return final_list

    def do_login(self):
        d = {'loginUsername': self.username,
                'loginPassword': self.password}
        self.login.go(data=d)            


