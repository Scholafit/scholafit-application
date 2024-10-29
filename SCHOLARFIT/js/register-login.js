import { signUp, login, updateUserProfile } from "./apiService.js"
import {saveToSessionStorage, getItemFromSessionStorage } from './utils.js'


export const submitRegistrationForm = () => {
    
    const registrationForm = document.getElementById('registration_form')
    if (registrationForm) {
        registrationForm.addEventListener('submit', async (evt) => {
            
            evt.preventDefault()
            const formData = new FormData(registrationForm)
            const data = {
                first_name: formData.get("firstname"),
                last_name: formData.get("lastname"),
                username: formData.get("username"),
                email: formData.get('Email'),
                password: formData.get('Password')
            }
    
            const response = await signUp(data)
            console.log(response)
            if (response.error && response.status !== 201) {
                const respData = response["data"]
                const errorData = response["error"]
                const message = errorData["code"]
                alert(message);
                return;
                // show form errors
            }
            
            const respData = response["data"]
            const user = respData["new_user"]
            const profle = respData["new_profile"]
            const userId = user["id"]
            const profileId = profle["id"]
            saveToSessionStorage("user", 
                {"userId": userId, 
                 "profileId": profileId,
                 "firstname": user.first_name,
                 "email": user.email})

            window.location.replace('/profile_customize.html')
            

        })
    }
} 

export const submitLoginForm = () => {
    
    const loginForm = document.getElementById('login_form')
    if (loginForm) {
        loginForm.addEventListener('submit', async (evt) => {
    
            evt.preventDefault()
            const formData = new FormData(loginForm)
            const data = {
                identifier: formData.get('identifier'),
                password: formData.get('password')
                //username: formData.get('email')
            }
    
            const response = await login(data)
            console.log(response)
            if (response.error && response.status !== 201) {
                const respData = response["data"]
                const errorData = response["error"]
                const message = errorData["code"]
                alert(message);
                return;
                // show form errors
            }
            
            const respData = response["data"]
            const user = respData["user"]
            const profile = user.profile_data
            const userId = user["id"]
            const profileId = profile["id"]
            saveToSessionStorage("user", 
                                {"userId": userId, 
                                 "profileId": profileId,
                                 "firstname": user.first_name,
                                 "email": user.email})
            window.location.replace('/dashboard.html')
            

        })
    }
} 

export const updateProfile = () => {
    // add guard clause that user and profileId are present
    const user = getItemFromSessionStorage("user")
    const profileId = user["profileId"]
    const profileForm = document.getElementById('profile-form')
    if (profileForm){
        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault()
            const formData = new FormData(profileForm)
            const selectedSubjects = []
            for (let[key, value] of formData.entries()){
                if (key === 'subjects'){
                    selectedSubjects.push(value)
                }
            }
            if (selectedSubjects.length > 4){
                // add better error handling here
                return
            }
            const data = {
                profile_data: {
                    desired_course: formData.get('course'),
                    university_choices: formData.get('uni'),
                    expected_graduation_year: formData.get('grad').slice(0,4),
                    school_name: formData.get('school')
                },
                subject_data: selectedSubjects
            }
            const response = await updateUserProfile(profileId,data)
            if (response.status === 401){
                // profile does not exist create or login
                window.location.replace('/login.html')
            }
            if (response.status === 500){
                window.location.href="/500.html"
            }
            if (response.status === 404){
                console.log(response)
            }

            window.location.replace('/dashboard.html')
            
        })
    }
}