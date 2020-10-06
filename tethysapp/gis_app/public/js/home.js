/*
Function to upload input files to the user workspace
*/
function uploadFile(file_upload_id, file_name){
    console.log("Upload file js")
    var input_file=$(file_upload_id)[0].files;

    //Preparing data to be submitted via AJAX POST request
    var data = new FormData();
    data.append("file_name", file_name);
    for(var i = 0; i < input_file.length; i++){
        data.append("shapefile", input_file[i])
    }

    file_upload_process(file_upload_id, data);
};

/*
Helper function
Passes files without fields to the ajax to be uploaded to the user workspace
*/
function file_upload_process(file_upload_id, data){
    var file_upload = ajax_update_database_with_file("file-upload-ajax", data); //Submitting the data through the ajax function, see main.js for the helper function.
    file_upload.done(function(return_data){
        if("success" in return_data){
            var file_upload_button = $(file_upload_id);
            var file_upload_button_html = file_upload_button.html();
            file_upload_button.text('File Uploaded');
        };
    });
};

/*
Function to download file and show popup
*/
function downloadFile(){
    console.log("Download file js")
    var data = new FormData();
    data.append("file_name", "CSV_To_Shapefile");
    var file_download = ajax_update_database_with_file("file-download-ajax", data); //Submitting data through ajax, see main.js for helper function
    file_download.done(function(return_data){
        download_path = return_data.file_path;
        document.getElementById("myPopup").innerHTML = "File downloaded to " + download_path;
        $("#popup-modal").modal('show');
    });
}

/*
Function to convert csv to shapefile
*/
process_csv = function(data){
    $("#loading-modal").modal('show');
    var data = new FormData();
    data.append("file_name", "csv_file");

    csv_crs = document.getElementById('csv-crs').value;
    data.append("csv_crs", csv_crs);

    var csv_to_shapefile = ajax_update_database_with_file("csv-to-shapefile-ajax", data); //Submitting data through ajax, see main.js for helper function
    csv_to_shapefile.done(function(return_data){
        $("#loading-modal").modal('hide');

         //Show download files button
            document.getElementById("download_button").classList.remove("hideDiv");

            //Show and update map
            ol_map = TETHYS_MAP_VIEW.getMap();
            //Remove existing layers from map
            var layers = ol_map.getLayers();
            layers.forEach(function(layer){
                ol_map.removeLayer(layer);
            });
            ol_map.renderSync(); // Update the map

            // Style layer
            var none_style = [
                new ol.style.Style({
                    image: new ol.style.Circle({
                        stroke: new ol.style.Stroke({
                            color: '#A9A9A9',
                            width: 1,
                        }),
                        fill: new ol.style.Fill({
                            color: 'green',
                        }),
                        radius: 5
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#A9A9A9',
                        width: 1,
                    }),
                    fill: new ol.style.Fill({
                        color: 'green',
                    })
                }),
            ];

            // Create a geojson object holding features
            var geojson_object = {
                'type': 'FeatureCollection',
                'crs': {
                    'type': 'name',
                    'properties': {
                        'name': 'EPSG:3857'
                    }
                },
                'features': return_data.point_features
            };

            // Convert from geojson to openlayers collection
            var these_features = new ol.format.GeoJSON().readFeatures(geojson_object);

            // Create a new ol source and assign street features
            var none_vectorSource = new ol.source.Vector({
                features: these_features
            });

            // Create a new modifiable layer and assign source and style
            var none_layer = new ol.layer.Vector({
                name: 'CSV Points',
                source: none_vectorSource,
                style: none_style,
            });
            var basemap = new ol.layer.Tile({
                source: new ol.source.OSM(),
            });

            // Add streets layer to map
            ol_map = TETHYS_MAP_VIEW.getMap();
            ol_map.addLayer(basemap);
            ol_map.addLayer(none_layer);
            ol_map = TETHYS_MAP_VIEW.getMap();

            // Print Control
            var printControl = new ol.control.Print();
            ol_map.addControl(printControl);
            // On print save image file
            printControl.on('printing', function(e){
                $('body').css('opacity',  0.5);
            });
            printControl.on(['print', 'error'], function(e){
                $('body').css('opacity',  1);
                // Print success
                if(e.image){
                    e.canvas.toBlob(function(blob){
                        saveAs(blob, 'map.'+e.imageType.replace('image/', ''));
                    }, e.imageType);
                } else {
                    console.warn('No canvas to export');
                }
            });

            // Define a new legend
            var legend = new ol.control.Legend({
                title: 'Legend',
                margin: 5,
                collapsed: false
            });
            ol_map.addControl(legend);

            legend.addRow({
                title: 'CSV Point',
                typeGeom:'Point',
                style: new ol.style.Style({
                    image: new ol.style.Circle({
                        stroke: new ol.style.Stroke({
                            color: '#A9A9A9',
                            width: 1,
                        }),
                        fill: new ol.style.Fill({
                            color: 'green',
                        }),
                        radius: 5
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#A9A9A9',
                        width: 1,
                    }),
                    fill: new ol.style.Fill({
                        color: 'green',
                    })
                }),
            });

            select = new ol.interaction.Select();
            ol_map.addInteraction(select);

            // Add a popup overlay to the map
            var element = document.getElementById('popup');
            var popup = new ol.Overlay({
                element: element,
                positioning: 'bottom-center',
                stopEvent: false,
                offset:[0,-10],
            });
            ol_map.addOverlay(popup);
            ol_map.on('click', function(event){
                try{
                    var feature = ol_map.getFeaturesAtPixel(event.pixel)[0];
                } catch(err){}
                if(feature){
                    $(element).popover('destroy');
                    setTimeout(function(){
                        var coordinate = feature.getGeometry().getCoordinates();
                        popup.setPosition(coordinate);
                        popupContent = '<div class="point-popup">'+
                        '<p>Northing: '+feature.get('Northing')+'</p>'+
                        '<p>Easting: '+feature.get('Easting')+'</p>'
                        + '</div>';
                        $(element).popover({
                            container: element.parentElement,
                            html: true,
                            sanitize: false,
                            content: popupContent,
                            placement: 'top'
                        });
                        $(element).popover('show');
                    },500);
                } else {
                    $(element).popover('destroy');
                }
            })
            TETHYS_MAP_VIEW.zoomToExtent(return_data.extent) // Zoom to layer
            $("#loading-modal").modal('hide');
    });

}

$("#submit-csv").click(process_csv);

$(function(){

    console.log("In the function")

    $('#csv-input').change(function(){
        uploadFile('#csv-input', 'csv_file');
        console.log("In the upload file js")
    });

});
