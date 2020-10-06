from django.http import JsonResponse, HttpResponse, Http404
from tethys_sdk.gizmos import *
from .utilities import *
import shutil
import geopandas as gpd
from shapely.geometry import Point
import fiona

def file_upload(request):
    print("File upload ajax")
    return_obj = {}

    if request.is_ajax() and request.method == 'POST':

        file_name = request.POST["file_name"]
        shapefiles = request.FILES.getlist('shapefile')

        move_files(shapefiles, file_name)

        return_obj['success'] = "success"

        return JsonResponse(return_obj)

#Function which copies file from user directory to user download folder
def file_download(request):
    print("File download ajax")
    return_obj = {}

    # Get source folder
    file_name = request.POST["file_name"]
    SHP_DIR = "/home/dstock/tethysdev/tethysapp-gis_app/tethysapp/gis_app/workspaces/user_workspaces/" + file_name + '/'

    # Get destination folder
    pathname = os.path.expanduser('~/Downloads/') + file_name + '/'

    #Copy source to destination
    try:
        print("First Try")
        shutil.copytree(SHP_DIR, pathname)
    except:
        print("File already downloaded")
        try:
            pathname = pathname[:-1]+'_copy/'
            shutil.copytree(SHP_DIR, pathname)
        except:
            print("File already downloaded")
            try:
                pathname = pathname[:-1] + '_copy/'
                shutil.copytree(SHP_DIR, pathname)
            except:
                print("File already downloaded")

    return_obj['file_path'] = pathname
    return JsonResponse(return_obj)

#Function which converts a csv file to a shapefile
def csv_to_shapefile(request):
    return_obj = {}

    file_name = request.POST["file_name"]
    csv_crs = request.POST["csv_crs"]
    csv_file = find_file(file_name, ".csv")
    csv_dataframe = gpd.read_file(csv_file)

    geometry = []
    for idx, row in csv_dataframe.iterrows():
        geometry.append(Point(float(csv_dataframe.loc[idx, 'Easting']), float(csv_dataframe.loc[idx, 'Northing'])))
    csv_dataframe.drop(['Northing', 'Easting'], axis=1)
    csv_dataframe = gpd.GeoDataFrame(csv_dataframe, crs=("EPSG:"+csv_crs), geometry=geometry)
    print(csv_dataframe.head())

    if not csv_dataframe.empty:
        mk_change_directory("CSV_To_Shp")
        csv_dataframe.to_file("CSV_To_Shp.shp")

        # Find bounds of final dataframe
        csv_dataframe = csv_dataframe.to_crs("EPSG:4326")
        this_bounds = csv_dataframe.total_bounds
        x1, y1, x2, y2 = this_bounds[0], this_bounds[1], this_bounds[2], this_bounds[3]
        this_extent = [x1, y1, x2, y2]
        return_obj["extent"] = this_extent

        # Convert all coordinates to EPSG:3857 for openlayers vector layer
        csv_dataframe = csv_dataframe.to_crs("EPSG:3857")
        # Export manhole flooding geojson in EPSG:3857
        csv_dataframe.to_file(filename=("CSV_To_Shp.geojson"), driver='GeoJSON')
        point_features = []
        if not os.stat(find_file("CSV_To_Shp", ".geojson")).st_size == 0:
            with fiona.open("CSV_To_Shp.geojson") as data_file:
                for data in data_file:
                    point_features.append(data)
                return_obj["point_features"] = point_features  # Return features in geojson format

    return JsonResponse(return_obj)