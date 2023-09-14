import globals from "./globals";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function getImages() {
    return fetch(globals.IMAGES_API)
        .then(response => response.json())
        .then(data => data);
}

export function postImage(body) {
    return fetch(globals.IMAGES_API, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: body
    }).then(response => response.json())
}