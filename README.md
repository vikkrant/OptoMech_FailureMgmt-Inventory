# Tracking Inventory and Analyzing Failure for L2SI MODS Opto-Mechanical Components

## Background
Currently at LCLS there are no tools in place to keep track of opto-mechanical or optical components. This means that there is no centralized resource that keeps track of the components as they are ordered into LCLS or as they tend to break during their time at the facility. 

This is problematic for two reasons: 
- Money: Are stages more prone to failure when compared to mounts? If a higher rate of failure is observed in a certain line of stages, is this due to a recurring manufacturing issue or can this be attributed to the environment the component exists in (hutch, upstream/downstream assets etc.)? Currently, questions like these and many other related ones are unanswered leading to unfeterred flow of unchecked component failures. Consequently, replacement components are continually being ordered with prices between $2,000-8,000 resulting in a constant outflow of funds without any measures being taken to put an end to this.
- Time: Since failure is not currently analyzed, scientists are unable to prepare for component failures that might occur during the course of their experiments. The lead time to replace an opto-mechanical component is 12-18 months. So, an experiment's completion can be heavily delayed as scientists wait on replacement parts to be delivered.

To combat this, our solution is twofold:
- Tracking: Create a central space where all opto-mechanical components can be tracked, functional and broken ones
- Analyzing: Obtain characteristics about these failures 



## Tracking
[Opto-Mechanical Failure Records and Inventory.xlsx](/Opto-Mechanical_Failure_Records_and_Inventory.xlsx) is the space where all the opto-mechanical component failures found over the course of this project have been recorded. Its comprises of data collected from problem tickets gathered by [Dr. Anthony Fong](/records_AnthonyFong.xlsx) and [Dr. Adam Berges](/records_AdamBerges.pdf). 100% of the failures captured were of components manufactured by SmarAct, so the characteristics and their associated values captured may not align with the overall collection of opto-mechanical devices at LCLS. The eventual goal is for this database to keep a record of opto-mechanical components as they are shipped into LCLS from manufacturers (inventory tracking) and as they break (failure tracking).

The following characteristics have been captured for each failure

