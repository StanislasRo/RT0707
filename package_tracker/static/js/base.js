$(function() {
    console.log( "ready!" );

    $( "#form-tracking" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            type: "GET", 	        //Méthode à employer POST ou GET 
            url: "/api/v1/????",  //Cible du script coté serveur à appeler 
            beforeSend: function () {
              //Code à appeler avant l'appel ajax en lui même
            }
        }).done(function (output) {
        //Code à jouer en cas d'éxécution sans erreur du script du PHP
        }).fail(function (error) {
        //Code à jouer en cas d'éxécution en erreur du script du PHP ou de ressource introuvable
        }).always(function () {
        //Code à jouer après done OU fail quoi qu'il arrive
        });
    });

});