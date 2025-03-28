import { useState } from "react"
import "./styles/other.css"
import Planner from "./planner"
import Finance from "./finance"

function Other(){
    const [frame, setFrame] = useState(null)

    function selector(type){
        setFrame(type)
    }
    
    return(
        <div id="other">
           <h1 className="inter">What aspect of your life do you want to plan?</h1>
           <div id="selectors">
                <button id="planner_selector" onClick={() => selector("planner")}/>
                <button id="finance_selector" onClick={() => selector("finance")}/>
           </div> 
           
           {frame == "planner" ? <Planner/>: <></>} 
           {frame == "finance" ? <Finance/>: <></>} 
        </div>
    )
}

export default Other