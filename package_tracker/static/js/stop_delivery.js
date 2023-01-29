$(function() {
    console.log( "ready!" );

    $( "#form-tracking" ).submit(function( event ) {
        event.preventDefault();
        console.log($("#tracking-number").val());
        $.ajax({
            type: "GET", 	        //Méthode à employer POST ou GET 
            url: "/api/v1/stop_delivery?tracking-number="+$("#tracking-number").val(),  //Cible du script coté serveur à appeler
            //Cible du script coté serveur à appeler
        }).done(function (output) {
            //Code à jouer en cas d'éxécution sans erreur du script du PHP
            // Retrieve the package data from the database
            var package_data = Package.query.filter_by(tracking_number=output).first()
            // Display the package status and time on the page
            $('#package_status').text(package_data.status)
            $('#package_time').text(package_data.time)
        }).fail(function (error) {
            //Code à jouer en cas d'éxécution en erreur du script du PHP ou de ressource introuvable
            var errorMessage = "Error: " + error;
            console.log(errorMessage);
            alert(errorMessage);
        }).always(function () {
        //Code à jouer après done OU fail quoi qu'il arrive
        });
    });

});