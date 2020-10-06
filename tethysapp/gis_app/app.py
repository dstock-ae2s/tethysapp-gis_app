from tethys_sdk.base import TethysAppBase, url_map_maker


class GisApp(TethysAppBase):
    """
    Tethys app class for GIS Demo.
    """

    name = 'GIS Demo'
    index = 'gis_app:home'
    icon = 'gis_app/images/gis_multi.png'
    package = 'gis_app'
    root_url = 'gis-app'
    color = '#ac162c'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='gis-app',
                controller='gis_app.controllers.home'
            ),
            UrlMap(
                name='file_download_ajax',
                url='gis-app/file-download-ajax',
                controller='gis_app.ajax_controllers.file_download'
            ),
            UrlMap(
                name='file_upload_ajax',
                url='gis-app/file-upload-ajax',
                controller='gis_app.ajax_controllers.file_upload'
            ),
            UrlMap(
                name='csv_to_shapefile_ajax',
                url='gis-app/csv-to-shapefile-ajax',
                controller='gis_app.ajax_controllers.csv_to_shapefile'
            ),
        )

        return url_maps