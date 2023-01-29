$(function() {
    console.log( "ready!" );


    $.ajax({
        type: "GET", 	        //Méthode à employer POST ou GET 
        url: "/api/v1/warehouses"
    }).done(function (output) {
        for ( var i = 0, l = output.length; i < l; i++ ) {
            $('#warehouse-name').append($('<option>', {
                value: output[i],
                text: output[i]
            }));
        }
    });

    

    $( "#form-tracking" ).submit(function( event ) {
        event.preventDefault();
        console.log($("#tracking-number").val());
        var tracking_number = $("#tracking-number").val();
        var warehouse = $('#warehouse-name').find(":selected").val();
        $.ajax({
            type: "POST", 	        //Méthode à employer POST ou GET 
            url: "/api/v1/simulate/change_warehouse?tracking-number="+tracking_number+"&warehouse="+warehouse
            //Cible du script coté serveur à appeler
        }).done(function (output) {
            //Code à jouer en cas d'éxécution sans erreur du script du PHP
            // Retrieve the package data from the database
            alert(output);
        }).fail(function (error) {
            //Code à jouer en cas d'éxécution en erreur du script du PHP ou de ressource introuvable
            var errorMessage = "Error: " + error;
            console.log(errorMessage);
            alert(errorMessage);
        });
    });

});