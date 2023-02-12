// rows is passed from html 
window.onload = function () {
    function updateTable() {

        // remove first and last character
        //rows = rows.substring(1, rows.length - 1);
        // fix &#34; to "
        rows = rows.replace(/&#34;/g, '"');
        // fix &#39; to '
        rows = rows.replace(/&#39;/g, "'");
        // fix &quot; to "
        rows = rows.replace(/&quot;/g, '"');
        // fix &apos; to '
        rows = rows.replace(/&apos;/g, "'");
        // fix &amp; to &
        rows = rows.replace(/&amp;/g, "&");

        rows = JSON.parse(rows);

        var table = document.getElementById("csv-table");
        //     <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        table.className = "w-full text-sm text-left text-gray-500 dark:text-gray-400";
        // add row for headers Address nth, n-1th, n-2th, n-3th, n-4th, n-5th, n-6th, n-7th, n-8th, n-9th, n-10th
        var header = table.insertRow();
        // add this css to header         <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        header.className = "text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400";
        var address = header.insertCell(0);
        // <th scope="col" class="px-6 py-3">
        address.className = "px-6 py-3";
        address.innerHTML = "Address";
        // add Type column to header
        var type = header.insertCell(1);
        // <th scope="col" class="px-6 py-3">
        type.className = "px-6 py-3";
        type.innerHTML = "Type";


        // var max_day = length of maximum array in rows[1]
        let max_day = 0;
        rows.forEach((row) => {
            max_day = Math.max(max_day, row[1].length);
        });

        // set header to   <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        for (var i = 0; i < max_day; i++) {
            
            var day = header.insertCell(i + 2);
            // <th scope="col" class="px-6 py-3">
            day.className = "px-6 py-3";

            var ordinal = i + 1;
            day.innerHTML = ordinal + (ordinal > 3 ? "th" : ordinal === 1 ? "st" : ordinal === 2 ? "nd" : "rd");
        }
        rows.reverse()
        //            <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"> for body

        for (var i = 0; i < rows.length; i++) {
            
            var row = table.insertRow();
            url = rows[i][2];
           
            //  <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            row.className = "px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 "
       
            // add href link to url in address column
            var address = row.insertCell(0);
            //                 <th scope="col" class="px-6 py-3">
            address.className = "px-6 py-3";
            address.innerHTML = '<a href="' + url + '">' + rows[i][0] + '</a>';
            // add column for type
            var type = row.insertCell(1);
            //                 <th scope="col" class="px-6 py-3">
            type.className = "px-6 py-3";
            var type_data = rows[i][3];
            // short_type = Korr if type_data contains  Korridor, else take the integer of the string and P if Pentry or K if Kök ex. 3P, 2K. Disregard case
            var short_type = type_data.includes("korridor") ? "Korr" : type_data.includes("pentry") ? type_data.substring(0, 1) +" & "+ "P" : type_data.substring(0, 1)+" & " + "K";

        
            type.innerHTML = short_type
            // Reverse the sub-array at index 1
            rows[i][1] = rows[i][1].reverse();
            for (var j = 0; j < rows[i][1].length; j++) {
                var day = row.insertCell(j + 2);
                //                 <th scope="col" class="px-6 py-3">
                day.className = "px-6 py-3";
                day.innerHTML = rows[i][1][j];
            }
            // fill in empty cells
            for (var j = rows[i][1].length; j < max_day; j++) {
                var day = row.insertCell(j + 2);
                //                 <th scope="col" class="px-6 py-3">
                day.className = "px-6 py-3";
                day.innerHTML = "";
            }
        }
        drawColor();

    }
    function search() {
        let searchTerm = document.getElementById("searchInput").value.toLowerCase();
        let table = document.getElementById("csv-table");
        let rows = table.getElementsByTagName("tr");

        // Loop through all table rows
        for (let i = 1; i < rows.length; i++) {
            let address = rows[i].getElementsByTagName("td")[0];
            let addressText = address.innerHTML.toLowerCase();

            if (addressText.indexOf(searchTerm) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
        drawColor();
    }
    function drawColor() {

       // of all visible rows, color every other row dbe7f6
        let table = document.getElementById("csv-table");
        let rows = table.getElementsByTagName("tr");
        // color the first row #dbe7f6
        rows[0].style.backgroundColor = "#dbe7f6";
        visiblerows = [];
        for (let i = 1; i < rows.length; i++) {
            if (rows[i].style.display == "") {
                visiblerows.push(rows[i]);
            }
        }
        // draw whole row with color
        for (let i = 0; i < visiblerows.length; i++) {
            if (i % 2 == 0) {
                visiblerows[i].style.backgroundColor = "";
            } else {
                visiblerows[i].style.backgroundColor = "#dbe7f6";
            }
        }
    }
    document.getElementById("searchInput").addEventListener("input", search);
    // Update the table every 10 minutes
    setInterval(updateTable, 600000);
    // Update the table when the page loads
    updateTable();
};