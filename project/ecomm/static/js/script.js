function validateform() {
    x= document.forms["myform"]["email"].value;
    if (x == "") {
        document.getElementById('email').placeholder = "hhhh";
        return false
    }
}

