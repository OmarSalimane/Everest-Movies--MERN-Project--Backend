import mongoose from 'mongoose'

const connectDB = async () => {

    mongoose.connection.on('connected',()=> {
        console.log("MongoDB Connected");
    })
    
    await mongoose.connect(`${process.env.MONGODB_URI}/everestmovies`)

}

export default connectDB;