var Helpers = {

    randomString: function (length) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    },

    makeOperation: function(type, payload={}){
        var op = {
            "cmd": type,
            "payload": payload
        }
 
        return JSON.stringify(op)
    }
}

export default Helpers;