// This is for chat, message, review, and feedback features:

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
};

window.setTimeout(function() {
    window.location.reload(true);
}, 10000);

function chat(event, index, element) {
    if (event.which === 13 && !event.shiftKey) {
        event.preventDefault();
        element.blur();
        if (element.value != element.placeholder) {
            element.placeholder = element.value;
            let xhr = new XMLHttpRequest();
            xhr.open('POST', window.location.href + '/edit', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({
                msg: element.value,
                i: index
            }));
            document.getElementById('edited' + index).textContent = '(Edited)';
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
    while (document.getElementById("msg" + I) != null) {
        let _I = I;

        let ele = document.getElementById("msg" + _I);
        let deleteEle = document.getElementById("delete-msg" + _I);
        let editEle = document.getElementById("edit-msg" + _I);

        ele.addEventListener("keypress", (event) => chat(event, _I, ele));

        deleteEle.addEventListener("click", function(event) {
            let xhr = new XMLHttpRequest();
            xhr.open("POST", window.location.href + "/edit", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({
                msg: '',
                i: _I
            }));
            removeFadeOut(deleteEle.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, 1);
            deleteEle.parentElement.parentElement.parentElement.parentElement.remove();
        });

        editEle.addEventListener("click", function(event) {
            let D = document.getElementById("msg" + _I);
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

    document.getElementById("chat").addEventListener("submit", function(event) {
        let thisEle = document.getElementById("chat");
        thisEle.submit();
        thisEle.reset();
        return false;
    });
});

// This is for chat, message, review, and feedback features.
