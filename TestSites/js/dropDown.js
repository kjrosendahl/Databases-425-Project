var products = ["Laptop","Raspberry Pi","Clock","USB 3.0 Cord","USB 2.0 Cord","Lightning Cable","USB Charger","Aux Cord","Monitor","Keyboard","Computer Mouse","Live Mouse (Only 4 Left in Stock)","Headphones","Earbuds","Air Pods","iPhone","Android Phone","Windows Phone","Rotary Phone","Flashdrive","Floppy Disk","All Dogs Go To Heaven 2","USB Microphone","USB Web Camera","Calculator","Desk Lamp","Power Strip","RAM","RAM (Download Code)","HDMI Cable","DisplayPort Cable"];


const QUESTION_VALUE = "question_value";

/**
 * Takes care of autocomplete items
 * @param inp The text field element
 * @param arr The list of possible autocomplete items
 */
function autoComplete(inp, arr) {
    // The element containing the autocompleted lists
    const activeElements = document.createElement("DIV");
    // Configure the activeElements
    activeElements.setAttribute("id", "autocomplete-list");
    activeElements.setAttribute("class", "autocomplete-items");
    // Append that element as a child of the autocomplete container 
    inp.parentElement?.appendChild(activeElements);
    // Index of the current item focused on
    var currentFocus;
    // Execute a function when someone writes in the text field
    inp.addEventListener("input", function (e) {
        // Construct the searchQuery
        let searchQuery = new RegExp(this.value.toLowerCase(), 'g');
        // Close any already open lists of autocompleted values
        closeAllLists();
        // If there is no search query, don't show results
        currentFocus = 0;
        if (this.value == "") {
            addSearchDiv(arr[0],[],0);
            for (let i = 1; i < arr.length; i++) {
                addSearchDiv(arr[i],[],i)
            }
            addActive()
            return;
        }
        let exactMatches = [];
        let searchMatchesBegin = []; // query item, indexes
        let searchMatchesRandom = [];
        // For each item in the tempListay...
        for (let i = 0; i < arr.length; i++) {
            // Search through the entire string for the input value
            let temp = arr[i].toLowerCase().matchAll(searchQuery);
            let matches = [];
            let b = temp.next();
            while (!b.done) {
                matches.push(b.value.index ?? 0);
                b = temp.next();
            }
            if (matches.length > 0) {
                let found = false;
                for (let j = 0; j < matches.length; j++) {
                    if (matches[j] == 0 || arr[i][matches[j] - 1] == " ") {
                        found = true;
                        break;
                    }
                }
                if (this.value.toLowerCase() == arr[i].toLowerCase()) {
                    exactMatches.push([arr[i], matches, i]);
                }
                else if (found) {
                    searchMatchesBegin.push([arr[i], matches, i]);
                }
                else {
                    searchMatchesRandom.push([arr[i], matches, i]);
                }
            }
        }
        // If there are no results, cancel
        if (searchMatchesRandom.length == 0 && searchMatchesBegin.length == 0 && exactMatches.length == 0) {
            addQuestionDiv();
            addActive();
            return false;
        }
        for (let i = 0; i < exactMatches.length; i++) {
            addSearchDiv(exactMatches[i][0], exactMatches[i][1], exactMatches[i][2]);
        }
        for (let i = 0; i < searchMatchesBegin.length; i++) {
            addSearchDiv(searchMatchesBegin[i][0], searchMatchesBegin[i][1], searchMatchesBegin[i][2]);
        }
        for (let i = 0; i < searchMatchesRandom.length; i++) {
            addSearchDiv(searchMatchesRandom[i][0], searchMatchesRandom[i][1], searchMatchesRandom[i][2]);
        }
        addActive();
    });
    // Call a function when someone presses a key on the keyboard
    inp.addEventListener("keydown", function (e) {
        if (activeElements.firstChild) {
            if (e.code == "ArrowDown") {
                e.preventDefault();
                // DOWN key, increase focus
                removeActive();
                currentFocus++;
                addActive();
            }
            else if (e.code == "ArrowUp") {
                e.preventDefault();
                // UP key, decrease focus
                removeActive();
                currentFocus--;
                addActive();
            }
            else if (e.code == "Enter" || e.code == "NumpadEnter") {
                // ENTER key, prevent form being submitted
                e.preventDefault();
                // And update the input field if needed
                if (currentFocus > -1) {
                    let entry = activeElements.getElementsByTagName("div")[currentFocus].getElementsByTagName("input")[0].name;
                    if (entry == QUESTION_VALUE) {
                        questionClicked();
                    }
                    else {
                        inp.value = activeElements.getElementsByTagName("div")[currentFocus].getElementsByTagName("input")[0].name;
                        itemSelected(activeElements.getElementsByTagName("div")[currentFocus].getElementsByTagName("input")[0].getAttribute('indexNumber'), arr);
                    }
                    // CLose the lists of autocompleted values
                    closeAllLists();
                }
            }
        }
    });
    function addSearchDiv(item, matches, index) {
        // Create a DIV element for the matching search
        let a = document.createElement("DIV");
        a.innerHTML = "";
        // Make the matching letters bold
        let cursor = 0;
        for (let j = 0; j < matches.length; j++) {
            a.innerHTML += item.slice(cursor, matches[j]) + "<strong>" + item.substr(matches[j], inp.value.length) + "</strong>";
            cursor = matches[j] + inp.value.length;
        }
        // Add the remaining part of the strign
        a.innerHTML += item.substr(cursor);
        // Insert a hidden input field that will hold the current array item's value
        a.innerHTML += "<input type='hidden' name='" + item + "' indexnumber='" + index + "'>";
        // Call a function when someoen clicks on this DIV element
        a.addEventListener("click", function (e) {
            // Insert the value fo rthe autocomplete text field
            inp.value = item;
            itemSelected(index, arr);
            // CLose the lists of autocompleted values
            closeAllLists();
        });
        activeElements.appendChild(a);
    }
    function addQuestionDiv() {
        let a = document.createElement("DIV");
        a.innerHTML = "<i>Not in database, sorry</i>";
        // Insert a hidden input field that will hold the current array item's value
        a.innerHTML += "<input type='hidden' name='" + QUESTION_VALUE + "'>";
        a.classList.add("question-div");
        activeElements.appendChild(a);
    }
    /**
     * Close all autocompleted list items
     */
    function closeAllLists() {
        while (activeElements.lastChild) {
            activeElements.removeChild(activeElements.lastChild);
        }
    }
    function addActive() {
        let eles = activeElements.getElementsByTagName("DIV");
        if (currentFocus >= eles.length)
            currentFocus = 0;
        if (currentFocus < 0)
            currentFocus = eles.length - 1;
        // Add the active class "autocomplete-active"
        eles[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive() {
        activeElements.getElementsByTagName("DIV")[currentFocus].classList.remove("autocomplete-active");
    }
}

