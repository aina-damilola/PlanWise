import Other from "./other"
import "./styles/mainpage.css"

function Mainpage(){
    const handleScroll = () => {
        window.scrollTo({
            top: window.scrollY + 500,  
            behavior: "smooth",        
        });
    };



    return(
        <div id="mainpage">
            <div id="homepage">
                <h1 className="inter">PlanWise.</h1>
                <h2 className="inter">Insert your one-liner slogan in here... </h2>
                <button id="scroll_down" className="jump" onClick={handleScroll}/>
            </div>
            <Other/>
        </div>
    )
}

export default Mainpage