import express from 'express'
import cors from 'cors'
import 'dotenv/config'
import connectDB from './config/mongodb.js'
import connectCloudinary from './config/cloudinary.js'
import userRouter from './routes/userRoute.js'
import mediaRouter from './routes/mediaRoute.js'

// App configuration

const app = express()
 const port = process.env.PORT || 4000
 connectDB()
 connectCloudinary()

 // Middlewares

 app.use(express.json())
 app.use(cors())

 // API endpoints

 app.use('/api/user', userRouter)
 app.use('/api/media', mediaRouter)

 app.get('/', (req,res)=>{
    res.send("API WORKING")
 })

 app.listen(port, ()=> console.log('Server started on PORT : '+ port))