"use strict";


(async function () {/*STAR NAČIN:
    function makeRequest(url, callback) {
        var httpRequest = new XMLHttpRequest();

        httpRequest.onreadystatechange = () => stateChangeHandler(httpRequest, callback)

        httpRequest.open("GET", url);
        httpRequest.send()
    }

    function stateChangeHandler(request, callback) {
        console.log(request.readyState);
        if (request.readyState == XMLHttpRequest.DONE) {
            if (request.status == 200) {
                callback(request.response)
            } else{
                console.error("Problem with request")
            }
        }
    }

    makeRequest("http://catfact.ninja/fact", (response) => {
        console.log(response)
    })*/

    /*    KRAJŠI NAČIN:
        function errorHandler(error) {
                console.error("Request failed", error)
            }

        var fetch_cat_fact = fetch("https://catfact.ninja/fact")

        console.log(fetch_cat_fact)

        fetch_cat_fact
            .then(response => response.text())
            .then(function (text) {
                console.log(text)
            })
            .catch(errorHandler)*/

    var response = await fetch("https://catfact.ninja/fact")
    var fact = await response.json()

    console.log(fact)

})()
