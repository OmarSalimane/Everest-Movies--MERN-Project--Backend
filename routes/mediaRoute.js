import express from 'express'
import {listMedias, addMedia, RemoveMedia, singleMedia}  from '../controllers/mediaController.js'
import upload from '../middleware/multer.js';
import adminAuth from '../middleware/adminAuth.js';

const mediaRouter = express.Router();

mediaRouter.post('/add',adminAuth,upload.fields([{name:'image1', maxCount:1}, {name:'image2', maxCount:1}, {name:'image3', maxCount:1}, {name:'image4', maxCount:1}]),addMedia);
mediaRouter.post('/remove',adminAuth,RemoveMedia);
mediaRouter.post('/single',singleMedia);
mediaRouter.get('/list',listMedias);

export default mediaRouter