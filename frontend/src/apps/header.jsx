import "./styles/header.css"
import pfp from "../assets/pfp.svg"

function Header(){
    return(
        
        <div id="Header">
            <img src={pfp}/>
            <div id="Links" className="inter">
                <a>Home</a>
                <a>Categories</a>
                <a>Other</a>
            </div>
            
        </div>
    )
}

export default Header