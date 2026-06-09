const BASE = import.meta.env.VITE_API_BASE ?? '';
export const post_contact = async (formData) =>{
    try{
        const response = await fetch(`${BASE}/contact/`,{
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
