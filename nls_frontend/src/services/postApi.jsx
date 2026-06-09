export const post_contact = async (formData) =>{
    try{
        const response = await fetch("http://127.0.0.1:8000/contact/",{
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body:JSON.stringify(formData)
        });
        return await response.json();
    }
    catch(err){
        console.log(err);
    }
} 
