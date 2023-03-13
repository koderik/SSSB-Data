// rows is passed from html 
window.onload = function () {
    function updateAddress() {
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
        console.log(rows);
        const order = ["Rum i korridor", "1 rum & pentry", "2 rum & pentry", "3 rum & pentry", "1 rum & kök", "2 rum & kök", "3 rum & kök", "4 rum & kök"];

        rows = rows.map(([address, apartments]) => {
            const sortedApartments = apartments.sort((a, b) => order.indexOf(a[0]) - order.indexOf(b[0]));
            return [address, sortedApartments];
        });
        // Get the address container element from the DOM
        const addressContainer = document.getElementById("address-container");
        // Clear the container
        addressContainer.innerHTML = "";

        // Loop through each address in the rows array
        rows.forEach((addressData) => {
            // Create a new card element for the address
            // Create a new card element for the address
            const card = document.createElement("a");
            card.classList.add("block", "max-w-sm", "p-6", "bg-white", "border", "border-gray-200", "rounded-lg", "shadow", "hover:bg-gray-100", "dark:bg-gray-800", "dark:border-gray-700", "dark:hover:bg-gray-700");
            

            // Create a heading element for the address name
            const heading = document.createElement("h5");
            heading.classList.add("mb-2", "text-2xl", "font-bold", "tracking-tight", "text-gray-900", "dark:text-white");
            heading.innerText = addressData[0];

            // Create a paragraph element for the address information
            const paragraph = document.createElement("p");
            paragraph.classList.add("font-normal", "text-gray-700", "dark:text-gray-400");
            let apartmentInfo = "";
            addressData[1].forEach((apartmentData) => {
                // Create a string with the apartment size and average queue days, with a line break between each apartment data
                apartmentInfo += `${apartmentData[0]}: ${apartmentData[1]} days\n`;
            
            });
            paragraph.innerText = apartmentInfo;

            // Add the heading and paragraph to the card
            card.appendChild(heading);
            card.appendChild(paragraph);

            // Add the card to the address container
            addressContainer.appendChild(card);

        });
    }

    // Update the table every 10 minutes
    setInterval(updateAddress, 600000);
    // Update the table when the page loads
    updateAddress();
};
