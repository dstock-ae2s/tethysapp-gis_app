
from django.shortcuts import render, reverse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import *

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    submit_csv = Button(
        display_text='Submit',
        name='submit-csv',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'id': 'submit-csv'},
    )

    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=3.5,
        maxZoom=18,
        minZoom=2
    )

    drawing_options = []

    # basemaps = ['OpenStreetMap',
    #             'CartoDB',
    #             'Stamen',
    #             'ESRI']

    MapView.old_version = '5.3.0'

    map_view = MapView(
        # height='100%',
        # width='100%',
        # controls=['ZoomSlider', 'Rotate', 'FullScreen',
        #           {'MousePosition': {'projection': 'EPSG:4326'}},
        #           {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[],
        view=view_options,
        basemap=None,
        draw=drawing_options
    )

    context = {
        'map_view': map_view,
        'submit_csv': submit_csv,
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'gis_app/home.html', context)