- Deployment Date: The date a given component entered operations
- Failure Date: The date when said component was first found to be malfunctioning
- Time to Failure: A non-negative integer that represents the amount of days between deployment date and failure date (not including the failure date)
- Hutch: An alphanumeric string that represents the location of the component in terms of hutches (Controls naming convention is used: LM1K4 refers to TMO, LM2K2 refers to chemRIXS)
- Serial Number W/O Production Number: An alphanumeric string that contains all the characters that are present before the dash in a component's serial number
- Production Number: A non-negative integer that indicates when a component was rolled off the assembly line (Present to the right of the dash in a component's serial number)
- PV Base: An alphanumeric string that represents a component's name and location combined
- Symptoms: A string that represents the symptoms displayed by a component upon or leading up to failure. Given that the failure records from our two primary sources, Dr. Berges and Dr. Fong, were captured independently of each other, they vary vastly in the way they record the condition of the failed components. [Dr. Fong's records](/records_AnthonyFong.xlsx) has a "Comment" column that lists the condition of a component while [Dr. Berges' records](/records_AdamBerges.pdf) have "Symptom" and "RCA" (Root cause analysis) columns where the former gives a brief overview of the part's condition while the latter delves into specifics. Since these methods of recording information regarding failure are different, a standardized list of 6 symptoms was created to which these exisiting components were fit. The method used for standardization can be found in [standardized_symptoms_key.pdf](/standardized_symptoms_key.pdf). For Dr. Berges' records, the information in the "RCA" and "Symptom" columns was combined into one column (where information from each file is in its own bullet point) as can be seen in the aformentioned file.
  
  The following are the 6 standardized symptoms:
  - Unresponsive
  - Piezo Damage
  - Cable Damage
  - Unknown
  - Inaccurate Motion
  - Intermittent Response
    


 
## Machine Learning Models
Three Features (Independent Variables):
- Serial Number W/O Production Number
- Hutch
- PV Base
  
Two Targets (Dependent Variables):
- Time to Failure
- Symptoms

"Time to Failure" is a continuous variable while "Symptoms" is a discrete variable. Thus, two machine learning models have been set up to analyze these different datatypes:

- A Linear Regression model ("Time to Failure") present in [RGRSN_TTF.py](/RGRSN_TTF.py) 
- A Naive Bayes model ("Symptoms") present in present in [CLSFN_SYMP.py](/CLSFN.SYMP.py)
- 80% data being used for training and 20% for testing
- Overfitting exists because of a small dataset and only 20-60% accuracy in results as evidenced by SKLearn's score function

## Frontend
The end goal of this initiative is for there to be for there to be a space to keep track of new opto-mechanical components as they are shipped into SLAC and of opto-mechanical components as they break and for users to be able to receive predictions regarding certain characteristics of any opto-mechanical component with a high-level of accuracy. Furthermore, the software responsible for these predictions should be accessible to all regardless of their familiarity with programming. Thus, a lightweght approach has been taken for the frontend: Easy-to-use forms.
- [index.html](/index.html): What the user will encounter upon opening the application. They will have two options, "Report" and "Test". The former will be used to submit a record of component failure or a new part that has been ordered into LCLS. The latter will be used to make predicitions regarding the targets (dependent variables) of the ML models.
- [reportFailure.html](/reportFailure.html): What the user will encounter if they choose to report component failure. All the fields (deployment date, failure date, hutch, etc.) present in this form are present as categories in the spreadsheet (the spreadsheet also contains some extra categories which are expanded on below)

Similarly, two other screens can be made: One to report inventory and another to predict predict the targets of the machine learning. Forms will be ideal here as well as it will be easy to transfer the data to the database as will be seen below

## Backend
Once the system is fully functional, if a user chooses the "record" option on the form, their information, regarding component failure or inventory, will be sent to the database through the server. [database_navigation.py](/database_navigation.py) contains several helper functions that will assist in parsing through the database and ultimately sending some information to the ML model. 
- multiLabelClassification(): Any given component is capable of displaying more than a single symptom. For example, cell H2 in our database (representing the component with serial number SLLV42sc) holds the string "Unresponsive,Piezo Damage". Logically, one can infer that this means that the component, upon or leading up to failure, was unresponsive and displayed Piezo damage. The best way for the classification model to process this information in this case is for it to receive an array like ["Unresponsive", "Piezo Damage"] which it can then encode in a binary manner. This function creates an array that has a length equivalent to the number of standardized symptoms and all elements are either 0's or 1's where the element 1 at an index indicates that the symptom represented by that index can be seen in the given component. This method of assigning more than one value to a category for classification is known as multi-label classification. Currently, the Naive Bayes model cannot perform this. An alternative would be that if a component displays n symptoms, then make n entries of that component in the database where each entry records one symptom. This, however could greatly skew predictions made by the model. Neural networks, however, are capable of handling multi-label classification so as the dataset grows over time and the model shifts from Naive Bayes to a more complex one, this approach will come in handy. 
- classifyFailures(): Parses through the database and returns an array of the indices of the components that have failed, filtering out inventory components. This is crucial because we only want datapoints that record failure being fed to the ML model to train it. 
- compModelsRatio(): Parses through the database, and for each type of component calculates the number of failed units for a specific component, the total amount of recorded units of that component in a hashmap in the form component_name:(x,y) where x represents the number of recorded failed units of a component and y represents the total number of recorded units for the same component. For example, as of 08/22/2024, the database has 3 total datapoints of "STT50.8v" components and all 3 of them represent broken units. So, when this function is run, one of the elements in the hashmap returned by the function is 'STT50.8v': (3, 3).

## Future
With this endeavor, we have only just scratched the surface of inventory tracking and failure analysis at LCLS. This repository aims to be a small building block in the development of a much more robust system that can help SLAC and its scientists monetarily and temporally. The list below gives some ideas on some changes that can be made along this path of development:
- 

