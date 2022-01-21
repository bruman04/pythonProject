// Done by Ng Rong Kai:

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
};

window.setTimeout(function() {
    window.location.reload(true);
}, 60000);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function feedback(event, index, element, force) {
    if (force || (event.which === 13 && !event.shiftKey)) {
        element = document.getElementById("rvw" + index);
        element.blur();
        if (force || (element.value != element.placeholder)) {
            element.placeholder = element.value;
            let xhr = new XMLHttpRequest();
            xhr.open("POST", window.location.href + "/edit", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            setTimeout(function() {
                xhr.send(JSON.stringify({
                    i: index,
                    rvw: element.value,
                    stars: document.querySelector("input[name='stars" + index + "']:checked").value
                }));
                if (force) {
                    setTimeout(function() {
                        window.location.reload();
                    }, 100);
                };
            }, 100);
            document.getElementById("edited" + index).textContent = "(Edited)";
        };
        if (element.value.trim() === '') {
            element.parentElement.parentElement.remove();
        };
    };
};

function removeFadeOut(elem, seconds) {
    elem.style.transition = "opacity " + seconds + "s ease";
    elem.style.opacity = 0;
    setTimeout(function() {
        elem.remove();
    }, seconds * 1000);
};

window.addEventListener("load", function() {
    let I = 0;
    while (document.getElementById("rvw" + I) != null) {
        let _I = I;

        let ele = document.getElementById("rvw" + _I);
        let deleteEle = document.getElementById("delete-rvw" + _I);
        let editEle = document.getElementById("edit-rvw" + _I);

        ele.addEventListener("keypress", (event) => feedback(event, _I, ele, false));

        deleteEle.addEventListener("click", function(event) {
            let xhr = new XMLHttpRequest();
            xhr.open("POST", window.location.href + "/edit", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({
                i: _I
            }));
            removeFadeOut(deleteEle.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, 1);
            deleteEle.parentElement.parentElement.parentElement.parentElement.remove();
        });

        editEle.addEventListener("click", function(event) {
            let D = document.getElementById("rvw" + _I);
            D.focus();
            D.select();
        });

        I++;
    };

    document.getElementById("text").addEventListener("keypress", function(event) {
        if (event.which === 13 && !event.shiftKey) {
            event.target.form.dispatchEvent(new Event(
                "submit", {
                    cancelable: true
                }
            ));
            event.preventDefault();
        }
    });

    document.getElementById("review").addEventListener("submit", function(event) {
        let thisEle = document.getElementById("review");
        thisEle.submit();
        thisEle.reset();
        return false;
    });
});

// Done by Ng Rong Kai.
