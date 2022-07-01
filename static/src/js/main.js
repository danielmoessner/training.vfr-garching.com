import Alpine from 'alpinejs'
import './lazyimages'
import {orderBy, shuffle} from 'lodash';

import intersect from '@alpinejs/intersect'

Alpine.plugin(intersect)

setTimeout(
    () => document.documentElement.style.setProperty('--scrollbar-width', (window.innerWidth - document.documentElement.clientWidth) + "px"),
    2000
);

window._orderBy = orderBy;
window._shuffle = shuffle;

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

window.getCookie = getCookie

window.Alpine = Alpine

Alpine.start()


