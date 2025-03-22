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
           <h1 className="inter">Insert Text Here...</h1>
           <div id="selectors">
                <button id="planner_selector" onClick={() => selector("planner")}/>
                <button id="finance_selector" onClick={() => selector("finance")}/>
           </div>
           <Planner/>
           {/* {frame == "planner" ? <Planner/>: <></>} */}
           {/* {frame == "finance" ? <Finance/>: <></>} */}
        </div>
    )
}

export default Other