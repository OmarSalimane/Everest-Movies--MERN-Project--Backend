import { v2 as cloudinary} from "cloudinary"
import mediaModel from "../models/mediaModel.js"

// add media
const addMedia = async (req,res) => {
    try {
        const { name, description, category, subCategory, seasons, bestseller } = req.body

        const image1 = req.files.image1 && req.files.image1[0]
        const image2 = req.files.image2 && req.files.image2[0]
        const image3 = req.files.image3 && req.files.image3[0]
        const image4 = req.files.image4 && req.files.image4[0]

        const images = [image1, image2, image3, image4].filter((item)=> item !== undefined)

        let imagesUrl = await Promise.all(
            images.map(async (item) => {
                let result = await cloudinary.uploader.upload(item.path,{resource_type:'image'});
                return result.secure_url
            })
        )

        const mediaData = {
            name,
            description,
            category,
            subCategory,
            bestseller: bestseller === "true" ? true : false,
            seasons: JSON.parse(seasons),
            image: imagesUrl,
            date: Date.now()
        }

        console.log(mediaData);

        const media = new mediaModel(mediaData);
        await media.save()
        

        res.json({success:true, message:"Product Added"})
        
    } catch (error) {
        console.log(error);
        res.json({success:false, message:error.message})
    }
}

// list media
const listMedias = async (req,res) => {
    
}

// remove media
const RemoveMedia = async (req,res) => {
    try {
        await mediaModel.findByIdAndDelete(req.body.id)
        res.json({success:true,message:"Product Removed"})
    } catch (error){
        console.log(error);
        res.json({ success: false, message: error.message})
        
    }
}


// media info
const singleMedia = async (req,res) => {
    try {

        const { mediaId } = req.body
        const media = await mediaModel.findById(mediaId)
        res.json({success:true,media})
    } catch (error){
        console.log(error);
        res.json({ success: false, message: error.message})
    }
}

export {listMedias, addMedia, RemoveMedia, singleMedia} 