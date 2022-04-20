//cashing

//cash with one by one assets
const cashName = 'djangopwa-v1';
const cashAssets = [
    '',
    '/base_layout',
    '/static/js/idb.js',
    '/static/js/idbop.js',
    '/createpost',
]


//call install events
self.addEventListener('install', (e) => {
    console.log('service worker is installlled....')

    //wait until get rid of serviceworker
    e.waitUntil(
        //caches API
        caches.open(cashName).then(cache => {
            console.log('CACHING FILES BROOO!')
            cache.addAll(cashAssets)
        }).then(() => self.skipWaiting())
    );
});

//call activate events
self.addEventListener('activate', (e) => {
    console.log('service worker is activated....')

    //get rid of unwanted caches
    e.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== cashName) {
                        console.log('service worker clearing old caches');
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

//main sync event to run background sync
self.addEventListener('sync', function (event) {
    if (event.tag === 'sync-messages') {
        console.log('SYNC is running Broooooo!...');
        event.waitUntil(syncdatafun());
    } else {
        window.alert('sync didnt worked broooo!');
    }
});

//call fetch event offline mode
self.addEventListener('fetch', e => {
    console.log('Service Worker Fetching...');
    e.respondWith(
        fetch(e.request).catch(() => caches.match(e.request))
    )

})

//-----------------------------------------------------


//function to sync the data from indexeddb
function syncdatafun() {

    console.log('SYNC DATA FUNCTION FIRED.....')

    var request = indexedDB.open('ProductDB', 1);

    request.onsuccess = function (e) {
        // e.target.result has the connection to the database
        let dbd = e.target.result;

        console.log(dbd);
        console.log("DB Opened!" + `${dbd}`);

        let transaction = dbd.transaction("product", "readwrite");
        // Access an object store
        let articles = transaction.objectStore("product");
        const request = articles.openCursor();
        request.onsuccess = e => {
            const cursor = e.target.result
            if (cursor) {
                //alert(`ID: ${cursor.key} Topics: ${cursor.value.text} `)
                console.log(`indexeddb data : keys: ${cursor.key} and values: ${cursor.value.text}`);
                sendDataToServer(cursor.value, cursor.key);
                console.log('daaaaataaa---->>>', cursor.value)
                cursor.continue()
            }
        }
        request.onerror = function (error) {
            console.error('IndexedDB error:', error)
        }

        // order sent to the server
        function sendDataToServer(data, index) {
            fetch('/createpost', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {"X-CSRFToken": '{{csrf_token}}'}
            }).then((response) => {
                if (response) {
                    console.log(`delete data here... ${index}`)
                    deleteFromIndexdb(index)
                }
            });
        }

    }

    request.onerror = function (e) {
        console.log(e);
    };


}

// delete data from indexedb, that sent to server
function deleteFromIndexdb(index) {
    var indexedDBOpenRequest = indexedDB.open('ProductDB', 1)
    indexedDBOpenRequest.onsuccess = function () {
        let db = this.result
        let transaction = db.transaction("product", "readwrite");
        let storeObj = transaction.objectStore("product");
        storeObj.delete(index)
        console.log('data successfully deleted...')
    }
}
