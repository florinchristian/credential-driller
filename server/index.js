const express = require('express')
const app = express()
const http = require('http').createServer(app)
const multer = require('multer');
const fs = require('fs');

const storage = multer({dest: __dirname + '/uploads'});

app.get('/', (req, res) => {
    // console.log('Accessed / from', req.socket.remoteAddress);
    res.send('Server up');
});

app.post('/upload', storage.array('files', 20), (req, res) => {
    const ip = req.socket.remoteAddress.replace(/:/g, '-');

    for (var i in req.files) {
        let file = req.files[i];

        fs.readFile(file.path, 'utf-8', (err, data) => {
            if (err) {
                res.send('error');
                return;
            }

            fs.writeFile(__dirname + `\\data\\${ip}_${file.originalname}`, data, (err) => {
                // console.log('Downloaded', `${ip}\\${file.originalname}`);
                if (err) console.log(err);

                fs.rm(file.path, (err) => {
                    if (err) console.log(err);
                });
            });
        });
    }
    res.send('done');
});

http.listen(40389, () => console.log('Server started on port 40389'));