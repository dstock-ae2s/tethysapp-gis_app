from django.http import JsonResponse, HttpResponse, Http404
import os
import glob


"""
Function to make a directory if it does not exist and change directories
"""
def mk_change_directory(file_name):
    SHP_DIR = "/home/dstock/tethysdev/tethysapp-gis_app/tethysapp/gis_app/workspaces/user_workspaces/" + file_name + '/'
    SHP_DIR = os.path.join(SHP_DIR, '')
    try:
        os.mkdir(SHP_DIR)
    except OSError:
        print("Creation of the directory %s failed" % SHP_DIR)
    else:
        print("Successfully created the directory %s " % SHP_DIR)
    os.chdir(SHP_DIR)

"""
Function to move files to user workspace
"""
def move_files(shapefile, file_name):
    SHP_DIR = '/home/dstock/tethysdev/tethysapp-gis_app/tethysapp/gis_app/workspaces/user_workspaces/' + file_name + '/'

    mk_change_directory(file_name)

    # Remove existing files in directory
    files = glob.glob(SHP_DIR + '*')
    for f in files:
        os.remove(f)

    # Iterate over files and add to user workspace
    for f in shapefile:
        f_name = f.name
        f_path = os.path.join(SHP_DIR, f_name)

        with open(f_path, 'wb') as f_local:
            f_local.write(f.read())

    return JsonResponse({"success": "success"})

"""
Function to find file of specified file type in directory
"""
def find_file(file_name, ending):
    SHP_DIR = "/home/dstock/tethysdev/tethysapp-gis_app/tethysapp/gis_app/workspaces/user_workspaces/" + file_name + '/'
    for file in os.listdir(SHP_DIR):
        # Reading the output shapefile only
        if file.endswith(ending):
            file_path = os.path.join(SHP_DIR, file)
            return file_path