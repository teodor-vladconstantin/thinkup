

export const createUniqueId = function(){
    return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

export const getCurentDate = ()=>{
    let date = new Date();
    return date.getDate() +'/'+date.getMonth()+'/'+date.getFullYear();
}

export const verifyText = (text, maxLength, required = false) => {
    if (text == undefined || text == null) {
        return !required;
    }
    if (required && text.trim().length === 0) return false;
    if (text.length > maxLength) return false;
    return true;
}