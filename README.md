# Tracking Inventory and Analyzing Failure for L2SI MODS Opto-Mechanical Components

## Background
Currently at LCLS there are no tools in place to keep track of opto-mechanical or optical components. This means that there is no centralized resource that keeps track of the components as they are ordered into LCLS or as they tend to break during their time at the facility (over the course of experiments or in other ways). 

This is problematic for two reasons: 
- Money: Are stages more prone to failure when compared to mounts? If a higher rate of failure is observed in a certain line of stages, is this due to a recurring manufacturing issue or can this be attributed to the environment the component exists in (hutch, upstream/downstream assets etc.)? Currently, questions like these and other related ones are unanswered leading to unfeterred flow of unchecked component failures. Consequently, replacement components are continually being ordered with prices between $2,000-8,000 resulting in a constant outflow of funds without any measures being taken to put an end to this.
- Time: Since failure is not currently analyzed, scientists are unable to prepare for component failures that might occur during the course of their experiments. The lead time to replace an opto-mechanical component is 12-18 months. So, an experiment's completion can be heavily delayed as scientists wait on replacement parts to be delivered.

To combat this, our solution is twofold:
- Tracking: Create a central space where all opto-mechanical components can be tracked, functional and broken ones
- Analyzing: Obtain characteristics about these failures 



## Tracking
[724Ready.xlsx](/724Ready.xlsx) is the central space where all the opto-mechanical component failures found over the course of this project have been recorded. Its comprises of [---# Number of tickets from Dr. Berges---] and [---# Number of tickets from Dr. Fong---]

The following characteristics have been captured for each failure ***(The categories below have all been captured with SmarAct components in mind. For example, "Serial Number W/O Production Number" assumes that the user will enter a serial number that contains a dash.)***

- Deployment Date: The date a given component entered operations
- Failure Date: The first recorded instance of said component malfunctioning
- Time to Failure: Days between deployment date and failure date (not including the failure date)
- Hutch: The hutch the component is present in (Controls naming convention is used [---SPECIFY THE CONVENTION---])
- Serial Number W/O Production Number: An alphanumeric string that contains all the characters that are present before the dash in a component's serial number
- Production Number: A positive integer that indicates when a component was rolled off the assembly line (Present to the right of the dash in a component's serial number)
- PV Base: [---WHAT IS THIS---]
- Symptoms: The symptoms displayed by a component upon or leading up to failure. These have been standardized using the following list:
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

- A Linear Regression model ("Time to Failure") present in [RGRSN_TTF.ipynb](/RGRSN_TTF.ipynb) 
- A Naive Bayes model ("Symptoms") present in present in [CLSFN_SYMP.ipynb](/CLSFN.SYMP.ipynb)
- 80% data being used for training and 20% for testing
- Overfitting exists because of a small dataset and only 20-60% accuracy in results as evidenced by SKLearn's score function

## UI Functionality
[SCRIPTS.ipynb](/SCRIPTS.ipynb) contains several functions that will update the database as users input information into the forms 
- Binary Encoding Symptoms: One component is capable of displaying more than a single symptom. This function creates an array that has a length equivalent to the number of standardized symptoms and all elements are either 0's or 1's where the element 1 at an index indicates that the symptom represented by that index can be seen in the given component
- Filtering Components to be Analyzed: Parses through the database and returns an array of the indices of the components that have failed, filtering out inventory components
- Calculating Ratio of Failed V/S Working Components: Parses through the database, and for each type of component calculates the number of failed units for a specific component, the total amount, and the ratio of failed to working components and then writes these values to the dataframe

## Future 

