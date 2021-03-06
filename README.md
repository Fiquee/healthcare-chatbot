# healthcare-chatbot

Natural Language Processing Assignment

In this assignment we are required to build an NLP application in order to help in healthcare domain.

### **Overview**

- We decided to build a chatbot that will act as a platform for the end user to give feedback about the healthcare they were in
- The chatbot will be include with two NLP models:
  - sentiment analysis model: to predict polarity of the reviews
  - multiclass text classification model: to predict the category/categories of the reviews
- The classes we chose are:
  - Appointment
  - Facilities
  - Staff
  - Treatment

### **Dataset**

- dataset was collected by scrapping hospital/clinic reviews from Google Maps reviews

### **Model used**

- We plan to implement a pre-trained model by Spacy and retrain with our dataset

### Running the Application

1. Run the command `pip install -r requirements.txt` to install the required modules.
2. Download the application configuration files (private to the team members)
3. Place the `.env` file and the service account file in the `app` folder.
4. Run the following sequence of commands to start the app:
   ```
   cd app
   streamlit run app.py
   ```
