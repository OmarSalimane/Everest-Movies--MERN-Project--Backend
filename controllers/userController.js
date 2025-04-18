import userModel from '../models/userModel.js';
import validator from "validator";
import bcrypt from "bcrypt";
import jwt from 'jsonwebtoken';

const createToken = (id) => {
    return jwt.sign({id},process.env.JWT_SECRET)
}

// LogIn
const loginUser = async (req,res) => {
    try {
        const {email,password} = req.body;
        const user = await userModel.findOne({email});

        if (!user) {
            return res.json({success:false, message:"User doesn't exist"})
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (isMatch) {
            const token = createToken(user._id)
            res.json({success:true, token})
        }
        else{
            res.json({success:false,message:'Invalid login details'})
        }
    } catch (error) {
        console.log(error);
        res.json({success:false, message:error.message})
    }
}


// Sign Up
const registerUser = async (req,res) => {
    try {
        const {name, email, password } = req.body;

        // check if user already exists
        const exists = await userModel.findOne({email})
        if (exists) {
            return res.json({success:false, message:"User already existing"})
        }

        // Valid email & strong password????
        if (!validator.isEmail(email)) {
            return res.json({success:false, message:"Enter a valid email address"})
        }
        if (password.length < 8) {
            return res.json({success:false, message:"Paassword must be at leat 8 characters long"})
        }

        // Hash password
        const salt = await bcrypt.genSalt(10)
        const hashedPassword = await bcrypt.hash(password,salt)

        const newUser = new userModel({
            name,
            email,
            password:hashedPassword
        })

        const user = await newUser.save()

        const token = createToken(user._id)

        res.json({success:true, token})

    } catch (error) {
        console.log(error);
        res.json({success:false, message:error.message})
    }
}

//Admin Login
const adminLogin = async (req,res) => {
    try {
        const {email,password} = req.body

        if(email === process.env.ADMIN_EMAIL && password === process.env.ADMIN_PASSWORD){
            const token = jwt.sign(email+password,process.env.JWT_secret);
            res.json({success:true,token})
        } else {
            res.json({success:false,message:"Invalid credetentials"})
        }
    } catch (error) {
        console.log(error);
        res.json({success:false, message:error.message})
    }
}

export { loginUser, registerUser, adminLogin} 