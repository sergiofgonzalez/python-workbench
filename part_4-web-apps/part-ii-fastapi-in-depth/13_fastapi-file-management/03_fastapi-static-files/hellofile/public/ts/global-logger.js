"use strict";
class GlobalLogger {
    static logEmailsToConsole() {
        for (const email of CONTACT_EMAIL_ARRAY) {
            console.log(`found contact:`, email);
        }
    }
}
window.addEventListener('load', () => {
    console.log(`Window is loaded!`);
    GlobalLogger.logEmailsToConsole();
    sendCrossOriginRequest();
});
// console.log(`What am i doing?`);
// interface OpenLibraryAuthor {
//   personal_name: string;
//   photos: number[];
// }
// const xhr = new XMLHttpRequest();
// const showData = () => {
//   if (xhr.status !== 200) {
//     console.log(`ERROR: could not retrieve data: ${ xhr.status }: ${ xhr.statusText }`);
//   } else {
//     const response: OpenLibraryAuthor = JSON.parse(xhr.response);
//     const body = document.querySelector('body');
//     const image = document.createElement('img');
//     image.src = `http://covers.openlibrary.org/a/id/${ response.photos[0] }-M.jpg`;
//     body?.appendChild(image);
//     const name = document.createElement('h1');
//     name.textContent = response.personal_name;
//     body?.appendChild(name);
//   }
// };
// xhr.onload = showData;
// const url = 'https://openlibrary.org/authors/OL9388A.json';
// xhr.open('GET', url);
// const xhr = new XMLHttpRequest();
// function requestListener() {
//   console.log(xhr.responseText);
// }
// xhr.addEventListener('load', requestListener);
// xhr.open('GET', 'http://www.example.com');
// xhr.send();
async function sendCrossOriginRequest() {
    console.log(`Sending cross origin request`);
    const response = await fetch('http://localhost:5000/allow-cors', { mode: 'cors' });
    const contents = await response.json();
    console.log(contents);
}
//# sourceMappingURL=global-logger.js.map