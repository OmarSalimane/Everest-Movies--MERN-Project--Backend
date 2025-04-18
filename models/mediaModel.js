import mongoose from 'mongoose';

const mediaSchema = new mongoose.Schema({
    name:{type:String, required:true},
    description: {type:String, required:true},
    image: {type:Array, required:true},
    category: {type:String, required:true},
    subCategory: {type:String, required:true},
    seasons: {type:Array, required:true},
    bestseller: {type:Boolean},
    date: {type:Number, required:true},
})

const mediaModel = mongoose.models.media || mongoose.model("media", mediaSchema);

export default mediaModel;