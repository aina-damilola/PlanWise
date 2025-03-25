# PlanWise
GenAI Genesis Hackathon Project

# Inspiration
Technology has made great advancements in promoting accessibility. However, it has also left people in need of it behind. Users who are unfamiliar with technology often struggle to adapt to using it, and with the world becoming more technologically oriented, non-technology inclined individuals such as the elderly are at risk of being unable to access resources such as their bank accounts as they become more and more automated. The good news is that our team at PlanWise has a solution.

# What it does
PlanWise is a comprehensive tool that simplifies and streamlines the process of accessing your bank account and planning your day-to-day activities.

Our proof of concept features a simulation of a banking system implemented through databases. The user can ask for whatever relevant banking information they wish to know by typing it in the chatbot, and PlanWise will return the information, removing the unneeded complexity of searching through menus for what they need. For simulation purposes, the user can log purchases by uploading pictures of their receipts, and it will update the user’s account.

PlanWise also offers a planning tool, where the user can provide textual information about an event or task they want to schedule, and the program will schedule it, enabling it to show up on the calendar on the UI.

# How we built it
PlanWise combines generative AI models with a React-based frontend to deliver a smart, end-to-end solution for personalized task management and financial planning. By leveraging agent-based architectures and seamless API integrations. Frontend: Built with React, providing a highly responsive and intuitive user interface.

We used Cohere’s API to power the planner component, where we processed user inputs and generated structured JSON files. These JSON files serve as blueprints that our backend logic executes to create personalized and actionable plans. Gemini’s API, deployed through an agent-based architecture, is responsible for the financial planning module. The agent autonomously interacts with LangChain and Google gemini to retrieve relevant data, perform financial analyses, and deliver tailored recommendations to users.

# Challenges we ran into
We ran into some issues with idea generation before the idea was finalized, and had trouble at some point integrating the frontend and backend together due to issues with CORS.

# Accomplishments that we're proud of
We are proud of developing an end-to-end full stack application with robust AI functionality under the time and resource constraints presented by the hackathon.

# What we learned
Some of our team members learned to develop with generative AI using APIs for the first time, and others in our team learned to use APIs to integrate frontends and backends together for the first time.

# Built With
- cohere
- flask
- google gemini
- javascript
- json
- nosql
- python
- react
