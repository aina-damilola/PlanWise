import Other from "./other"
import "./styles/mainpage.css"

function Mainpage(){
    return(
        <div id="mainpage">
            <div id="homepage">
                <h1 className="inter">PlanWise.</h1>
                <h2 className="inter">AI powered tool built for the student by the students</h2>
            </div>
            <Other/>
        </div>
    )
}

export default Mainpage