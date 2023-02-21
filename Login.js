function validate()
{
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if(username=="Dr.Redfield" && password=="computersciencerocks")
    {
        alert("Login successful");
        
    }
    else
    {
        alert("Login failed");
        
    }
}