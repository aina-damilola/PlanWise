import "./styles/header.css"
import pfp from "../assets/planwise.png"

function Header(){
    const handleScroll = () => {
        const targetElement = document.getElementById("other");

        // Scroll to the element smoothly if it exists
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: "smooth",  // Enables smooth scrolling
                block: "start",      // Aligns the element to the top of the viewport
            });
        }
    }
    const handleScrollHome = () => {
        const targetElement = document.getElementById("homepage");

        // Scroll to the element smoothly if it exists
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: "smooth",  // Enables smooth scrolling
                block: "start",      // Aligns the element to the top of the viewport
            });
        }
    }

    return(
        

        <div id="Header">
            <img src={pfp} onClick={handleScroll}/>
            <div id="Links" className="inter">
                <a onClick={handleScroll}>Categories</a>
            </div>
            
        </div>
    )
}

export default Header